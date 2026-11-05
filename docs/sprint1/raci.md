# Bookademic – Team Roles and RACI Matrix

**Owner:** Sıla (Scrum Master) · **Last updated:** November 4, 2026

## 1. Team roles

| Member | Role | Area of responsibility | Sprint 1 deliverables | Code ownership (Sprint 3+) |
| --- | --- | --- | --- | --- |
| Melih | Product Owner & Requirements Engineer | Product | Project proposal, system vision and boundary, user survey, product backlog | M3: US-11, US-13, US-14 |
| Sıla | Scrum Master & Agile Process Coach | Process | Roles and RACI, GitHub Projects board, meeting records, submission coordination | M1: US-05, US-23 · M2: US-09 · M3: US-12, US-16 |
| Mürsel | Lead Software Architect & Technical Lead | Architecture | OpenAPI YAML contract, technology stack decision (ADR) | M2: US-06, US-08 (core engine and module template) |
| Mirac | Quality Assurance & Test Automation Engineer | Quality | Testability review of acceptance criteria, draft test plan | M2: US-07 (conflict-engine and access-rule tests) · M3: US-15 · M4: US-20 |
| Mehmet | DevOps & CI/CD Infrastructure Engineer | DevOps | GitHub organization, repository, branch protection, docker-compose skeleton, release tag | M1: US-01–US-04 · EN-01, EN-03, EN-04 |
| Emir | Implementation & Integration Engineer | Implementation and integration | OpenAPI M4 contribution, screen list and main user-journey screen flow | M4: US-10, US-17–US-19, US-21, US-22 · frontend skeleton |

**R** = Responsible (does the work) · **A** = Accountable (owns the outcome; exactly one per row) · **C** = Consulted (gives input) · **I** = Informed (kept up to date)

## 2. Sprint 1 RACI matrix

| Sprint 1 deliverable | Melih | Sıla | Mürsel | Mirac | Mehmet | Emir |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| Project proposal and problem definition | A/R | C | C | I | I | C |
| User survey and primary evidence | A/R | C | I | C | I | I |
| System vision and boundary | A/R | I | C | I | I | C |
| OpenAPI YAML contract | C | I | A/R | C | I | R |
| Technology stack decision (ADR) | I | I | A/R | C | C | I |
| Team roles and RACI matrix | C | A/R | C | C | C | C |
| GitHub organization and repository structure | I | C | C | I | A/R | I |
| Git-Flow and branch protection rules | I | A | C | C | R | I |
| GitHub Projects board and Issues | C | A/R | I | I | C | I |
| Initial product backlog | A/R | C | C | C | I | C |
| Testability of acceptance criteria | A | I | I | R | I | I |
| Draft test plan | C | I | C | A/R | I | I |
| Screen list and screen flow | C | I | C | I | I | A/R |
| docker-compose skeleton | I | I | C | I | A/R | I |
| Meeting records | I | A/R | I | I | I | I |
| Sprint 1 release tag and submission | C | A | C | I | R | I |

## 3. Project-wide RACI matrix (Sprint 2 – Final)

> This section is a **plan** for the upcoming sprints and shows what each role covers over the semester. It is reviewed at the start of every sprint and updated if needed.

| Deliverable | Sprint | Melih | Sıla | Mürsel | Mirac | Mehmet | Emir |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| SRS and refined backlog | 2 | A/R | C | C | C | I | C |
| Non-functional requirements and quality measures | 2 | C | I | C | A/R | C | I |
| Figma prototypes and user flows | 2 | A | I | C | C | I | R |
| C4 model and UML document | 2 | C | I | A/R | C | C | C |
| Stand-up and retrospective records, contribution tracking | 2–Final | I | A/R | I | I | I | I |
| MVP development (own user stories) | 3 | R | R | A/R | R | R | R |
| Frontend skeleton and API integration | 3 | I | I | C | I | I | A/R |
| Code review and PR approval process | 3–Final | I | I | A/R | R | I | I |
| GitHub Actions CI pipeline | 3 | I | I | C | C | A/R | I |
| Unit test coverage ≥ 50% | 3 | R | R | R | A/R | R | R |
| Single-command Docker / docker-compose run | Final | I | I | C | C | A/R | C |
| Integration and E2E test report | Final | I | I | C | A/R | C | R |
| SonarQube analysis and technical debt report | Final | I | I | C | C | A/R | I |
| Live demo and architectural defense | Final | R | R | A/R | R | R | R |

## 4. Working agreements

- Every task is a GitHub Issue and is done on its own `feature/<issue-no>-<short-name>` branch.
- Every change enters `develop` through a Pull Request; at least 1 approval is required, and nobody approves their own PR.
- PRs are merged with a **regular merge commit** (no squash), and branches are not deleted, so each member's commit history stays intact.
- Before submission, every member has at least **1 Issue, 1 PR and 1 review** under their own account.
- Nobody pushes someone else's work from their own account.
- The names in these tables must match the commit and PR authors on GitHub.
