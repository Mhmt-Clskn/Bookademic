# Sprint 1 Test Plan and Quality Assurance Strategy

## 1. Overview and Quality Objectives
This test plan defines the verification and validation strategy for the Bookademic modular monolith core (Sprint 1). The target release scope focuses on scheduling consistency, appointment lifecycle integrity, and catalog search precision across M1 (Identity/Notifications), M2 (Booking Core), M3 (Laboratory Resources), and M4 (Office Hours).

Quality objectives:
- 0 critical or blocking defects in core interval reservation logic.
- 100% specification conformance against OpenAPI v0.2.2 contracts.
- Automated regression suite coverage on domain logic and state transitions: CI enforces ≥ 50% line coverage (course requirement, ADR-0001); team target 80% on domain logic.
- Concurrency safety validated at the database engine level (PostgreSQL EXCLUDE constraints).

---

## 2. Test Scope Matrix

| Target ID | Scope / Focus | Level | Automated / Manual | Tooling |
|---|---|---|---|---|
| US-01 / US-02 | Institutional registration (US-01), JWT authentication & role-based route guards (US-02) | Integration | Automated | xUnit, Testcontainers, WebApplicationFactory |
| US-06 | Lab device reservation: 400 end before start, 409 overlap with pending/approved/checked-in, 403 LAB_APPROVAL_REQUIRED / TRAINING_REQUIRED | Integration | Automated | xUnit, PostgreSQL Testcontainers |
| US-07 | Interval exclusion lock & state-machine lifecycle (Double-booking engine & access rules) | Architecture / Integration | Automated | PostgreSQL Testcontainers |
| US-11 / US-12 | Catalog querying, equipment availability, interval filtering | Unit / Integration | Automated | xUnit, PostgreSQL Testcontainers |
| US-14 | Device training authorization & in-app notification to the approving instructor (US-04) | Integration | Automated | xUnit, WebApplicationFactory |
| US-17 | Staff appointment slot declaration & conflict prevention | Integration / Concurrency | Automated | xUnit, Parallel Task runners |
| US-18 | Appointment booking with topic note (10-500 chars), daily limit 409 | Integration | Automated | xUnit, PostgreSQL Testcontainers |
| US-23 | Status-change e-mail via SMTP | Integration | Automated | xUnit, Mailpit container |
| Web UI | Critical user flows (Login -> Reserve -> Confirmation) | E2E | Automated | Playwright |

---

## 3. Boundary Value Analysis (BVA) & Edge Cases

### 3.1 Interval and Temporal Boundaries (US-06, US-07, US-17)
- Exact adjacent slots: Slot A `[10:00, 10:30)` and Slot B `[10:30, 11:00)` must not trigger 409 conflict.
- Partial overlap: Slot A `[10:00, 10:30)` and Slot B `[10:15, 10:45)` must trigger 409 Conflict with Problem Details RFC 9457 schema.
- Enclosing interval: Slot A `[09:00, 12:00)` attempting reservation on Slot B `[10:00, 11:00)` must fail immediately.

### 3.2 Appointment Subject Field Boundaries (US-18)
- Minimum valid length: 10 characters (Must accept with 201 Created).
- Below minimum boundary: 9 characters (Must reject with 400 Validation Error).
- Maximum valid length: 500 characters (Must accept with 201 Created).
- Above boundary limit: 501 characters (Must reject with 400 Validation Error).
- Null or whitespace-only strings: Must reject with 400 Validation Error.

### 3.3 Pagination and Filtering Boundaries (US-11 / US-12)
- Zero matches: Valid filter criteria returning zero items must return 200 OK with empty array `[]` (not 404 or null).
- Database volume baseline: Catalog search queries evaluated on a populated baseline of 500 items to maintain p95 latency < 200 ms.

---

## 4. Test Environments and Tooling Stack

- **Unit & Integration Framework:** xUnit (.NET 10)
- **Code Coverage & Thresholds:** Coverlet (CI enforces ≥ 50% line coverage (course requirement, ADR-0001); team target 80% on domain logic)
- **Database Isolation:** Testcontainers running PostgreSQL 17 to validate native range exclusion constraints (`btree_gist` / `tstzrange`)
- **Notification Stubbing:** Mailpit local SMTP test server to verify asynchronous email dispatch without external network calls
- **Static Analysis & Linting:** SonarQube quality gate enforcement on CI
- **End-to-End Testing:** Playwright (Chromium headless) against local Docker Compose environment

---

## 5. Peer Review & QA Exit Criteria

A Pull Request is certified for merge into `develop` only when:
1. Associated acceptance criteria match the scenario specifications defined above.
2. At least one designated peer review approval is recorded in GitHub.
3. Automated unit and containerized integration test suites pass with zero failures.
4. OpenAPI schemas reflect all updated request/response contracts and RFC 9457 error structures.
