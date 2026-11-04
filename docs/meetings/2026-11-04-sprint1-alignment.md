# Decision Record – Sprint 1 Work and Document Alignment

| Field | Value |
| --- | --- |
| Period | 2–4 November 2026 |
| Medium | Asynchronous: team chat and GitHub pull-request reviews |
| Participants | Melih, Sıla, Mürsel, Mirac, Mehmet, Emir |
| Recorded by | Sıla (Scrum Master) |

Sprint 1 tasks planned on [31 October](2026-10-31-topic-roles-and-planning.md) started on 2 November. Once the first drafts were in, the Scrum Master cross-checked all documents and the team corrected them in a fixed order. This record lists the decisions taken during that work.

## Topics

1. Project name and technology stack
2. Notification scope (in-app vs. e-mail)
3. Cross-check of all Sprint 1 documents
4. Order of corrections before the 5 November submission

## Decisions

| # | Decision | Rationale |
| --- | --- | --- |
| D1 | Project name: **Bookademic** (3 Nov); repository moved to the `bookademic-team` organization | Team vote; EN-01 requires a GitHub organization |
| D2 | Technology stack accepted as in [ADR-0001](../adr/0001-tech-stack.md): .NET 10, PostgreSQL 17, React + Vite + JavaScript + Ant Design | Reviewed in the ADR pull request; Mürsel sets the status to Accepted |
| D3 | US-04 is the **in-app notification** story (Must, `GET /notifications`); e-mail notification is a new **Should** story, **US-23** (owner Sıla) | Agreed by Melih and Mürsel on 3 Nov; keeps the MVP free of an external dependency |
| D4 | The Product Owner's documents (`backlog.md`, `vision.md`, `issues.csv`, PR #38) are the reference for every other document | One source of truth for story IDs, priorities and acceptance criteria |
| D5 | Corrections are applied in order: Melih (PR #38) → Mirac (`test-plan.md`) → Mürsel (`openapi.yaml`, `story-mapping.md`, ADR-0001). Emir, Mehmet and Sıla work in parallel | Later documents are aligned to merged versions, so fixes do not overwrite each other |
| D6 | A reservation overlaps if it collides with a PENDING, APPROVED or **CHECKED_IN** booking (US-06) | Matches the `EXCLUDE … WHERE status IN (...)` constraint in ADR-0001 |
| D7 | The "start time in the past → 400" rule is **deferred to Sprint 2** and removed from the test plan | It is not in the backlog or the contract; adding it now would touch three documents a day before submission |
| D8 | `story-mapping.md` is generated from `x-story`; US-23 is listed under "Work items without an endpoint" instead of the table | Avoids hand edits to a generated table |
| D9 | The docker-compose skeleton follows ADR-0001: services `db` (PostgreSQL 17), `api`, `web`, `mailpit` | Backlog EN-03 acceptance criterion |

## Correction tasks

The Sprint 1 tasks themselves were assigned on 31 October; the items below are only the corrections that came out of the cross-check.

| Owner | Action | Due |
| --- | --- | --- |
| Melih | US-06 overlap rule (checked-in), vision e-mail scope (US-23), GitHub usernames in `sync_issues.py` – done in PR #38; final survey results in `proposal.md` | 5 Nov 12:00 |
| Mirac | Align `test-plan.md` story IDs with the backlog (US-01/02, US-06, US-07, US-11/12, US-17, US-18, US-23); RFC 9457, `tstzrange`, 50% CI threshold | 4 Nov |
| Mürsel | Reference US-23 in `openapi.yaml` and `story-mapping.md`; set ADR-0001 to Accepted | 5 Nov 12:00 |
| Emir | `ui-screens.md`: module names as in ADR-0001, US-23 by ID, separate register/sign-in errors on SCR-01 | 5 Nov 12:00 |
| Mehmet | Align `docker-compose.yml` with ADR-0001; fix `LICENSE`; set default branch to `develop`; run `sync_issues.py` | 5 Nov 12:00 |
| Sıla | `raci.md`: US-23 and US-07 by ID, ADR row set to I/I/A-R/C/C/I | 5 Nov 12:00 |

**Next meeting:** 5 November 2026 – Sprint 1 review and retrospective
