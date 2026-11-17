---
id: mathematics.operations-research.queueing-theory.queue-capacity-planning-with-littles-law
name: queue-capacity-planning-with-littles-law
category: mathematics
field: operations-research
product: queueing-theory
tags: [operations-research, queueing-theory, queuing-theory, waiting-lines, littles-law, utilisation, utilization, m-m-1, m-m-c, erlang-c, erlang-b, kingman-formula, arrival-rate, service-rate, poisson-arrivals, coefficient-of-variation, capacity-planning, staffing, call-centre, service-level, wait-time, throughput, latency, server-sizing]
level: practitioner
status: verified
description: "Size servers or staff with queueing maths: Little's law, utilisation, M/M/1 and M/M/c (Erlang C) wait formulas, Kingman's approximation for variability, and why 90% busy is too busy."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue capacity planning with Little's law

**Goal:** answer "how many servers / agents / checkouts do we need to keep waits
under X?" with numbers, and understand why queues explode near full utilisation.

## 1. Measure the inputs (with units)
- **λ** — arrival rate (customers per hour). Use the busiest relevant interval
  (peak 15–60 min), not the daily average.
- **Service time** 1/μ — average time one server spends per customer (handle time).
- **c** — number of parallel servers.
- **Variability:** coefficient of variation (SD / mean) of inter-arrival times (cₐ) and
  service times (cₛ). Poisson arrivals and exponential service have CV = 1.

## 2. Little's law — always true
**L = λ·W** (average number in system = arrival rate × average time in system), for
any stable system in long-run average, regardless of distributions. Also holds for
just the queue: L_q = λ·W_q.
Uses: 12 orders/hour, each in the kitchen 25 min on average → L = 12 × (25/60) = 5
orders in progress on average. Or infer W from L and λ when timing is hard to measure.

## 3. Utilisation
**ρ = λ / (c·μ)**. Must be < 1 or the queue grows without limit. Example: 100 calls/h,
6-min handle time (μ = 10/h), c = 12 → ρ = 100/120 = 0.83.

## 4. Single server: M/M/1
- W_q = ρ / (μ − λ), W = 1 / (μ − λ), L = ρ / (1 − ρ).
- The 1/(1 − ρ) term is why: at ρ = 0.5, L = 1; at 0.8, L = 4; at 0.9, L = 9; at 0.95, L = 19.
  The last 10% of utilisation doubles or triples waits.

## 5. Multiple servers: M/M/c and Erlang C
Probability an arrival has to wait:
P_wait = [ (a^c / c!) · c/(c − a) ] / [ Σ_{k=0}^{c−1} a^k/k! + (a^c / c!)·c/(c − a) ], with a = λ/μ (offered load, in Erlangs).
Then **W_q = P_wait / (cμ − λ)** and service level SL(t) = 1 − P_wait·e^{−(cμ−λ)t}.
Worked: a = 10, c = 12 → P_wait ≈ 0.45, W_q ≈ 0.45 / (120 − 100) h ≈ 1.35 min.
(Recomputed with the function below: P_wait = 0.4494, W_q = 1.348 min; SL(20 s) = 0.598.)
```python
from math import factorial, exp
def erlang_c(a, c):
    top = a**c / factorial(c) * c / (c - a)
    return top / (sum(a**k / factorial(k) for k in range(c)) + top)
```
Staffing: increase c until SL meets the target (e.g. 80% answered in 20 s), then add
shrinkage (breaks, training, absence — often 25–35%): agents rostered = c / (1 − shrinkage).
**Erlang B** (no queue, blocked calls lost) is the model for trunks, beds without waiting
lists, or parking spaces.

## 6. Variability: Kingman's approximation (G/G/1)
W_q ≈ [ρ/(1 − ρ)] · [(cₐ² + cₛ²)/2] · (1/μ).
Check: a simulated G/G/1 queue (Lindley recursion, 4e5 customers, Poisson arrivals, gamma service with cs = 0.50, rho = 0.8) gave W_q = 2.51 against Kingman 2.50, and with ca = cs = 1 Kingman equals the exact M/M/1 W_q (0.4 for lambda 8, mu 10).
Halving variability (more uniform service, scheduled arrivals) cuts waits as much as
a large capacity increase. Appointment systems and standard work attack the second
factor; extra servers attack the first.

## 7. Pooling
One shared queue feeding c servers beats c separate queues at the same total
utilisation (computed: lambda 8 per server, mu 10: two separate M/M/1 queues W_q = 0.40 h, one M/M/2 queue at lambda 16 W_q = 0.178 h) (no idle server while someone waits elsewhere). Separate lines are only
better when service types differ sharply.

## Gotchas
- Using daily averages hides peaks; a system fine "on average" fails every lunchtime.
- Formulas are steady-state; short peaks, abandonment (people hang up) and retrials
  break them — use simulation (see
  mathematics.operations-research.simulation-modelling.discrete-event-simulation-output-analysis)
  or Erlang A for abandonment.
- Service time includes after-call work, setup and walking — measure the whole cycle.
- Units: keep λ and μ in the same time unit.

## Verify
- [ ] λ taken from the peak interval; μ includes the full handling cycle.
- [ ] ρ < 1 with headroom (a common rule of thumb is ≤ 0.85 for human services; not derived here).
- [ ] Little's law cross-check: measured L ≈ λ × measured W.
- [ ] Erlang C (or simulation) result meets the service-level target; shrinkage added.
- [ ] Variability considered (Kingman) before buying more capacity.
