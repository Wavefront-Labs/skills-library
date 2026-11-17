---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.production-meeting-agenda-and-format
name: production-meeting-agenda-and-format
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [production-meeting-agenda, production-meeting-format, communication-and-collaboration, weekly-ops-review, sre-engagement]
level: practitioner
status: docs-checked
description: "Run the weekly SRE production meeting: the SRE Book agenda (upcoming changes, metrics, outages, paging events, non-paging events, prior action items), chair and attendance."
sources: ["https://sre.google/sre-book/communication-and-collaboration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Production meeting agenda and format

SRE Book "Communication and Collaboration in SRE": a production meeting is where an SRE team articulates to itself and
its invitees the state of the services in its charge, to raise awareness and improve operation. It is service-oriented,
not a status update from individuals. The goal is that everyone leaves with the same idea of what is going on, and
that operational performance is related to design, configuration or implementation with recommendations to fix problems.

## Cadence and chair
- Usually weekly, lasting somewhere between 30 and 60 minutes. Much shorter and you may be cutting things short; much
  longer and you are mired in detail or should shard the team or service set.
- Have a chair. Many teams rotate it so everyone has a stake, and it teaches chairing skills useful in incidents.
- With two SRE teams on video and one much larger, place the chair on the smaller side by default.

## Default agenda
The Book says it is not appropriate to be prescriptive; this is a default.
1. **Upcoming production changes**: track start time, duration and expected effect; near-term visibility.
2. **Metrics**: the core service metrics (see Service Level Objectives); latency and CPU over time, and sometimes
   resource usage and efficiency.
3. **Outages**: problems of about postmortem size, as an opportunity for learning.
4. **Paging events**: the tactical view. Ask whether the alert should have paged in the way it did, and whether it
   should have paged at all; remove unactionable pages.
5. **Nonpaging events**: something that should have paged but did not (fix the monitoring); something not pageable that
   needs attention (including reactive operational work); something not pageable that needs no attention (remove the
   alert).
6. **Prior action items**: assign owners and track progress; the Book suggests an explicit catchall agenda item.

## Attendance
- Compulsory for the SRE team in question, especially when spread across countries or time zones.
- Major stakeholders and partner product development teams should attend. If you cannot invite them, fix that
  relationship; options for crowded cases include one representative, a subset, or feedback sent in advance.
- Use a collaborative document with a well-known address, pre-populate the agenda with bottom-up items and prepare it
  in parallel.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Communication and Collaboration in SRE" (Production Meetings:
purpose, cadence, chair, agenda, attendance, collaborative doc). Removed: the scribe role, the doc template with example
figures, the prefilled paging-tool export advice, and the verify list; the Book does not state them.
Method: documentation only; no commands were run.
