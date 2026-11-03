# ADR 0001 – Technology Stack

| Field | Value |
|---|---|
| Status | Proposed (team approval is given in the review of this ADR's pull request) |
| Date | 2026-11-02 (revised 2026-11-03) |
| Decision owner (A) | Mürsel – Lead Software Architect |
| Consulted (C) | Mehmet (DevOps), Mirac (QA) |
| Informed (I) | Emir (Implementation), Melih (PO), Sıla (SM) |
| Related work | EN-02, EN-03, EN-04 |

## Context

Bookademic will be built in 10 weeks by a team of 6 and consists of four modules: M1 Identity/Notifications, M2 Booking Core, M3 Lab, M4 Office Hours. M3 and M4 do not implement their own conflict logic; they use M2.

Course requirements shape the technology choice directly: API-first (OpenAPI YAML), a single `docker compose up` command, at least 50% unit-test coverage in CI, SonarQube analysis, and dependencies compatible with the MIT license.

The most critical technical risk is double booking under concurrent requests. With a "check first, then write" approach, two requests can pass the check at the same time and take the same interval. The chosen stack must rely on a mechanism that guarantees correctness rather than on application code alone.

On the frontend, most screens are forms, tables, date-range selection and approval flows: catalogue filtering, the approval queue, office-hour definition, the day's appointments. The target platform is the desktop web browser; a mobile app is out of scope. The user interface is in English.

## Decision

### Backend and infrastructure

| Layer | Choice | Rationale |
|---|---|---|
| Backend | .NET 10 (LTS) + ASP.NET Core Web API | Experience of the technical lead and the team; strong type system. .NET 10 is supported until November 2028. .NET 8 and .NET 9 reach end of support on 10 November 2026, at the very start of the project, so they were not chosen ([Microsoft announcement](https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/)). |
| Architectural style | Modular monolith | One deployment unit, one compose service. Modules are separate projects and talk to each other only through contract projects. |
| Data access | EF Core 10 + Npgsql, code-first migrations | Schema changes are versioned and can be reviewed in pull requests. |
| Database | PostgreSQL 17 | Conflicts are prevented at database level with `tstzrange` and an `EXCLUDE` constraint (see below). |
| Authentication | ASP.NET Core JWT Bearer + role-based policies | The 5 roles (RBAC) are enforced with the built-in `[Authorize(Roles=...)]`. Passwords are hashed with ASP.NET Core `PasswordHasher`. |
| E-mail | MailKit; Mailpit in development | MailHog is no longer maintained; Mailpit does the same job and is actively maintained. |
| API contract | `docs/api/openapi.yaml` is the single source of truth | Code follows the contract, not the other way round. Until the backend is ready, the frontend works against a Prism mock server. |
| Backend tests | xUnit, coverlet, Testcontainers (PostgreSQL), ArchUnitNET | Unit and integration tests; ArchUnitNET tests module boundaries. Coverage reports go to CI and SonarQube in Cobertura format. |
| E2E tests | Playwright | The main user journey is tested through the browser. |
| Quality | SonarQube (`dotnet-sonarscanner`), `.editorconfig`, `dotnet format` | For the technical-debt report in the final submission. |
| Packaging | Multi-stage Dockerfile (sdk → aspnet runtime, `10.0` images); docker compose services: `db`, `api`, `web`, `mailpit` | Meets the single-command requirement. |

**Coverage measurement and threshold.** The `coverlet.collector` package measures coverage and produces a report with `dotnet test --collect:"XPlat Code Coverage"`, but it does not fail the build when coverage is low. To meet EN-04's "CI fails below 50%" criterion, CI will enforce the threshold with `coverlet.msbuild` (`/p:Threshold=50`) or ReportGenerator.

### Frontend

| Tool | Role | Rationale |
|---|---|---|
| React | UI library | Widely used, component-based, plenty of learning material. |
| JavaScript | Language | Chosen over TypeScript to reduce the team's learning load (see alternatives). |
| Vite | Dev server and build | Fast development; the `react` template ships with ESLint. |
| Ant Design | Single UI component library | Table (filtering, sorting, paging), form with built-in validation, date-range picker (`RangePicker`) and calendar (`Calendar`) in the free package. MIT licensed. Used with its default English locale. |
| React Router | Routing | Every screen has its own URL; the back button and page refresh work; page access is checked by role. |
| Day.js | Date and time handling | Ant Design's date components work with Day.js objects, so it is not a separate choice. Used with its default English locale. |
| `fetch` | API calls | Built into the browser; no extra library needed. |

Frontend rules:

1. **Single UI library.** No second UI library (MUI, Bootstrap, etc.) is added, so screens look consistent and styles do not clash.
2. **Design and code use the same building blocks.** The Figma prototypes in Sprint 2 are drawn with Ant Design components, so every designed screen can be built one-to-one in code.
3. **Single API layer.** Every request to the backend lives in `src/api/client.js`. Field names are kept in one place; when the contract changes, only this file changes.

### Conflict engine: why PostgreSQL

Every reservation is a resource plus a half-open time interval `[start, end)`, so 10:00–11:00 and 11:00–12:00 do not overlap (US-07). Overlaps between active records are prevented by a database constraint:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE booking.reservations
  ADD CONSTRAINT no_overlapping_active_reservations
  EXCLUDE USING gist (resource_id WITH =, period WITH &&)
  WHERE (status IN ('PENDING', 'APPROVED', 'CHECKED_IN'));
```

The application first checks with a query and returns a meaningful `409 SLOT_UNAVAILABLE`. If two requests still arrive at the same moment, the second one hits the constraint (SQLSTATE `23P01`), which is translated into the same 409 response. Double booking therefore cannot happen even in a race.

Office-hour appointments use the same engine: the time of an instructor or research assistant is also a resource. This is how the "everything is a resource plus a time slot" claim is implemented in the database.

### Module structure

```text
backend/
├── Bookademic.sln
├── src/
│   ├── Bookademic.Api/                   # host: Program.cs, DI, auth, middleware
│   └── Modules/
│       ├── Identity/                     # M1
│       ├── Booking/                      # M2 – shared core
│       │   ├── Bookademic.Booking.Contracts/   # IBookingEngine, IEligibilityPolicy, DTOs
│       │   └── Bookademic.Booking.Core/        # conflict engine, state machine, history
│       ├── Lab/                          # M3
│       └── OfficeHours/                  # M4
└── tests/
    ├── Bookademic.Tests/                 # unit tests (name to be confirmed with Mirac)
    ├── Bookademic.IntegrationTests/      # Testcontainers
    └── Bookademic.ArchitectureTests/     # ArchUnitNET rules

web/                                      # Vite + React + Ant Design
└── src/
    ├── api/client.js                     # single API layer
    ├── pages/                            # React Router pages
    └── components/
```

Naming: the product name is **Bookademic**. .NET solutions, projects and namespaces use `Bookademic` (e.g. `Bookademic.Api`); repository, Docker images and container names use lower case `bookademic`.

Dependency rules:

1. M3 and M4 create reservations and change their status only through the `IBookingEngine` interface in `Bookademic.Booking.Contracts`.
2. M2 does not know resource-specific rules. Before creating a reservation it calls the `IEligibilityPolicy` registered for the resource type: M3 provides the lab approval + device training rule, M4 provides the daily appointment limit. A new resource type (e.g. a meeting room) is supported by adding a new policy only; the core does not change.
3. Modules may not reference each other's internal projects. This rule is written as a test in `Bookademic.ArchitectureTests` and runs in CI.

## Alternatives considered

**Microservices.** Rejected. For 10 weeks and 6 people they add inter-service communication, separate databases and distributed transactions, while the course asks for a system that starts with one command. The clear boundaries of the modular monolith still allow splitting later if needed.

**Java/Spring Boot, TypeScript/NestJS, Python/FastAPI.** All technically suitable. The deciding factor was the .NET experience of the technical lead and the team; EF Core and the .NET test ecosystem also meet the needs.

**.NET 8 (LTS) and .NET 9.** Rejected. Both reach end of support on 10 November 2026; since the project runs until January 2027, almost the entire term would be spent on a version without security updates. Code is written almost identically in .NET 10, so .NET 8 learning material remains usable.

**Application-level locking (`SELECT … FOR UPDATE` or in-memory locks).** Rejected. Hard to get right and must be repeated on every new code path. The `EXCLUDE` constraint is defined once and cannot be bypassed.

**MySQL / SQL Server.** Without range types and exclusion constraints, the conflict guarantee would be left to application code.

**MediatR, AutoMapper, FluentAssertions.** Not used. All three moved to commercial licensing in 2025 and do not meet a real need in this project. Assertions use xUnit `Assert` or Shouldly.

**MUI (Material UI).** Considered, not chosen. It is stronger on mobile and more flexible to customise, but its date-range picker (`DateRangePicker`) is in the paid Pro package, it has no ready-made calendar component, and form validation is not built in. Since the target platform is the desktop web, Ant Design's ready-made components mean less code and fewer extra dependencies.

**TypeScript.** Considered, not chosen. Generating types from `openapi.yaml` would bind the contract and frontend code at build time, but it adds learning load for part of the team, so JavaScript was preferred. The risk of this decision is addressed below.

## Consequences

Positive:

- The no-double-booking guarantee rests on a single database constraint and can be shown as concrete evidence in the jury defense.
- One backend language and one deployment unit; docker compose stays at four services.
- Ant Design covers forms, tables, date ranges and calendars with one library, keeping frontend dependencies low.
- If the backend is late, the frontend can be built against the contract using the Prism mock.

Negative and mitigations:

- Learning curve for team members new to .NET. Mitigation: a module template and a short pair-programming session at the start of Sprint 2.
- In JavaScript, field names that do not match the contract (e.g. `topicNote` instead of `topic`) are not caught at build time, only at run time. Mitigation: ESLint, the single API layer (`src/api/client.js`) and the Prism mock server during development (it rejects requests that do not match the contract).
- Because a PostgreSQL-specific feature is used, integration tests cannot run on SQLite or an in-memory database. Mitigation: Testcontainers; the CI runner already has Docker.
- A modular monolith needs discipline; boundary violations are easy to introduce. Mitigation: ArchUnitNET tests and architectural checks in pull-request reviews.

## Open points

- **Unit-test project name:** `Bookademic.Tests` or `Bookademic.Booking.UnitTests`; to be decided with Mirac and recorded in the test plan.
- **Frontend tests:** If the 50% coverage requirement applies to the whole repository, Vitest and React Testing Library are added to the stack; to be decided with Mirac and recorded in the test plan.

## Follow-up

- [ ] Pull-request review: reviewer Sıla; Mehmet and Mirac add comments. When approved, status changes from "Proposed" to "Accepted".
- [ ] Mehmet: build the EN-03 compose skeleton on this stack (`db`, `api`, `web`, `mailpit`; `10.0` images)
- [ ] Mehmet: enforce the coverage threshold in EN-04 with `coverlet.msbuild` or ReportGenerator
- [ ] Mirac: use the xUnit, coverlet and Testcontainers decisions in the test plan
- [ ] Inform Emir: frontend stack and rules (including Figma)
- [ ] Check the licenses of all direct and transitive dependencies and record any that are incompatible with MIT as risks
