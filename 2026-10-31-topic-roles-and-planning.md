# Meeting Notes – Topic, Roles and Sprint 1 Planning

| Field | Value |
| --- | --- |
| Date | 31 October 2026 |
| Medium | Microsoft Teams (online) |
| Attendees | Melih, Sıla, Mürsel, Mirac, Mehmet, Emir |
| Minutes taken by | Sıla (Scrum Master) |

## Agenda

1. Project topic and the instructor's feedback
2. Team roles
3. Architecture direction
4. Working agreements (GitHub, reviews, merging)
5. Sprint 1 task assignment

## Decisions

| # | Decision | Rationale |
| --- | --- | --- |
| D1 | Topic: **office hours + lab/equipment reservation** on one platform, built around the student's project journey | The instructor said an office-hours-only app would be too simple and asked for at least 3–4 actors |
| D2 | Actors: Student, Instructor, Research Assistant, Department Secretary, Admin (+ SMTP as an external system) | Every main use case involves at least 3 actors |
| D3 | Four modules: M1 Identity/Notifications, M2 Booking Core, M3 Lab, M4 Office Hours | One shared booking core; M3 and M4 do not implement their own conflict logic |
| D4 | Team roles are assigned as in the [Team roles](#team-roles) table below | Course role list; responsibilities in [`raci.md`](../sprint1/raci.md) |
| D5 | The backend is a modular monolith; Mürsel proposes the technology stack in an ADR | Microservices would slow a 10-week project down; conflict guarantees fit in one transaction |
| D6 | Frontend: Emir sets up the skeleton (layout, routing, API client); everyone builds the screens of their own stories | Individual contribution is visible in both backend and frontend |
| D7 | Git-Flow (`main`, `develop`, `feature/<issue-no>-<name>`); every change goes through a pull request with `Closes #<no>` and at least one approval; no self-approval | Course rule and traceability between Issues and code |
| D8 | Pull requests are merged with a merge commit; no squash, branches are not deleted | Course rule: repository history must remain intact |
| D9 | Public repository, MIT license | Branch protection on GitHub Free works only on public repositories |
| D10 | Sprint 1 work starts on 2 November; all deliverables are merged into `develop` by 5 November 12:00 | Submission deadline 5 November 23:59 |

## Team roles

| Member | Role |
| --- | --- |
| Melih | Product Owner & Requirements Engineer |
| Sıla | Scrum Master & Agile Process Coach |
| Mürsel | Lead Software Architect & Technical Lead |
| Mirac | Quality Assurance & Test Automation Engineer |
| Mehmet | DevOps & CI/CD Infrastructure Engineer |
| Emir | Implementation & Integration Engineer |

Detailed responsibilities and the RACI matrix: [`docs/sprint1/raci.md`](../sprint1/raci.md).

## Action items

| Owner | Action | Due |
| --- | --- | --- |
| Mehmet | GitHub organization, public repository, `main`/`develop`, branch protection, labels, templates | 3 Nov |
| Mürsel | ADR-0001 (technology stack) pull request; everyone reviews | 4 Nov |
| Mürsel, Emir | `docs/api/openapi.yaml` pull requests | 4 Nov |
| Melih | Proposal, vision, survey, backlog; backlog entered as Issues | 4 Nov |
| Sıla | `raci.md`, review plan, GitHub Projects board, meeting notes, README | 4 Nov |
| Mirac | Acceptance-criteria review, test plan | 5 Nov |
| Emir | Screen list (`docs/ui-screens.md`) | 5 Nov |
| Sıla, Mehmet | Release PR `develop` → `main`, tag `v0.1.0-sprint1` | 5 Nov |
