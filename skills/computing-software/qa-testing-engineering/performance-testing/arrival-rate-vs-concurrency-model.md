---
id: computing-software.qa-testing-engineering.performance-testing.arrival-rate-vs-concurrency-model
name: arrival-rate-vs-concurrency-model
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [arrival-rate-model, open-workload-model, closed-workload-model, coordinated-omission-risk]
level: practitioner
status: verified
description: "Choose between arrival-rate (open) and concurrency (closed) workload models, convert between them with Little's Law, and see how each misreports a slowing system."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/
  - https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrival rate vs concurrency modelling

## Two models
- **Closed (concurrency):** fixed N users loop: request, wait for response, think, repeat. If the system slows, users send fewer requests: load drops automatically. (k6 `constant-vus`/`ramping-vus`, JMeter standard Thread Group, Locust users.)
- **Open (arrival rate):** new requests arrive at rate λ regardless of how the system is doing. If it slows, concurrency piles up. (k6 `constant-arrival-rate`/`ramping-arrival-rate`; in JMeter the Precise Throughput Timer or the Open Model Thread Group, which the JMeter manual marks experimental; the "Arrivals Thread Group" is a plugin element, not part of core JMeter.)

Public websites and APIs with many independent clients behave **open**: users don't wait for each other. Internal systems with a fixed pool of clients (call-centre agents, batch workers) are closer to **closed**.

## Why it matters
Under a closed model, a backend slowdown reduces offered load, making latency look better than users would experience and hiding queueing collapse (a form of coordinated omission, as the k6 docs call it). Schroeder, Wierman and Harchol-Balter ("Open Versus Closed: A Cautionary Tale", NSDI 2006) show a vast difference in behaviour between open and closed models and distil eight guiding principles.
Measured here with k6 v1.4.0 against a local server whose delay I changed: an open `constant-arrival-rate` of 20/s did 101 iterations in 5 s (20.2/s) at 0 ms delay and 97 (18.8/s) at 200 ms delay, while a closed `constant-vus` with 5 VUs went from 10,117 iterations/s at 0 ms to 24.9/s at 200 ms (5 VUs / 0.2 s = 25).

## Converting (Little's Law)
Concurrency N = λ x (response time R + think time Z).
Target 100 req/s, R ≈ 0.2 s, Z = 4.8 s -> N = 100 x 5 = 500 VUs in a closed model to produce the same rate **while R stays 0.2 s**. If R rises to 2 s, the closed model's rate falls to 500 / 6.8 = 73.5, about 74 req/s (computed).

## Practical choice
- Validate SLOs and capacity: open model with arrival-rate executors; size `maxVUs` ≥ λ x (expected worst R) and watch `dropped_iterations`.
- Simulate a known fixed user population (e.g. 300 concurrent agents): closed model with realistic think time.
- Report which model was used in every result.

## Gotchas
- Open-model tests can overwhelm a failing system faster: set abort thresholds.
- Generators need enough VUs for open models; insufficient VUs turn it back into a capped model with dropped iterations. k6 does warn: a 20/s arrival rate with `preAllocatedVUs: 1, maxVUs: 1` logged "Insufficient VUs, reached 1 active VUs and cannot initialize more" and reported `dropped_iterations` 63, `iterations` 17 over 4 s.

## Verify
Inject server delay mid-test: open model keeps request rate and shows latency/queue growth; closed model's rate drops.

## Checked
k6 v1.4.0 (official Windows release zip, run from a scratch folder) against a local stdlib HTTP server with an adjustable delay.
- Run: `constant-arrival-rate` vs `constant-vus` at 0 ms and 200 ms server delay (numbers in the body); the under-provisioned arrival-rate scenario (Insufficient VUs warning, `dropped_iterations`).
- Computed: 100 x (0.2 + 4.8) = 500; 500 / (2 + 4.8) = 73.5.
- Fetched: k6 open-vs-closed docs page (executor names, closed model definition, coordinated omission wording); JMeter component reference (Precise Throughput Timer note recommending Open Model Thread Group, which is marked experimental; no Arrivals Thread Group in core); the Schroeder et al. NSDI 2006 PDF (title, authors, abstract).
