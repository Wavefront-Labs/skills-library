---
id: creative-arts.design-for-form-and-experience.ux-design.measuring-task-success-and-time-on-task
name: measuring-task-success-and-time-on-task
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [task-success-rate, time-on-task, task-completion, error-rate, ux-metrics, usability-metrics, quantitative-usability]
level: practitioner
status: draft
description: "Measure task success and time on task in usability studies: define success, code outcomes, handle skewed times with geometric means, and report intervals for small samples."
sources:
  - "Tullis and Albert, Measuring the User Experience, 3rd ed. (Morgan Kaufmann, 2022), performance metrics chapters"
  - "Sauro and Lewis, Quantifying the User Experience, 2nd ed. (2016)"
  - "MeasuringU - Confidence Intervals for Completion Rates, adjusted-Wald (measuringu.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Task success and time on task

**Goal:** produce defensible performance numbers from a usability test.

## Define before you run
- Per task: a **start state**, an unambiguous **success criterion** ("order confirmation page reached with correct item"), and a **give-up or time limit**.
- Code each attempt: success without help, success with assistance, failure, abandoned. Binary success (1/0) is easiest to analyse; keep partial codes if you need severity.

## Completion rate
- Rate = successes / attempts. With small n use the **adjusted-Wald** interval: add z squared / 2 successes and z squared failures (z = 1.96, so about 2 and 2) before computing p and the interval. Example: 9 of 10 succeed gives about 90 percent with a 95 percent interval of roughly 60-98 percent.
- The published average task completion is about 78 percent (Sauro); use it only as rough context.

## Time on task
- Time only successful attempts (failed times distort). Start when the participant finishes reading the task; stop at success.
- Task times are right-skewed: report the **geometric mean** (exp of the mean of logs) or the median, not the arithmetic mean; log-transform before t-intervals.
- Unmoderated tools record time automatically; moderated sessions need a clear start/stop convention. Think-aloud inflates time, so do not compare think-aloud times with silent ones.

## Also capture
Errors (count of wrong paths), first-click correctness, and the SEQ rating (`creative-arts.design-for-form-and-experience.ux-design.measuring-usability-with-sus-and-seq`).

## Gotchas
- n of 5 supports finding problems, not estimating rates; for rates aim for 20+ (intervals are wide otherwise).
- Compare designs with a paired test when the same people did both.

## Verify
- [ ] Success criteria written per task before testing.
- [ ] Geometric mean or median for time; interval for completion.
- [ ] n and method reported with every number.
