---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.pager-load-caps-and-overload-response
name: pager-load-caps-and-overload-response
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [pager-load, operational-overload, alert-fan-out, incidents-per-shift, embedded-sre, on-call, pager-load-cap, operational-overload-response]
level: practitioner
status: docs-checked
description: "Measure pager load against the SRE target of at most two incidents per 12-hour shift, and respond to overload: fix monitoring, group alerts, set quarterly goals, borrow an SRE."
sources: ["https://sre.google/sre-book/being-on-call/", "https://sre.google/sre-book/operational-overload/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Pager load caps and operational overload response

## The targets (SRE Book, "Being On-Call")
- At least 50% of SRE time goes to engineering; of the remainder, no more than 25% on-call.
- An incident is a sequence of related events and alerts with the same root cause, discussed in one postmortem. Dealing
  with one (root-cause analysis, remediation, postmortem, bug fixes) takes about 6 hours on average, so the maximum is
  2 incidents per 12-hour on-call shift.
- Distribution of paging events should be very flat over time with a likely median of 0; a component that pages daily
  (median incidents per day above 1) is likely to cause more incidents than allowed.
- Measure incidents, not pages: the Book wants symptoms of overload to be measurable, with examples such as daily
  tickets and paging events per shift under 2.

## When the limit is exceeded
If it is exceeded temporarily, for example for a quarter, put corrective measures in place to return to sustainable
load. The Book's overload guidance:
1. The SRE team and leadership include concrete objectives in quarterly work planning.
2. Temporarily loan an experienced SRE to the overloaded team (Book chapter "Embedding an SRE to Recover from
   Operational Overload"). One engineer is enough; two may cause defensiveness. The embedded SRE focuses on improving
   the team's practices, not emptying the ticket queue.
3. **Fix misconfigured monitoring**, a common cause: paging alerts should match symptoms that threaten the SLO, and
   all must be actionable. Hourly low-priority alerts cause fatigue that makes serious alerts get less attention.
4. **Control alert fan-out**: group related alerts, silence duplicate or uninformative ones during an incident, and
   tweak noisy alerts toward a 1:1 alert-to-incident ratio.

## Gotchas
- Counting pages instead of incidents overstates load from noisy alerts; count both.
- The embedding chapter warns that a team under pressure slips into "ops mode", responding to emergencies instead of
  reducing them; more tickets should not require more SREs.

## Checked
2026-11-01. Confirmed against the SRE Book chapters "Being On-Call" (50% and 25% rule, 6 hours per incident, 2 per
12-hour shift, flat distribution, overload measures, monitoring and fan-out) and "Embedding an SRE to Recover from
Operational Overload" (one engineer, focus on practices). Removed: the PagerDuty and Alertmanager recipes, the
actionable ratio thresholds and the 20 percent alert rule, the "give back the pager" step and the error-budget freeze step
(neither is on these pages), and the Workbook source (not read).
Method: documentation only; no commands were run.
