# Bookademic – Project Proposal (Sprint 1)

**Course:** SENG 321 – Software Engineering Project
**Version:** v0.1.0-sprint1 · **Owner:** Melih (Product Owner & Requirements Engineer)

Bookademic is a Project Support Platform that manages, in a single flow, the two scarce resources a project student needs: the instructor's time and the laboratory.

---

## 1. Project proposal

### 1.1 Problem statement

A student working on a course project or a graduation project depends on two scarce resources: the instructor's time and laboratory equipment. Today both are managed manually and are disconnected from each other.

**Instructor's time**

- **Waiting at the door:** There is no appointment system, so students queue outside the office; the instructor is often unavailable.
- **Unprepared meetings:** The instructor does not know in advance why the student is coming.
- **Cancellations arrive late:** When the instructor cannot come in, the news is given by a note taped to the door.
- **Low usage:** Most students never attend office hours at all (see 1.2).

**Laboratory**

- **Double booking:** Devices and rooms are allocated with a paper list; the same time slot can be given to two teams.
- **Untrained use:** Expensive devices such as oscilloscopes and FPGA boards are handed out without checking whether the student has completed the usage training.
- **Untraceable inventory:** Who has a device, who is late, and who has not returned it cannot be seen in real time.

**The gap between the two**

- To use the lab, the student gets the instructor's approval by email or signature; the lab supervisor cannot see this approval in any system.
- There is no record of who has received device training.
- A student who gets stuck in the lab looks for the assistant in the corridor; help requests are not recorded anywhere.

### 1.2 Evidence

**Secondary data (published studies):**

- In a survey of more than 600 students, 66% had never attended office hours for the relevant course and only 8% attended more than once a month (Teaching Professor). This result comes from a survey published by other researchers.
- In the University of Maryland's 2024 survey, 21% of students who signed up for office hours said they attended "never or rarely". The same report lists the reasons students miss *any* appointment or event (not specific to office hours): "something else came up" (80%), "forgot" (55%) and "double-booked" (44%) (UMD CAWG report). Reminders and conflict checks target these reasons directly.

**Primary data (Sprint 1):** A 10-question survey of students in our department (target: 30+ responses; questions in `survey.md`), plus short interviews with 2–3 faculty members and one research assistant. The survey was distributed on 3 November 2026 (form in Turkish, see `survey.md`).

**Survey results – interim (n = __ responses, as of 3 Nov 2026, __:__)**

> Final results will replace this block on 5 November 2026 at noon.

| Indicator | Source question | Interim value |
|---|---|---|
| Responses | – | __ |
| Students who never attend office hours | Q3 | __% |
| Most frequent reasons for not attending (ranked) | Q4 | __ |
| Students who experienced a lab booking conflict or wait | Q7 | __% |
| Students who witnessed untrained device use / learned about training only afterwards | Q7 | __% |
| Students who got lab approval by email/signature | Q8 | __% |
| Usefulness of a single web app (mean, 1–5; share of 4–5) | Q10 | __ / __% |

**Takeaways:** __

*Note: This is a small convenience sample and cannot be generalized; it is presented as directional evidence alongside the published studies above.*

### 1.3 Stakeholders

| Stakeholder | Need / Expectation | Influence / Interest |
|---|---|---|
| Student | Reach the instructor and devices without waiting, from one place; keep the project on track | Medium / High |
| Instructor (faculty member) | Manage office hours in an orderly way, see the topic in advance, grant lab approval easily | High / High |
| Research Assistant | Prevent untrained use, conflict-free reservations, track check-out/return, organize help requests | High / High |
| Department Secretary | Notify students quickly when an instructor cannot come in, report usage | Medium / Medium |
| Admin | User and role management, audit logs | Medium / Medium |
| Department Head | See lab and office-hour usage, plan resources | High / Medium |
| University IT | Security, authentication, KVKK (Turkish data protection law) compliance | High / Low |
| Course instructor (jury) | Consistency and traceability of sprint outputs | High / High |

### 1.4 Proposed solution

Bookademic is built on a shared reservation core that models everything as a "resource + time slot". The instructor's office hours, the assistant's support and training hours, and lab devices all use the same conflict engine and the same state machine. The two domains are connected through the student's project journey:

