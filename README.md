# Bookademic

**A project support platform for university departments.** Bookademic manages, in a single flow, the two scarce resources a project student needs: the instructor's time and the laboratory.

> SENG 321 – Software Engineering Project · Fall 2026 · Current release: **Sprint 1 – Project Foundation** (`v0.1.0-sprint1`)

---

## The problem

Office hours and lab equipment are booked manually and are disconnected from each other: students queue at the instructor's door, the same oscilloscope can be given to two teams, expensive devices are used without training, and the instructor's approval for lab use lives in an e-mail that the lab staff cannot see. See the [Project Proposal](docs/sprint1/proposal.md) for the full problem statement and evidence.

## How Bookademic solves it

Everything is modelled as **a resource + a time slot**, handled by one shared booking core. The two domains are connected through the student's project journey:

1. The student books an **office-hour appointment** with a topic note.
2. In the meeting, the instructor grants **lab access approval** for a device category.
3. The student completes a **device training** with a research assistant and is authorised for that category.
4. The student **reserves the device**; overlapping requests are rejected (`409`).
5. The research assistant **approves** the request and hands over the device.

If an instructor cannot come in, the department secretary cancels the office hours and affected students are notified in the app.

### Actors

| Actor | Main goals |
|---|---|
| Student | Book office hours, get lab approval and training, reserve devices |
| Instructor | Define office hours, see topics in advance, grant lab approval |
| Research Assistant | Run support and training hours, manage the device catalogue and lab requests |
| Department Secretary | Cancel office hours, view usage reports |
| Admin | Manage users and roles |

## Architecture

Bookademic is a **modular monolith** with four modules ([ADR-0001](docs/adr/0001-tech-stack.md)):

| Module | Responsibility |
|---|---|
| M1 – Identity | Registration, login (JWT), 5 roles (RBAC), in-app notifications, usage reports |
| M2 – Booking Core | Shared conflict check, reservation state machine, status history |
| M3 – Lab | Device/room catalogue, lab approval, training authorisation, handover, maintenance |
| M4 – Office Hours | Office, support and training hours; appointments; cancellation and redirection |

M3 and M4 never implement their own conflict logic; every lab reservation and every appointment is an M2 reservation. Double booking is prevented at database level with a PostgreSQL `EXCLUDE` constraint, so it cannot happen even under concurrent requests.

## Tech stack

| Layer | Choice |
|---|---|
| Backend | .NET 10 (LTS), ASP.NET Core Web API, EF Core 10 |
| Database | PostgreSQL 17 |
| Frontend | React, Vite, JavaScript, Ant Design, React Router |
| API contract | OpenAPI 3.1 – [`docs/api/openapi.yaml`](docs/api/openapi.yaml) (single source of truth) |
| E-mail (dev) | Mailpit |
| Tests | xUnit, coverlet, Testcontainers, ArchUnitNET, Playwright |
| Quality and delivery | GitHub Actions, SonarQube, Docker Compose |

## Getting started

**Prerequisite:** Docker with Docker Compose v2.

```bash
git clone https://github.com/bookademic-team/Bookademic.git
cd Bookademic
docker compose up
```

| Service | URL |
|---|---|
| API | http://localhost:8080/api/v1 |
| Web app | http://localhost:5173 |
| Mailpit (dev inbox) | http://localhost:8025 |
| PostgreSQL | `localhost:5432` |

> **Sprint 1 status:** the compose file starts the infrastructure skeleton (`db`, `api`, `web`, `mailpit`). The `api` and `web` containers are placeholders until the application code is added in Sprint 3.

**Work against the API before the backend exists:** the contract can be mocked with Prism.

```bash
npx @stoplight/prism-cli mock docs/api/openapi.yaml
```

