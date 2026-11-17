---
id: computing-software.cloud-infrastructure-engineering.observability.burn-rate-thresholds-and-low-traffic-slos
name: burn-rate-thresholds-and-low-traffic-slos
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [slo, burn-rate, burn-rate-thresholds, burn-rate-table, multi-burn-rate, low-traffic-slo, synthetic-traffic-padding, extreme-availability-goals, high-availability-slo-alerting, sre-workbook]
level: advanced
status: docs-checked
description: "Derive multiwindow burn-rate thresholds from budget-consumption targets, and adapt SLO alerting for low-traffic services and extreme (99.99%+) availability goals."
sources: ["https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Burn-rate thresholds, low-traffic and extreme-availability SLOs

## Deriving thresholds
Burn rate is how fast, relative to the SLO, the service consumes its error budget; 1 uses exactly the whole budget by the end of the SLO window.
- Error rate threshold = burn rate x (1 - SLO). Time to exhaust budget = period / burn rate. Budget consumed when an alert fires = burn rate x (alert window / period).
- Detection time for a total outage is roughly alert window x threshold / error rate.

Recommended starting parameters for a 99.9% SLO over 30 days (Table 5-8):

| Severity | Long window | Short window | Burn rate | Budget consumed |
|---|---|---|---|---|
| Page | 1 h | 5 m | 14.4 | 2 % |
| Page | 6 h | 30 m | 6 | 5 % |
| Ticket | 3 d | 6 h | 1 | 10 % |

Require both windows to exceed the threshold. The short window is about 1/12 of the long one, so the alert clears soon after errors stop. Example: after 10 minutes of 15 % errors, the short-window alert clears about 5 minutes after errors stop and the long-window one about 60 minutes later. The chapter's rule-set example also contains a 24 h / 2 h condition at 3x for tickets that is not in Table 5-8; reconcile before use.

Rejected approaches, per the chapter: a fixed error-rate threshold over a short window (poor precision), a long window alone (poor reset time), and `for:` durations (do not scale with severity; recurring 5-minute total-error spikes consumed about 12 % of budget each without alerting).

## Low-traffic services
With 10 requests per hour, one failure is a 10 % error rate, a 1,000x burn rate for a 99.9 % SLO, and uses 13.9 % of the monthly budget. Options from the chapter:
1. Generate artificial traffic (covers few request types, can hide real user errors).
2. Combine related services that share a failure domain (pure total failures of one may go unnoticed).
3. Change clients or product: retries with exponential backoff and jitter, fallbacks, or require more failures before an incident counts.
4. Lower the SLO (for example 99.9 % to 99 %) or lengthen the alert window; both are product decisions.

## Extreme availability goals
- At a 90 % target, a one-hour total outage burns only about 1.4 % of budget, so the 2 % page threshold can never fire; tune the parameters.
- At 99.999 %, a total outage exhausts the 30-day budget in about 26 seconds, shorter than typical metric collection and notification delays. The defence is designing for a very low chance of total outage, for example a canary at 1 % of users, which leaves about 43 minutes.

## At scale
Do not tune windows per service; pick one parameter set and apply it everywhere, grouping request types into buckets (the chapter lists CRITICAL, HIGH_FAST, HIGH_SLOW, LOW, NO_SLO).

## Verify
- [ ] Each SLO's burn thresholds are computed from the table and documented
- [ ] Low-traffic services use one of the four options above

## Checked

2026-11-08. Confirmed on the Workbook chapter: burn-rate definition and formulas, Table 5-8 values and arithmetic, 1/12 short window, reset example, rejected approaches, low-traffic numbers and four options, extreme-availability numbers, alerting at scale. Removed as not in the chapter: the PromQL recording-rule example with job:slo_errors names, the "~52 s" detection time, the ticket/threshold table's 6 h and 3 d row justification beyond the arithmetic, the `increase(errors[1h]) > 5` rule, the traffic-guard expression, and the advice to page on any sustained error rate.
Method: documentation only; no commands were run.
