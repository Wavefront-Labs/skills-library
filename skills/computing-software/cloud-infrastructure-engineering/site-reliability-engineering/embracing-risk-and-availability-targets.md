---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.embracing-risk-and-availability-targets
name: embracing-risk-and-availability-targets
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, embracing-risk, risk-tolerance, availability-targets, nines, availability-table, cost-of-reliability, time-based-availability, aggregate-availability, request-based-availability, dependency-availability, serial-dependencies, risk-matrix, reliability-vs-velocity, consumer-vs-infrastructure, target-setting, slo-selection, error-budget, business-alignment]
level: advanced
status: docs-checked
description: "Set an availability target deliberately: the nines table and what each costs, time- vs request-based availability, risk tolerance of consumers vs infrastructure services."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/sre-book/service-level-objectives/", "https://sre.google/workbook/implementing-slos/", "https://sre.google/sre-book/availability-table/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embracing risk and availability targets

**Goal:** choose a reliability target that users notice, the business can pay for, and the
team can engineer to — then stop paying for reliability beyond it.

## 1. The premise
100% is probably the wrong target: it is impossible to achieve and typically more than users notice (the SRE
Book: a user on a 99% reliable smartphone cannot tell 99.99% from 99.999%), and an incremental improvement in
reliability may cost 100x more than the previous one, through redundancy and opportunity cost. Reliability is a feature competing with other features for the same
engineers. The job is to find the **lowest** target that keeps users happy, and spend the
rest (the **error budget**) on change velocity.

## 2. The nines, in time
| Target | Downtime / year | / 30 days | / week |
|---|---|---|---|
| 99% | 3.65 d | 7.2 h | 1.68 h |
| 99.9% | 8.76 h | 43.2 min | 10.1 min |
| 99.95% | 4.38 h | 21.6 min | 5.04 min |
| 99.99% | 52.6 min | 4.32 min | 1.01 min |
| 99.999% | 5.26 min | 25.9 s | 6.05 s |
Formula: `downtime = (1 - target) × period`. Memorise 99.9% ≈ 43 min/month.

## 3. Time-based vs request-based
- **Time-based** (`uptime / total time`): simple, but ignores partial outages and
  low-traffic hours; natural for infrastructure with no request stream.
- **Request-based** (`good requests / total requests`): a 50% error rate for 10 minutes at
  peak counts more than at 3 a.m.; works for partial failures; it is what SLIs usually measure.
  Prefer it; convert to "nines" for communication.
- The SRE Book uses request success rate (aggregate availability over a rolling window) because a globally
  distributed service is almost always at least partially up; a daily 99.99% target on 2.5M requests allows 250 errors.

## 4. Who sets the number: risk tolerance
Consumer-facing products: ask the product owner — what availability do users expect?
does a failure cost revenue, trust, or just annoyance? what does the competition offer?
can the service degrade (read-only, cached) instead of fail? do failures affect
everyone or a slice? Do a **cost analysis**: what would one more nine cost, and does the extra
revenue offset it? (The book's example: 99.9% -> 99.99% on $1M revenue is worth $900.)
Infrastructure services (storage, queues, Kubernetes): different customers want
different things (batch wants throughput; interactive wants latency). Offer **explicit
tiers** (standard vs premium pools, priority classes) with separate targets and prices,
rather than one compromise target everyone resents.

## 5. Dependency math
A service calling N dependencies in series cannot exceed the product of their
availabilities: `0.999 × 0.999 × 0.999 ≈ 0.997`. So:
- Your target must be **below** your critical dependencies' targets, or you must remove
  the dependency from the critical path (cache, fallback, async).
- Redundant (parallel) components multiply failure probabilities instead:
  two independent 99% replicas ≈ 99.99% — if they fail independently (same bug or same
  deploy pipeline = not independent).
Write the dependency chain with each target next to it before announcing yours.

## 6. From target to budget to behaviour
1. Pick the SLI (see `...site-reliability-engineering.slo-sli-design`).
2. Base the target on what users need and what has actually been achieved, not on a wish.
3. Error budget = `1 − target` over the window: 99.9% ⇒ 0.1% of
   requests, or 43.2 min of full outage per 30 days.
4. Agree the policy (`...site-reliability-engineering.error-budget-policy`): what happens
   when it is spent — freeze risky launches, prioritise reliability work — and what counts
   (planned maintenance spends budget too unless the SLO excludes it explicitly).
5. Review quarterly: budget never spent ⇒ target too loose or team too cautious; always
   blown ⇒ target too tight or investment needed.

## 7. Explicit risk register (what you are choosing to accept)
List each accepted risk with blast radius and expected frequency: single-region
deployment, no DB replica promotion automation, a third-party payment gateway at a lower
target than yours. Estimate frequency and duration for each. Expected downtime
= Σ frequency × duration; compare against the budget. If the sum exceeds the budget, the
target is a wish.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Embracing Risk (100% not the right target, smartphone
example, 100x incremental cost, nines as orders of magnitude, request success rate, 2.5M-request example, $900
example, consumer and infrastructure risk tolerance, tiers) and the Availability Table page (every downtime figure).
The dependency products are arithmetic. Removed: the 10x cost claim, the what-it-implies column, traffic-weighting,
the one-notch platform rule, the 4-8 week and 30 d rolling window claims, the example region outage figures and the
0.05 point tolerance.
Method: documentation only; no commands were run.

## Gotchas
- Quoting an SLA (contract with penalties) as the SLO: the internal objective must be
  stricter than the external promise, or you find out from customers.
- Picking 99.99% for a service released daily by a team with no canary pipeline: the
  arithmetic says a single bad deploy (4 min to detect + rollback) spends a month's budget.
- Excluding "dependency outages" from the SLI makes the number meaningless to users.
- Measuring availability only from the load balancer hides DNS/CDN/client failures
  (that may be fine if the target explicitly scopes to the service boundary — say so).

## Verify
- [ ] A one-page document states the target, the SLI, the window, the serial dependency chain with each dependency's target, and the expected-downtime sum from the risk register.
- [ ] Product owner and engineering lead have signed the number and the policy.
- [ ] Last quarter's achieved availability is close to the target (the book treats the target as both a minimum and a maximum).
