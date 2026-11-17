---
id: computing-software.it-support-helpdesk.servicenow.call-and-ticket-quality-monitoring
name: call-and-ticket-quality-monitoring
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, call-quality-monitoring, qa-scorecard, coaching, calibration, service-desk, agent-performance]
level: practitioner
status: draft
description: "Run quality monitoring for a service desk: QA scorecard for calls, chats and tickets, sampling, calibration sessions, coaching loops, and recording it in the ITSM tool."
sources:
  - "https://www.thinkhdi.com/library/supportworld/2018/building-quality-monitoring-program"
  - "https://www.icmi.com/resources/2018/quality-monitoring-form-best-practices"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/administer/survey-administration/concept/c_SurveyManagement.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# call-and-ticket-quality-monitoring

Quality monitoring checks *how* agents work, which metrics like AHT and FCR can't. Its
purpose is coaching, not policing.

## Scorecard (one form for calls/chats, one for tickets)
Weight items; mark critical items as auto-fail.
| Area | Example items | Weight |
|---|---|---|
| Opening | Greeting, name, caller verified per policy (**critical**) | 10 |
| Diagnosis | Open then closed questions, checked KB, confirmed the actual problem | 25 |
| Resolution | Correct fix or correct escalation with full info; no unnecessary steps | 25 |
| Communication | Plain language, set expectations, hold etiquette | 15 |
| Documentation | Category/CI correct, notes reproducible, resolution notes, KB linked | 20 |
| Close | Confirmed fixed, next steps, offered further help | 5 |
Security failures (no identity check before reset, password in ticket) = 0 for the contact.

## Sampling
- 4-8 contacts per agent per month, random across channels and times; more for new
  agents (first 90 days) and for agents under improvement plans.
- Include escalated and reopened tickets deliberately in a separate sample; they show
  process gaps.

## Calibration
Monthly, evaluators (team leads, QA analyst) score the same 3 contacts independently,
then compare. Aim for scores within 5 points; agree on interpretation and update the
form guide. Without calibration, agents rightly perceive scores as arbitrary.

## Coaching loop
1. Share the evaluation within a week, with the recording/ticket.
2. Agent self-scores first; discuss differences.
3. One or two improvement goals, not ten. Follow up next month.
4. Recognise good contacts publicly (with consent).

## In ServiceNow
- Build the scorecard as an assessment/survey (Survey Management or Assessment) with the
  ticket or interaction as the related record; evaluator takes it, results report per
  agent.
- Or a custom QA table referencing `task` with score fields; report trends per agent and
  per item (the item that fails across the team is a training topic).

## Gotchas
- Scoring only easy calls (selection bias) or only complaint calls.
- Using QA scores for pay before calibration is solid creates disputes.
- Recordings need consent/notification under local law; check with legal.

## Verify
Every agent has monthly evaluations, calibration variance is within target, and
team-wide weak items get training with scores improving the next quarter.
