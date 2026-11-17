---
id: computing-software.it-support-helpdesk.servicenow.service-desk-staffing-with-erlang-c
name: service-desk-staffing-with-erlang-c
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-desk, tiered-support, erlang-c, workforce-management, staffing-forecast, service-level-target, agent-utilization]
level: practitioner
status: draft
description: "Forecast contacts and staff a service desk with Erlang C: interval volumes, average handle time, service level targets like 80/30, shrinkage, and checking against real queues."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.callcentrehelper.com/erlang-c-formula-example-121281.htm"
  - "https://en.wikipedia.org/wiki/Erlang_(unit)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service-desk-staffing-with-erlang-c
Goal: enough agents logged in each half hour to answer calls and chats
within target, without overstaffing quiet periods.

## Inputs
- **Volume per interval** (30 min) by weekday, from telephony/chat history;
  at least 8-12 weeks, excluding outage spikes (handle those separately).
- **AHT** (average handle time) = talk + hold + after-call work.
- **Target service level**, e.g. 80% answered in 30 s (80/30).
- **Shrinkage**: breaks, training, meetings, leave, sickness; typically
  30-35%.

## Erlang C in practice
Traffic intensity A (Erlangs) = calls per interval × AHT ÷ interval
length. Example: 60 calls in 30 min, AHT 6 min → A = 60 × 6 / 30 = 12.
Erlang C gives the probability a caller waits for N agents; increase N
until the service level target is met. For A = 12 and 80/30 you need
16 agents (85% in 30 s; 15 agents only reach ~75%), occupancy ~75%.
Then divide by (1 − shrinkage): 16 / 0.67 ≈ 24 scheduled.
Use an Erlang calculator or spreadsheet add-in; do not hand-compute.

## Chat and email
- Chat: concurrency (2-3 chats per agent) reduces effective AHT, but
  measure actual handle time per chat; Erlang C is approximate.
- Email/portal tickets: backlog model (work in hours ÷ productive hours),
  scheduled into quiet phone periods.

## Limits of Erlang C
- Assumes callers never abandon (overstates need slightly); Erlang A
  models abandonment.
- Assumes steady arrivals within the interval; outages break it.
- Occupancy above ~85-90% for long periods burns agents out.

## Check against reality
Compare forecast vs actual volume each week (forecast accuracy within
±10% per interval is good) and adjust. Post-outage, plan a surge roster.

## Verify
A staffing sheet per interval exists from volume, AHT, target and
shrinkage, and actual service level stays near target on normal days.
