# Bookademic – Initial Product Backlog (Sprint 1)

The backlog contains 10 epics, 23 user stories (84 points) and 4 technical enablers (11 points); 95 points in total. Priority is given with MoSCoW, estimates with Fibonacci story points. **MVP = 15 Must stories (60 points) + the enablers.**

The backbone of the MVP is the demo journey: US-17 (define hours) → US-18 (appointment) → US-13 (lab approval) → US-14 (training and authorization) → US-06 (reservation) → US-08 (research assistant approval). US-20 (secretary cancellation) shows the third actor alongside this journey; US-04 (in-app notifications) delivers the notifications that US-14 and US-20 require.

**Notification decision (3 Nov 2026, Melih + Mürsel):** US-04 is the **in-app notification** story (Must), mapped to `GET /notifications` in the OpenAPI contract. Email notification is a separate **Should** story, US-23.

## Epics

| Epic | Name | Module | Priority | Stories | Points |
|---|---|---|---|---|---|
| E1 | Identity and authorization | M1 | Must | US-01, US-02, US-03 | 8 |
| E2 | Notifications and reporting | M1 | Must | US-04, US-05, US-23 | 9 |
| E3 | Reservation core | M2 | Must | US-06, US-07, US-09, US-10 | 18 |
| E4 | Lab approval flow | M2 | Must | US-08 | 5 |
| E5 | Resource catalog | M3 | Must | US-11, US-12 | 6 |
| E6 | Lab access and device training | M3 | Must | US-13, US-14 | 10 |
| E8 | Office hours and appointments | M4 | Must | US-17, US-18, US-19, US-20 | 15 |
| E10 | Infrastructure (enablers) | — | Must | EN-01 … EN-04 | 11 |
| E7 | Check-out/return and maintenance | M3 | Should | US-15, US-16 | 8 |
| E9 | Redirection and help | M4 | Should | US-21, US-22 | 5 |

US-03 in E1, US-05 and US-23 in E2, and US-10 in E3 are Should; an epic's priority follows its main stories.

## User stories

