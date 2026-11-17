---
id: computing-software.it-support-helpdesk.servicenow.sla-target-setting-and-attainment-reporting
name: sla-target-setting-and-attainment-reporting
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, sla-target-setting, sla-attainment-report, service-level-management, task-sla, historic-data]
level: practitioner
status: draft
description: "Set realistic SLA targets from historic ticket data, then report SLA attainment correctly with task SLA records, exclusions and breach analysis."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/service-level-management/concept/c_ServiceLevelManagement.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
  - "https://www.thinkhdi.com/library/supportworld/2019/metrics-that-matter"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sla-target-setting-and-attainment-reporting

## Setting targets from data
1. Pull 6-12 months of resolved tickets per priority (and per service if targets will
   differ), excluding duplicates and cancelled.
2. Compute business-hours durations for response and resolution with the schedule the
   SLA will use (calendar hours make targets meaningless).
3. Look at percentiles, not the mean: if P3 resolution p80 is 14 business hours and p90 is
   26, a 3-day target at 90% is achievable; a 1-day target is not without change.
4. Set target = a percentile you can meet today plus a stretch agreed with the business
   (e.g. "90% within 2 business days, improving to 1.5 next year").
5. Pilot for a month with the SLA running but not reported to customers; adjust.

## Rules worth agreeing in writing
- Which states pause (Awaiting caller, Awaiting vendor) and who may use them.
- What happens on priority change (retroactive start or restart).
- Business hours schedule and holidays per region.

## Reporting attainment
- Report on **task SLA** records (`task_sla`), not incidents: `has_breached`,
  `planned_end_time`, `business_percentage`, `stage`.
- Attainment % = met / (met + breached) for completed task SLAs in the period, grouped by
  SLA definition. Exclude `stage=cancelled`.
- Report response and resolution separately; mixing them hides problems.
- Breakdowns: by assignment group, category, channel, priority. Trend monthly.
- Add a breached-list drilldown with the reason; repeated "waiting on vendor" breaches
  point at an underpinning contract, not the desk.

## Pitfalls
- Paused SLAs abused to protect attainment: report time in pause per group.
- Reporting from incident `made_sla` alone misses multiple SLAs per ticket.
- Target changed mid-period: report old and new definitions separately.

## Verify
Attainment numbers reconcile with a manual sample of 20 task SLA records, and the agreed
targets sit near current p80-p90 performance.
