# 8. OpenAPI – backlog traceability

This table is generated from the `x-story` fields in `docs/api/openapi.yaml`. When the contract changes, the table is regenerated; it is not edited by hand.

Contract version: 0.2.2 · 35 operations · 21 stories mapped to endpoints.

| Story | Title | Priority | Owner | Operations (response codes) |
|---|---|---|---|---|
| US-01 | Register with school e-mail | Must | Mehmet | `POST /auth/register` (registerStudent; 201, 400, 409) |
| US-02 | Log in and role-based access | Must | Mehmet | `POST /auth/login` (login; 200, 400, 401)<br>`GET /users/me` (getCurrentUser; 200, 401) |
| US-03 | Assign roles to staff | Should | Mehmet | `PUT /admin/users/{userId}/role` (assignUserRole; 200, 400, 401, 403, 404) |
| US-04 | In-app notifications | Must | Mehmet | `GET /notifications` (listMyNotifications; 200, 401) |
| US-05 | Usage report | Should | Sıla | `GET /reports/usage` (getUsageReport; 200, 400, 401, 403) |
| US-06 | Reserve a lab device | Must | Mürsel | `POST /reservations` (createReservation; 201, 400, 401, 403, 404, 409)<br>`GET /reservations/{reservationId}` (getReservation; 200, 401, 403, 404) |
| US-07 | Unit tests for conflict engine | Must | Mirac | — (no endpoint, see below) |
| US-08 | Approve or reject lab requests | Must | Mürsel | `GET /reservations` (listReservations; 200, 400, 401)<br>`POST /reservations/{reservationId}/approve` (approveReservation; 200, 401, 403, 404, 409)<br>`POST /reservations/{reservationId}/reject` (rejectReservation; 200, 400, 401, 403, 404, 409)<br>`GET /reservations/{reservationId}/history` (getReservationHistory; 200, 401, 403, 404) |
| US-09 | Cancel reservation or appointment | Must | Sıla | `GET /reservations` (listReservations; 200, 400, 401)<br>`POST /reservations/{reservationId}/cancel` (cancelReservation; 200, 401, 403, 404, 409) |
| US-10 | Unified calendar | Should | Emir | `GET /me/calendar` (getMyCalendar; 200, 400, 401) |
| US-11 | Add and edit devices and rooms | Must | Melih | `POST /resources` (createResource; 201, 400, 401, 403, 409)<br>`PUT /resources/{resourceId}` (updateResource; 200, 400, 401, 403, 404, 409) |
| US-12 | Filter the catalogue | Must | Sıla | `GET /resources` (listResources; 200, 400, 401)<br>`GET /resources/{resourceId}` (getResource; 200, 401, 404) |
| US-13 | Lab access approval from office hour | Must | Melih | `POST /lab-approvals` (grantLabApproval; 201, 400, 401, 403, 404)<br>`GET /lab-approvals` (listLabApprovals; 200, 401, 403) |
| US-14 | Device training and authorisation | Must | Melih | `POST /training-authorizations` (grantTrainingAuthorization; 201, 400, 401, 403, 404, 409)<br>`GET /training-authorizations` (listTrainingAuthorizations; 200, 401, 403)<br>`GET /appointments/incoming` (listIncomingAppointments; 200, 400, 401, 403) |
| US-15 | Handover code and return | Should | Mirac | `POST /reservations/{reservationId}/handover-code` (issueHandoverCode; 201, 401, 403, 404, 409)<br>`POST /reservations/{reservationId}/check-in` (checkInReservation; 200, 400, 401, 403, 404, 409)<br>`POST /reservations/{reservationId}/return` (returnReservation; 200, 401, 403, 404, 409) |
| US-16 | Put a device into maintenance | Should | Sıla | `POST /resources/{resourceId}/maintenance` (startMaintenance; 200, 400, 401, 403, 404, 409)<br>`DELETE /resources/{resourceId}/maintenance` (endMaintenance; 200, 401, 403, 404) |
| US-17 | Define office, support and training hours | Must | Emir | `POST /office-hours` (createOfficeHourSchedule; 201, 400, 401, 403, 409)<br>`GET /office-hours` (listOfficeHourSchedules; 200, 401) |
| US-18 | Book an appointment with a topic | Must | Emir | `GET /office-hours` (listOfficeHourSchedules; 200, 401)<br>`GET /office-hours/{scheduleId}/slots` (listSlots; 200, 400, 401, 404)<br>`POST /appointments` (bookAppointment; 201, 400, 401, 403, 404, 409)<br>`GET /appointments/my` (listMyAppointments; 200, 400, 401, 403) |
| US-19 | View the day's appointments | Must | Emir | `GET /appointments/incoming` (listIncomingAppointments; 200, 400, 401, 403) |
| US-20 | Secretary cancels an office-hour day | Must | Mirac | `POST /office-hours/{scheduleId}/cancellations` (cancelOfficeHourDay; 200, 400, 401, 403, 404) |
| US-21 | Redirect to a support hour | Should | Emir | `POST /appointments/{appointmentId}/redirect` (redirectAppointment; 201, 400, 401, 403, 404, 409) |
| US-22 | Help appointment from a lab reservation | Should | Emir | `POST /appointments` (bookAppointment; 201, 400, 401, 403, 404, 409) |

**Work items without an endpoint:**

- **US-07** is a test story and has no API of its own; it is verified by unit tests and Testcontainers integration tests (see docs/test-plan.md) behind `createReservation` and `approveReservation`.
- **US-23 – E-mail notifications** (Should, owner Sıla) reuse the same events as US-04 and are delivered through SMTP (Mailpit in development). They add no endpoint.
- **EN-01, EN-03 and EN-04** are infrastructure work. **EN-02** is this contract itself.

**Reverse check:** every operation in the contract has at least one `x-story` value; there is no endpoint without a story.
