---
id: computing-software.it-support-helpdesk.servicenow.proactive-problem-identification-from-trends
name: proactive-problem-identification-from-trends
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, problem-management, incident-trend-analysis, proactive-problem-management, top-talkers, recurring-incidents, ci-hotspots, itil-4]
level: practitioner
status: draft
description: "Find problems before they become major incidents: monthly trend analysis of incidents by CI, category and resolution, repeat callers, and turning findings into problem records."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# proactive-problem-identification-from-trends

Goal: the desk spots the recurring fault that generates 60 tickets a month
and gets it fixed, instead of resolving it 60 times (ITIL 4 problem
identification: trend analysis of incident records).

## Monthly analysis (60–90 minutes)
Pull last 30/90 days of resolved incidents (report or export):
1. **By CI / model** — top 10 CIs or hardware models by incident count
   (e.g. one dock model, one app server).
2. **By category/subcategory** and **resolution code** — "Solved
   (workaround)" clusters are unresolved problems.
3. **Repeat callers / devices** — same user or asset with 3+ incidents.
4. **Text clustering** on short descriptions (ServiceNow Predictive
   Intelligence clustering, or a simple keyword count) — finds issues
   miscategorised across buckets.
5. **Time patterns** — spikes after Patch Tuesday, Monday mornings, month
   end.
6. **Changes** — incidents within 72 h after changes to related CIs.

## From finding to problem record
Criteria for raising a problem: e.g. ≥ 10 incidents/month with the same
symptom, any recurring P2, high handle time with a workaround. Raise with:
data summary (counts, list of incidents linked), impact estimate (hours of
user downtime + agent time), suspected area. Assign a problem owner in the
resolver group.

## Present it
A short monthly "top problems" note to IT leadership: top 5 trends, cost in
hours, status of each problem. Visibility gets problems prioritised.

## Gotchas
- Poor categorisation and "Other" hide trends — fix data quality first.
- Shift-left candidates (user can self-fix) are also an output, not just
  problems.
- Don't open problems for one-offs; noise kills the practice.

## Verify
Each month produces at least one linked problem or shift-left action; the
volume of the previous month's top trend drops after the fix.
