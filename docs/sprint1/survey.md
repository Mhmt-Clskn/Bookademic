# Bookademic – Student Survey (Sprint 1)

**Target:** 30+ responses · **Results:** analysed and reported in the Sprint 2 SRS
**Owner:** Melih · **Tool:** Google Forms (anonymous, email addresses not collected)

> **Language note:** The project is run in English, so this file is the English reference version of the survey. Because the respondents are students in our department, **the form itself will be distributed in Turkish** (Sprint 2). The Turkish form will contain the same questions and options in the same order.

## Form introduction

Hello! We are developing a course project, **Bookademic**, that makes it easier for students working on course or graduation projects to book office hours and laboratory equipment in our department. The survey takes about 3 minutes, is anonymous and does not collect personal data. Your answers will be used only for the requirements analysis of the course project.

## Questions

**1. What year are you in?** *(single choice)*
1st year · 2nd year · 3rd year · 4th year · Graduate

**2. Are you working on a course or graduation project this semester?** *(single choice)*
Yes, a course project · Yes, a graduation project · Both · No

**3. How often do you attend a faculty member's office hours?** *(single choice)*
Never · 1–2 times per semester · Once a month · More than once a month

**4. What are the main reasons you do not attend office hours, or find it difficult to?** *(multiple choice)*
- I don't know when the instructor is available
- When I went, the instructor was not in the office / office hours were cancelled
- I had to wait in a queue
- There is no easy way to book an appointment
- I forgot the appointment
- I don't prepare what to ask in advance
- Something else came up
- Other: ____

**5. Would it make the meeting more productive if the instructor knew the topic in advance?** *(1–5 scale: Strongly disagree … Strongly agree)*

**6. Did you need to use a lab device (oscilloscope, FPGA board, etc.) or a lab room for your project?** *(single choice)*
Yes, often · Yes, a few times · No, but I needed to · No, I didn't need to
*(If Q6 is "No, I didn't need to", skip to Q10.)*

**7. What problems did you experience when using a lab device/room?** *(multiple choice)*
- We clashed with another team at the same time (double booking)
- I couldn't find out whether the device was available
- I found out only afterwards that I needed training to use the device
- I saw devices being used without training
- I didn't know whom to ask for device training
- I had problems checking out / returning the device
- I had no problems
- Other: ____

**8. Did you need approval (email/signature) from your instructor for a lab device? How did you get it and how long did it take?** *(single choice)*
Not needed · By email, same day · By email, took several days · By signature · Couldn't get it / gave up

**9. When you get stuck in the lab (device not working, don't know how to use it), how easy is it to reach the assistant / research assistant?** *(1–5 scale: Very difficult … Very easy)*

**10. How useful would it be for you to book appointments with instructors, get lab approval, complete device training and reserve devices in a single web application?** *(1–5 scale: Not useful at all … Very useful)*

**Optional, open-ended:** What feature would you most like to see in this application? ____

## Analysis plan (for the Sprint 2 SRS)

| Output | Source question |
|---|---|
| Share of students who never attend office hours | Q3 |
| Most frequent reasons for not attending (ranked) | Q4 |
| Value of knowing the topic in advance (mean) | Q5 |
| Shares of lab conflicts / untrained use / lack of information | Q7 |
| Slowness of the approval process | Q8 |
| Ease of reaching the assistant (mean) | Q9 |
| Need for the solution (mean, share of 4–5) | Q10 |

**Reporting schedule:** Results are analysed with this plan and reported in the Sprint 2 SRS; proposal.md 1.2 will then be updated with the findings.

**Note:** The results come from a small convenience sample and cannot be generalized. In the Sprint 2 SRS, present them as directional evidence, together with the published studies (UMD, Teaching Professor).
