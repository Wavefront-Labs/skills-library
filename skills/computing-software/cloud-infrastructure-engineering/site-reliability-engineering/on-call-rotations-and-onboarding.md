---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.on-call-rotations-and-onboarding
name: on-call-rotations-and-onboarding
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, on-call, on-call-rotation, on-call-schedule, on-call-handover, on-call-training, shadow-on-call, reverse-shadow, wheel-of-misfortune, disaster-role-playing, pager-load, pages-per-shift, follow-the-sun, primary-secondary, escalation, on-call-compensation, time-off-after-incidents, on-call-health, operational-load-cap, pagerduty, opsgenie, grafana-oncall, runbooks, handover-notes]
level: advanced
status: docs-checked
description: "Run a humane on-call: rotation shapes (primary/secondary, follow-the-sun), the 50% ops cap and 2-incidents-per-shift ceiling, compensation and recovery rules, handover ritual."
sources: ["https://sre.google/sre-book/being-on-call/", "https://sre.google/workbook/on-call/", "https://sre.google/sre-book/accelerating-sre-on-call/", "https://sre.google/sre-book/dealing-with-interrupts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call rotations and onboarding

**Goal:** someone competent responds to every page within minutes, nobody burns out doing
it, and a new engineer becomes a confident on-caller in weeks rather than through trial by fire.

## 1. Rotation shape
- **Team size**: the SRE Book derives a minimum of eight engineers for a single-site 24/7
  rotation (primary and secondary, week-long shifts, from its 25% on-call rule) and six per site
  for a dual-site team. Merge small teams' rotations with shared runbooks rather than running
  3-person rotations.
- **Primary + secondary**: the split of duties varies by team. The Book describes a secondary
  as fall-through for pages the primary misses, or as the owner of non-urgent production work
  while the primary handles only pages; two related teams can also be each other's secondary.
- **Follow-the-sun**: a multi-site rotation avoids night shifts (the Book cites their health
  effects) at the cost of communication and coordination overhead; each site must own the
  service during its shift and share an incident tracker. Weigh it against single-site by the
  importance of the system and its workload.
- **Shift boundaries** at a quiet, awake hour, never midnight; handoff on weekdays so the
  incoming person can ask questions.
- **Response time** target written down; the Book's typical values are 5 minutes for
  user-facing or highly time-critical services and 30 minutes for less time-sensitive ones.
  It constrains where the on-caller can be and must be compensated accordingly.

## 2. Load limits and the numbers that enforce them
- SRE rule: **≤ 50% of an engineer's time on operations** (on-call, tickets, interrupts), and
  no more than 25% of it on-call; the rest is engineering that reduces future ops. Measure
  quarterly; above the cap, put concrete load-reduction objectives in the quarterly plan.
- **≤ 2 incidents per 12-hour shift** (SRE Book). An incident consumes ~6 h end to end
  (respond, mitigate, write-up, follow-ups); more than two means no learning happens and
  fatigue causes mistakes. Too few pages and skills rot (the Book's "operational underload") — use drills.
- Track per shift: pages, out-of-hours pages, time to acknowledge, time to mitigate,
  non-actionable pages. The Book says every paging alert should be actionable, so any
  non-actionable page is an alert to review first (`...observability.alert-fatigue-reduction`).
- Operational load cap breached ⇒ escalate to management with the page data; the Book's
  remedies include quarterly objectives and temporarily embedding an experienced SRE.

## 3. Compensation and recovery
- On-call is compensated: Google offers time-off in lieu or cash capped at some proportion of
  salary, and the cap also limits how much on-call one person takes on. Write the rule; do not
  rely on goodwill.
- After a night incident: late start/day off, no meetings. After a Sev-1: the responder
  does not own the postmortem alone and gets the next shift swapped if needed.
- Cap consecutive on-call days; enforce schedule quality checks (no gaps, even spread of
  shifts) in the scheduling tool.

## 4. Handover ritual (15 minutes, same time weekly)
Outgoing primary walks through: open incidents and their state; active silences and
why; ongoing risky changes (migrations, freezes, canaries in flight); anything flaky
with a link; pages last week by alert name with the action taken; runbook gaps found.
Incoming confirms pager works (test page), VPN/credentials valid, laptop charged. Notes
go in a standing document/channel so the week's history is searchable.

## 5. Onboarding a new on-caller
The SRE Book sequence, condensed:
1. **Study**: an on-call learning checklist (architecture docs, dependency map, dashboards,
   past postmortems, where the runbooks live) that the student completes before shadowing;
   progress on it is visible to mentors.
2. **Shadow**: pages are copied to the newcomer, at first in business hours; they watch the
   outage unfold without time pressure, review the reasoning afterward, and co-author the
   postmortem (not the sole author).
3. **Reverse shadow**: the newcomer is primary and owns escalations; the experienced SRE
   diagnoses independently without modifying state and helps as needed. Debrief after each page.
4. **Wheel of Misfortune / disaster role-playing**: at its best a weekly ritual; a game master
   picks a primary and secondary on-caller, announces a page from a past incident or a
   hypothetical, and describes what the graphs would show as they say what they would do.
   Sessions run roughly 30-60 minutes. Everyone attends; seniors go too.
5. **Project work on the service** before the first solo shift: fixing one real postmortem
   action item builds more understanding than any doc.
6. First solo shifts during the day with the mentor as secondary; night shifts later.
Readiness criteria are explicit, not "feels ready": the Book describes teams gating on a
final exam or on completion of the learning checklist.

## 6. Tooling
Scheduler with overrides, swaps, iCal export and escalation chains
(`...prometheus-grafana.grafana-oncall-schedules-and-escalation`, PagerDuty, Opsgenie);
one alert → one page with runbook link; a personal notification policy that actually
wakes people (`important` → call/SMS); chat channel per incident; a "who's on call" command.

## Gotchas
- "Everyone on the team is on call" with 3 people is a burnout schedule disguised as fairness.
- Developers on call without ownership of the alerts (SRE owns alert config) learn nothing
  and resent it; the people paged must be able to change the alerts and the code.
- Handover in a chat message nobody reads; make it synchronous or a short doc with a checklist.
- Measuring MTTA alone encourages acking and ignoring; pair it with time-to-mitigate and
  non-actionable rate.
- Skipping shadowing because "they're senior": seniority elsewhere does not include this
  service's failure modes.

## Verify
- [ ] Rotation meets the Book's minimum size (8 single-site, 6 per site dual-site), has no gaps, changes shifts at a daytime hour, and has documented response-time and compensation rules.
- [ ] Last quarter: at most 2 incidents per 12-hour shift, every page actionable, ops time per engineer ≤ 50%.
- [ ] Every new on-caller in the last year completed study → shadow → reverse shadow before a solo shift.
- [ ] A Wheel of Misfortune session happened recently and produced at least one runbook fix.

## Checked
2026-11-01. Confirmed in SRE Book Being On-Call (50% cap, 25% on-call, minimum 8 single-site and 6 per site dual-site, 5 and 30 minute response times, 6 hours per incident and 2 per 12-hour shift, compensation, primary/secondary, follow-the-sun trade-offs, actionable alerts) and Accelerating SREs to On-Call (learning checklist, weekly disaster role playing at 30-60 minutes, shadow, reverse shadow, postmortem co-authoring). Removed the invented shadow duration, 20% non-actionable threshold, 25%-of-shifts rule and runbook-count readiness test.
Method: documentation only; no commands were run.
