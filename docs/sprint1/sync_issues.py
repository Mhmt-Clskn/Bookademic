#!/usr/bin/env python3
"""
Sync GitHub Issues with issues.csv (title, body, labels, assignee).

Usage (after `gh auth login`):
    python3 sync_issues.py <owner>/<repo>            # dry run: prints what would change
    python3 sync_issues.py <owner>/<repo> --apply    # applies the changes

- Existing Issues are matched by the ID prefix of their title ("US-18:", "EN-03:").
- Missing Issues (e.g. the new US-23) are created.
- Labels are set to exactly the CSV labels (e.g. `devops` is removed from EN-02).
- Fill in ASSIGNEES with GitHub usernames before running; empty entries are skipped.
"""
import csv, json, subprocess, sys

ASSIGNEES = {
    "Mehmet": "Mhmt-Clskn",
    "Melih": "",
    "Mürsel": "",
    "Mirac": "",
    "Emir": "",
    "Sıla": "",
}

def gh(*args, apply=True):
    if not apply:
        print("   [dry-run] gh " + " ".join(a if " " not in a else repr(a) for a in args[:6]) + (" ..." if len(args) > 6 else ""))
        return ""
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    repo, apply = sys.argv[1], "--apply" in sys.argv
    rows = list(csv.DictReader(open("issues.csv", encoding="utf-8-sig")))

    issues = json.loads(gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "500",
                           "--json", "number,title,labels,assignees"))
    by_id = {i["title"].split(":")[0].strip(): i for i in issues if ":" in i["title"]}

    for lab in sorted({l for r in rows for l in r["labels"].split(",")}):
        gh("label", "create", lab, "--repo", repo, "--force", apply=apply)

    for r in rows:
        want = set(r["labels"].split(","))
        user = ASSIGNEES.get(r["owner"], "")
        cur = by_id.get(r["id"])
        if cur is None:
            print(f"+ create {r['id']}")
            args = ["issue", "create", "--repo", repo, "--title", r["title"], "--body", r["body"],
                    "--label", ",".join(sorted(want))]
            if user:
                args += ["--assignee", user]
            gh(*args, apply=apply)
            continue
        have = {l["name"] for l in cur["labels"]}
        args = ["issue", "edit", str(cur["number"]), "--repo", repo, "--title", r["title"], "--body", r["body"]]
        if want - have:
            args += ["--add-label", ",".join(sorted(want - have))]
        if have - want:
            args += ["--remove-label", ",".join(sorted(have - want))]
        if user and user not in {a["login"] for a in cur["assignees"]}:
            args += ["--add-assignee", user]
        note = []
        if cur["title"] != r["title"]: note.append("title")
        if want != have: note.append(f"labels +{sorted(want-have)} -{sorted(have-want)}")
        if "--add-assignee" in args: note.append(f"assign {user}")
        print(f"~ #{cur['number']} {r['id']}: body" + (", " + ", ".join(note) if note else ""))
        gh(*args, apply=apply)

    missing = [k for k, v in ASSIGNEES.items() if not v]
    if missing:
        print(f"\n! No GitHub username for: {', '.join(missing)} — their Issues were not assigned.")
    if not apply:
        print("\nDry run only. Re-run with --apply to make the changes.")

if __name__ == "__main__":
    main()
