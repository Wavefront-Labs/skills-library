---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.on-call-schedule-design
name: on-call-schedule-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [schedule-design, rotation-length, follow-the-sun-design, on-call, rotation-sizing, primary-secondary]
level: practitioner
status: docs-checked
description: "Design on-call schedules: team size for 25% on-call, primary/secondary, follow-the-sun split across sites, handoffs and swaps, with the SRE Book sizing arithmetic."
sources: ["https://sre.google/sre-book/being-on-call/", "https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call schedule design

## Sizing (SRE Book "Being On-Call")
- At least 50% of SRE time goes to engineering; of the rest, no more than 25% can be spent on-call.
- With two people always on call (primary and secondary) and week-long shifts, a single-site team needs a minimum of
  **eight** engineers: each is on call (primary or secondary) one week every month.
- For dual-site teams the book calls six per site a reasonable minimum, to honour the 25% rule and keep a critical mass.
- Fewer people than that means more than 25% on-call or no secondary; flag it as a staffing risk.

## Load per shift
The book's figure: dealing with one incident (root-cause analysis, remediation, follow-up such as the postmortem and
bug fixes) takes about 6 hours on average, so at most 2 incidents fit in a 12-hour shift. Keep paging flat, with a
median near zero; if a component pages daily, something else will break. If the limit is exceeded for a while (for
example a quarter), put corrective measures in place.

## Primary / secondary
The distribution of duties varies by team: the secondary may be fall-through for missed pages, or may handle non-urgent
production work while the primary takes pages. See `primary-and-secondary-on-call-roles`.

## Single-site or multi-site
The book prefers a multi-site "follow the sun" team once the work justifies growing a single-site team: it avoids night
shifts (which harm health) and limits rotation size so engineers stay in touch with production. It also names the cost:
communication and coordination overhead. Decide from the trade-offs, the importance of the system and its workload.

## Handoffs, swaps and fairness
- Hand off in writing at each switch (see `on-call-handover-process`); the Workbook's example has the outgoing engineer
  email the next one and the incoming engineer read it at shift start.
- Workbook scheduling guidance: a scheduler should be fair, factoring in preferences (its example is "no primary during
  weekends in April") and recent on-call load per engineer.
- Record swaps as overrides in the paging tool rather than verbally.

## Gotchas
- Daylight-saving changes move handoff times when the schedule and its members use different time zones.
- Join new engineers to the rotation only after training (see `on-call-learning-paths`).

## Verify
- [ ] Per-person on-call fraction is at most 25% over a quarter.
- [ ] No gap or overlap in the next few weeks of the schedule (export and check).

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Being On-Call" (50% engineering and 25% on-call rule, eight engineers
single-site with week-long shifts and one week per month, six per site for dual-site, follow-the-sun reasons and
overhead, 6 hours per incident and 2 per 12-hour shift) and the SRE Workbook chapter "On-Call" (handoff email, fairness
factors). Corrected: the skill said "2 weeks in 8"; the book says one week every month. Removed: the rotation-length
pros and cons table, handoff day and hour advice, the example site hours, the escalation timings and the one-month
publishing rule.
Method: documentation only; no commands were run.