The contract can also be viewed in [Swagger Editor](https://editor.swagger.io/) by pasting `docs/api/openapi.yaml`.

## Documentation

| Document | Description | Owner |
|---|---|---|
| [Project Proposal](docs/sprint1/proposal.md) | Problem, evidence, stakeholders, solution, feasibility, risks, license | Melih |
| [System Vision & Boundary](docs/sprint1/vision.md) | Scope, context diagram, constraints, actors and use cases | Melih |
| [Product Backlog](docs/sprint1/backlog.md) | Epics, user stories, acceptance criteria, estimates, owners | Melih |
| [Student Survey](docs/sprint1/survey.md) | Primary-evidence survey and analysis plan | Melih |
| [OpenAPI Contract](docs/api/openapi.yaml) | API-first contract (v0.2.2) | Mürsel |
| [Story ↔ API Mapping](docs/api/story-mapping.md) | Traceability from backlog stories to API operations | Mürsel |
| [ADR-0001 Tech Stack](docs/adr/0001-tech-stack.md) | Architecture and technology decisions | Mürsel |
| [Test Plan](docs/test-plan.md) | Test strategy, levels, coverage goals, quality gates | Mirac |
| [Screen List & Flow](docs/ui-screens.md) | Screens per role, main user journey, error messages | Emir |
| [Team Roles & RACI](docs/sprint1/raci.md) | Responsibilities and RACI matrix | Sıla |
| [Git-Flow & Repository Workflow](docs/sprint1/git-flow.md) | Branch model, protection, PR and review rules, releases | Sıla |
| [Individual Contributions](CONTRIBUTIONS.md) | Each member's role, work and GitHub links | Sıla |
| [Meeting Notes](docs/meetings/) | Team decisions and action items | Sıla |

## Repository structure

```text
.
├── backend/              # .NET solution (from Sprint 3)
├── web/                  # Vite + React + Ant Design (from Sprint 3)
├── docs/
│   ├── adr/              # architecture decision records
│   ├── api/              # openapi.yaml and story mapping
│   ├── meetings/         # meeting notes
│   ├── sprint1/          # proposal, vision, backlog, survey, RACI, Git-Flow
│   ├── test-plan.md
│   └── ui-screens.md
├── .env.example          # default database settings for docker compose
├── CONTRIBUTIONS.md      # individual contributions with GitHub links
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Team

| Member | Role |
|---|---|
| Melih | Product Owner & Requirements Engineer |
| Sıla | Scrum Master & Agile Process Coach |
| Mürsel | Lead Software Architect & Technical Lead |
| Mirac | Quality Assurance & Test Automation Engineer |
| Mehmet | DevOps & CI/CD Infrastructure Engineer |
| Emir | Implementation & Integration Engineer |

Detailed responsibilities are in the [RACI matrix](docs/sprint1/raci.md); each member's Issues, pull requests, reviews and commits are listed in [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

## How we work

Full rules: [Git-Flow & Repository Workflow](docs/sprint1/git-flow.md).

- **Branches (Git-Flow):** `main` holds released versions only; `develop` is the integration branch; every task gets its own `feature/<issue-no>-<short-name>` branch created from `develop`.
- **Issues:** every user story, enabler and fix is a GitHub Issue with module, priority and story-point labels, tracked on the GitHub Projects board.
- **Pull requests:** every change reaches `develop` through a PR that references its Issue (`Closes #<no>`) and has at least one approving review. Nobody approves their own PR.
- **Merging:** "Create a merge commit" only (no squash), and branches are kept, so each member's commit history stays intact.
- **Commit messages:** [Conventional Commits](https://www.conventionalcommits.org/) in English, e.g. `feat(M2): add overlap check for reservations (#12)`.
- **Releases:** at the end of each sprint `develop` is merged into `main` and tagged (`v0.1.0-sprint1`, …).

## Roadmap

| Sprint | Deliverables |
|---|---|
| Sprint 1 | Proposal, vision and boundary, OpenAPI draft, roles and RACI, Git-Flow, initial backlog |
| Sprint 2 | SRS and refined backlog, non-functional requirements, Figma prototypes, C4 and UML |
| Sprint 3 | First working MVP, GitHub Actions CI with ≥ 50% unit-test coverage |
| Final | Live product with one Docker command, integration and E2E test report, SonarQube report, demo and architectural defense |

## License

Released under the [MIT License](LICENSE).