1. The student books an appointment in the instructor's office hours, writing the topic ("I need an oscilloscope for my project").
2. From the meeting screen, the instructor grants the student lab access approval for the relevant device category.
3. If the student will use the device for the first time, they book a slot in the research assistant's device training hours. When the training is completed, the student is authorized for that category.
4. A student with both approval and authorization reserves the device. A conflicting request is rejected with 409.
5. The research assistant approves the request, hands over the device with a check-out code and receives the return.
6. If the student gets stuck in the lab, they open an appointment in the assistant's support hours from the reservation screen.

If the instructor cannot come in that day, the department secretary cancels the office hours and the students with appointments are notified automatically. The system starts with a single command (`docker compose up`).

### 1.5 Expected outcomes

All outcomes are measurable and will be verified by tests or by the Sprint demo.

| # | Outcome | Measure |
|---|---|---|
| O1 | No double bookings in office hours or lab reservations | 100% of overlapping requests are rejected with 409 (conflict-engine unit tests, incl. edge cases) |
| O2 | No device use without approval and training | 100% of reservations without a valid lab approval or training authorization are rejected with 403; 100% of approvals and trainings are recorded |
| O3 | Prepared meetings | A student books an office-hour appointment in under 2 minutes; 100% of appointments carry a topic note (10–500 characters) visible to the instructor before the meeting |
| O4 | Timely cancellation notices | 100% of students with an appointment in a cancelled office hour receive an in-app notification within 1 minute of the cancellation |
| O5 | Extensible core | A new resource type (e.g. meeting room) can be added with zero changes to the reservation core (M2) code |

---

## 2. Feasibility, assumptions, risks and license

### 2.1 Feasibility and initial scope

- **Technical:** Standard web technologies, a REST API and a relational database (PostgreSQL) are sufficient. Conflict checking is done with a time-range overlap query; access control uses approval and authorization tables. No special hardware is required.
- **Economic:** Open-source tools and GitHub's free tier (including Actions) are used; the cost is zero.
- **Time and team:** 10 weeks, 6 people. The shared core (M2) is written once; the lab (M3) and office-hours (M4) modules are developed in parallel on top of it.
- **MVP (week 8):** All Must stories in the backlog (15 stories, 60 points) and the enablers. This scope makes **steps 1–4 and the approval part of step 5** of the project journey in 1.4, plus secretary cancellation, work end-to-end. Check-out/return codes (US-15), maintenance, redirecting to the assistant, the unified calendar, email notifications and reports remain Should.

### 2.2 Assumptions and constraints

- The system is designed for one university and one department; authentication uses the school email address (no SSO).
- Lab access approval is granted by the faculty member of the student's course or project; approval is per device category and has an end date.
- Device training is per category (e.g. "Oscilloscope"); training completed once is valid for the whole semester.
- Office-hour appointments are approved automatically if the slot is free; lab reservations are approved by a research assistant.
- Only synthetic/test data is used; there is no real student data.
- Delivery constraints: API-first (OpenAPI YAML), Git-Flow, unit test coverage of at least 50%, runs with a single Docker command, SonarQube analysis.
- **The UI and documentation are in English**, as are code, API descriptions, Issues, PRs and commit messages. Only the student survey form is distributed in Turkish (see `survey.md`).

### 2.3 Risks

| Risk | Mitigation | Owner |
|---|---|---|
| The jury sees the project as "two independent applications" | The flows connecting the two domains (lab approval, device training) are Must; the demo is built on this journey | Melih |
| The "shared core" claim has no counterpart in the code | M2 is written first; M3 and M4 do not implement their own reservation logic but call M2; checked in PR reviews | Mürsel |
| Scope creep (5 actors, two domains) | MoSCoW; only Must until the MVP; live queue and mobile app out of scope | Melih |
| No feedback from real users | Survey in Sprint 1, short interviews in Sprint 2; if not possible, persona assumptions are flagged | Melih |
| Test coverage below 50% | The conflict engine and access rules are written with tests from day one; coverage threshold in CI | Mirac |
| System does not start with a single command | docker-compose skeleton set up in Sprint 1; demo rehearsal at the end of each sprint | Mehmet |
| Unbalanced contributions | Every task has an Issue + PR; weekly contribution check | Sıla |
| OpenAPI and backlog out of sync | Every endpoint is linked to at least one story (`x-story`) | Mürsel |

### 2.4 Open-source license

**MIT License.** It is short and easy to understand, and lets other universities or students freely use and extend the project. The risk of conflict with the licenses of the common libraries we use is low. Copyleft licenses such as the GPL require derivative works to be open as well, which can make institutional adoption harder; therefore they were not chosen.
