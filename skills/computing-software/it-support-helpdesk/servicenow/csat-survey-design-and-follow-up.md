---
id: computing-software.it-support-helpdesk.servicenow.csat-survey-design-and-follow-up
name: csat-survey-design-and-follow-up
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, metrics, kpi, csat-survey, customer-satisfaction, survey-design, detractor-follow-up]
level: practitioner
status: draft
description: "Run ticket CSAT surveys that drive improvement: one-question design, send triggers, response-rate tactics, closing the loop on bad scores, and reporting by agent and category."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
  - "https://support.zendesk.com/hc/en-us/articles/4408886173338"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# csat-survey-design-and-follow-up
Goal: satisfaction data that is representative, actionable per ticket, and
leads to a call-back for every unhappy user.

## Design
- One rating question plus one optional comment: "How satisfied were you
  with the resolution of INC0012345?" 5-point scale (or good/bad in
  Zendesk). Comments are where the value is.
- Optional second question to separate the outcome from the agent
  ("Was your issue fixed?" Yes/No).
- Avoid 10-question surveys; response rate collapses.

## Sending
- Trigger on resolution (ServiceNow Assessment / Survey Designer with a
  trigger condition on `incident.state` = Resolved; Zendesk automation
  for "Solved" tickets after 24 hours).
- Survey each ticket, but throttle per user (e.g. max one survey per 7
  days) to avoid fatigue.
- Exclude auto-closed monitoring tickets and tickets the user never saw.

## Response rate
Typical 10-20%. Raise it with a one-click rating in the email, a short
subject line naming the ticket, and agents mentioning the survey only
neutrally. Low response rates bias toward extremes; report n alongside %.

## Close the loop
- Any score of 1-2 creates a follow-up task for the team lead within one
  business day (ServiceNow: survey trigger condition creating a task;
  Zendesk: trigger on bad satisfaction).
- Call the user, listen, fix or explain, and record the cause (process,
  knowledge, agent behaviour, product/tool).
- Reopen the incident if not actually fixed.

## Reporting
- CSAT % = satisfied responses (4-5) ÷ all responses.
- Cut by category, channel, assignment group and agent; read comments for
  the top themes monthly.
- Per-agent CSAT needs enough volume (30+ responses) before conclusions.

## Gotchas
- Users rate the outcome (policy said no) rather than the service; tag
  those so agents are not penalised for policy.
- Gaming: agents choosing which tickets get surveys. Automate sending.

## Verify
Response rate and CSAT reported with n, every low score has a follow-up
task, and themes lead to at least one change per quarter.
