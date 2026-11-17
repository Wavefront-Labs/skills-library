---
id: computing-software.it-support-helpdesk.servicenow.service-review-meetings-and-monthly-reports
name: service-review-meetings-and-monthly-reports
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-review-meeting, monthly-service-report, balanced-scorecard, service-level-management, customer-review]
level: practitioner
status: draft
description: "Run service review meetings with customers and produce the monthly service report and balanced scorecard: contents, narrative, actions and follow-through."
sources:
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
  - "https://www.thinkhdi.com/library/supportworld/2019/metrics-that-matter"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/c_ServiceLevelManagement.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# service-review-meetings-and-monthly-reports

## Monthly service report: structure
1. **Headline** (3 lines): overall status (green/amber/red), the biggest event, the main
   action.
2. **Scorecard** across four perspectives (balanced scorecard):
   | Perspective | Example measures |
   |---|---|
   | Customer | CSAT, complaints, VIP escalations |
   | Operational | SLA attainment (response, resolution), backlog age, FCR |
   | Financial | Cost per ticket, contact volume per user |
   | Learning / improvement | Shift-left ratio, KB reuse, staff training |
   Show target, this month, last 3 months trend.
3. **Major incidents and outages**: dates, duration, impact, problem status.
4. **Changes**: count, success rate, failed changes and their impact.
5. **Improvement actions**: status of last month's actions, new ones, owners, dates.
6. **Upcoming**: planned maintenance, projects, risks.

## Writing it
- Lead with what changed and why, not a wall of charts. Each chart gets one sentence:
  "Resolution SLA fell to 82% because of the 3-day VPN outage; excluding it 91%."
- Same metrics, same definitions every month; a changed definition gets a footnote.
- Automate data pulls (saved reports, Performance Analytics) so preparation time goes on
  analysis.

## Service review meeting
- Attendees: service owner, customer representative(s), service desk lead, key resolver
  group leads as needed. Monthly or quarterly depending on contract.
- Send the report 2 working days before; meeting time is for questions and decisions.
- Agenda: actions from last time, scorecard exceptions, major incidents, customer
  feedback, upcoming changes, agree new actions.
- Minute actions with an owner and date; publish within 24 hours.
- Use it to renegotiate targets that no longer fit, with data, rather than quietly
  missing them.

## Verify
Actions from the previous review are each closed or carried forward with a reason, and
the customer can state the top three issues from the report.
