---
id: computing-software.it-support-helpdesk.servicenow.problem-prioritisation-and-review-board
name: problem-prioritisation-and-review-board
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, problem-prioritization, problem-review-board, problem-management, itil-4, backlog]
level: practitioner
status: draft
description: "Prioritise problem records by business impact and run a regular problem review board that keeps investigations moving, assigns owners and closes stale problems."
sources:
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/problem-management/concept/c_ProblemManagement.html"
  - "https://www.atlassian.com/itsm/problem-management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# problem-prioritisation-and-review-board

## Prioritising problems
Problem priority is about ongoing and future impact, not how loud the last incident was.
Score each problem on:
| Factor | Low | High |
|---|---|---|
| Incident frequency | Rare, single user | Daily, many users |
| Impact per occurrence | Minor annoyance | Business process stops |
| Workaround | Easy, documented | None, or painful |
| Risk of recurrence getting worse | Stable | Growing (capacity, ageing hardware) |
| Cost of the incidents | Few minutes | Hours of desk + user time |
Simple model: priority from impact x urgency, where urgency rises when there's no
workaround. Record the reasoning in the problem's description so it can be challenged.
Quantify: "34 incidents in 60 days, ~45 min each, 20 users" gets resources; "users unhappy"
doesn't.

## The problem review board
- Cadence: weekly (large orgs) or fortnightly. 30-45 minutes.
- Attendees: problem manager (chair), service desk lead, resolver group leads, change
  manager as needed.
- Agenda:
  1. New problems: accept, merge with existing, or reject (with reason); set priority
     and owner.
  2. Top-priority open problems: progress since last time, blocker, next step, date.
  3. Problems waiting on change or vendor: confirm the dependency is real.
  4. Proposed closures: fix implemented and verified (no recurrences for agreed period),
     or accepted risk with known error documented.
  5. Trend candidates from the desk (repeat incidents not yet linked).
- Output: actions with owners and dates in the problem records, not just meeting notes.

## Keeping it honest
- Report ageing open problems and problems with no update in 30 days.
- Allow "accept and close" for problems not worth fixing, with the known error kept.

## Verify
Every open problem has an owner, a priority with reasoning, and an update within the last
review cycle; closures have a verification note.