| ID | Epic | User story | Acceptance criteria | Points | Priority | Dependencies | Owner |
|---|---|---|---|---|---|---|---|
| US-01 | E1 | As a student, I want to register with my school email. | Only emails with the school domain are accepted, otherwise 400; registering the same email a second time returns 409. | 3 | Must | — | Mehmet |
| US-02 | E1 | As a user, I want to log in and access the screens for my role. | Valid credentials → 200 + JWT; invalid credentials → 401; no token → 401; unauthorized role → 403. | 3 | Must | US-01 | Mehmet |
| US-03 | E1 | As an admin, I want to assign roles to staff. | ADMIN only; undefined role → 400; every change is written to the audit log. | 2 | Should | US-02 | Mehmet |
| US-04 | E2 | As a user, I want to receive an in-app notification when the status of my booking changes. | A notification is created for the affected user on approval, rejection, cancellation, redirection and training authorization; GET /notifications returns only the caller's own notifications, newest first; a failure to create a notification is logged and does not roll back the operation. | 3 | Must | US-02 | Mehmet |
| US-05 | E2 | As a department secretary, I want to see the device and office-hour usage report. | Date-range filter; occupancy rate and number of cancellations; SECRETARY/ADMIN only. | 3 | Should | US-06, US-18 | Sıla |
| US-06 | E3 | As a student, I want to reserve a time slot for a lab device. | End before start → 400; overlaps a pending, approved or checked-in booking → 409; no valid lab approval → 403 LAB_APPROVAL_REQUIRED; no training authorization → 403 TRAINING_REQUIRED; on success 201 + PENDING. | 8 | Must | US-02, US-11 | Mürsel |
| US-07 | E3 | As a QA engineer, I want to verify the conflict engine and access rules with unit tests. | Overlapping, nested and back-to-back ranges (10:00–11:00 and 11:00–12:00 do not conflict); all combinations of approval/authorization present or missing; M2 coverage at least 50%. | 5 | Must | US-06 | Mirac |
| US-08 | E4 | As a research assistant, I want to approve or reject pending lab requests. | RESEARCH_ASSISTANT/ADMIN only; rejection reason required; only PENDING requests can be changed, otherwise 409; every transition is written to the status history. | 5 | Must | US-06 | Mürsel |
| US-09 | E3 | As a student, I want to cancel my reservation or appointment. | Can be cancelled before the start time, otherwise 409; another user's booking → 403; the status becomes CANCELLED and the slot is freed immediately. | 2 | Must | US-06 | Sıla |
| US-10 | E3 | As a student, I want to see this week's appointments, trainings and reservations in a single calendar. | Chronological list with a type label; only the user's own bookings. | 3 | Should | US-06, US-18 | Emir |
| US-11 | E5 | As a research assistant, I want to add and edit devices and rooms. | Name, type, category and location required; serial number unique, duplicate → 409; RESEARCH_ASSISTANT/ADMIN only. | 3 | Must | US-02 | Melih |
| US-12 | E5 | As a student, I want to filter the catalog by type, category and availability. | Filters work together; no results → 200 + empty list; with a 500-record test dataset, p95 response time < 200 ms. | 3 | Must | US-11 | Sıla |
| US-13 | E6 | As an instructor, I want to grant a student lab access approval from an office-hour meeting. | INSTRUCTOR only; device category and end date required; the approval is linked to the related appointment; the research assistant sees the approval in the lab panel; an expired approval is invalid. | 5 | Must | US-18, US-11 | Melih |
| US-14 | E6 | As a research assistant, I want to record a completed device training and authorize the student. | Authorization is created only when an appointment of type TRAINING is completed; authorization is per category; a second authorization for the same category → 409; the instructor who granted the approval receives an in-app notification (US-04). | 5 | Must | US-17, US-18, US-04 | Melih |
| US-15 | E7 | As a research assistant, I want to hand over a device with a check-out code and receive its return. | A 6-digit single-use code is generated for an approved reservation; when verified → CHECKED_IN; a second use is rejected; on return → COMPLETED. | 5 | Should | US-08 | Mirac |
| US-16 | E7 | As a research assistant, I want to put a device under maintenance. | A device under maintenance cannot be reserved (409); future reservations are cancelled and their owners are notified (US-04). | 3 | Should | US-11, US-04 | Sıla |
| US-17 | E8 | As an instructor or research assistant, I want to define weekly office hours, support hours or training hours. | Type (OFFICE_HOUR, SUPPORT, TRAINING), day, time range and slot length are entered; category required for TRAINING; an instructor may define only OFFICE_HOUR, a research assistant only SUPPORT and TRAINING, otherwise 403; the system generates the slots; the same person's hours cannot overlap (409). | 5 | Must | US-02 | Emir |
| US-18 | E8 | As a student, I want to book an appointment by writing my topic. | Topic note required (10–500 characters); full slot → 409; at most one appointment per day with the same staff member (instructor or research assistant), otherwise 409; the appointment is stored as a reservation in M2. | 5 | Must | US-17, US-06 | Emir |
| US-19 | E8 | As an instructor, I want to see today's appointments with their topics. | Listed in time order; cancelled appointments shown separately; only appointments in the instructor's own hours. | 2 | Must | US-18 | Emir |
| US-20 | E8 | As a department secretary, I want to cancel an office hour for a specific day. | SECRETARY/ADMIN or the owner of the hours only; reason required; all appointments of that day become CANCELLED; affected students receive an in-app notification (US-04). | 3 | Must | US-18, US-04 | Mirac |
| US-21 | E9 | As an instructor, I want to redirect an appointment to a research assistant's support hours. | No free slot in the target support hours → 409; the old appointment becomes CANCELLED and a new one is created; the student is notified (US-04). | 3 | Should | US-17, US-18, US-04 | Emir |
| US-22 | E9 | As a student, I want to open a help appointment in the assistant's support hours from my lab reservation. | Reservation details are attached to the appointment automatically; only for the student's own APPROVED or CHECKED_IN reservation. | 2 | Should | US-08, US-18 | Emir |
| US-23 | E2 | As a user, I want to receive an email when the status of my booking changes. | Sent for the same events as US-04 through the SMTP service (Mailpit in development); a send failure is logged and does not roll back the operation. | 3 | Should | US-04, EN-03 | Sıla |

## Technical enablers

| ID | Task | Acceptance criterion | Points | Sprint | Owner |
|---|---|---|---|---|---|
| EN-01 | GitHub organization, repository, Git-Flow, branch protection, templates | main and develop protected; first PR merged after review | 2 | 1 | Mehmet |
| EN-02 | OpenAPI contract v0.2 | Opens without errors in Swagger Editor; every operation is linked to a story via `x-story` (Section 8) | 3 | 1 | Mürsel |
| EN-03 | docker-compose skeleton (db + api + web + mailpit) | `docker compose up` starts the db, api, web and mailpit services (10.0 images, as in ADR-0001) | 3 | 1–2 | Mehmet |
| EN-04 | GitHub Actions CI (build + test + coverage) | Runs on every PR; fails if coverage is below 50% | 3 | 3 | Mehmet |

## Load per person (story + enabler points)

| Person | Points |
|---|---|
| Emir | 20 |
| Mehmet | 19 |
| Mürsel | 16 |
| Sıla | 14 |
| Mirac | 13 |
| Melih | 13 |
| **Total** | **95** |

## Summary

| | Stories | Points |
|---|---|---|
| Must | 15 | 60 |
| Should | 8 | 24 |
| Enablers | 4 | 11 |
| **Total** | **27** | **95** |
