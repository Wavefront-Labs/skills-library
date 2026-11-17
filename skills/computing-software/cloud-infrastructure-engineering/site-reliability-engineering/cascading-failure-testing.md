---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cascading-failure-testing
name: cascading-failure-testing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [cascading-failure-testing, overload-testing, cascading-failures, load-testing, fault-injection, popular-clients]
level: advanced
status: docs-checked
description: "Test for cascading failures: load until failure and beyond, test recovery after load drops, test popular clients, noncritical backends and component loss under load."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing for cascading failures

SRE Book section "Testing for Cascading Failures": the specific ways a service fails are hard to predict from first
principles, so test how it behaves under heavy load.

## Tests from the book
1. **Test until failure and beyond**: load test each component separately until it breaks. Ideally past its limit it
   serves errors or degraded results without significantly reducing the rate of successful requests; a component prone
   to cascading failure crashes or serves a very high error rate. Test both gradual ramps and impulse load, because
   caching makes them behave differently. For stateful or caching services, track state across interactions and check
   correctness at high load, where subtle concurrency bugs appear.
2. **Test recovery**: push well beyond nominal load, then return to it. Can a degraded mode exit without human
   intervention? How far must load drop for the system to stabilise after a few servers crash?
3. **Test popular clients**: understand how large clients use the service: can they queue work while it is down, do they
   use randomized exponential backoff, can an external trigger (for example a software update clearing an offline
   client's cache) create a large load spike? Stage failures with the largest internal clients and ask how they handle
   backend failure.
4. **Test noncritical backends**: make them unavailable, and also make them never respond (blackholing). The frontend
   must not start rejecting lots of requests, run out of resources or serve with very high latency. Long deadlines make
   backends advertised as noncritical able to hurt the frontend.
5. **Production tests in a small slice**, if you trust your protections: reduce task counts quickly or slowly beyond expected
   patterns, rapidly lose a cluster's worth of capacity, blackhole various backends. Have extra capacity ready to fail
   over manually if automatic protections fail.

## Test plan template
```
Component: <name>
1) Ramp past capacity, then return to nominal.
   Expect: successful request rate stays near capacity, excess rejected, recovery without manual action.
2) Lose capacity (a zone or cluster) at near-peak load.
   Expect: load shedding at most; no crash loops.
3) Slow or blackhole a noncritical dependency.
   Expect: latency and error rate of the main path unchanged.
4) Replay a large client's retry behaviour against a failing backend.
   Expect: backend load stays bounded by the client's retry budget.
Environment and dashboards: <links>
```

## What to watch
Goodput, error rate by type, queue lengths, restarts, health-check failures, retry ratios, dependency request rate
(amplification), recovery time.

## Gotchas
- Tests at normal load miss the problem; cascades emerge at overload.
- If recovery requires a manual action, document it as a known gap and fix it.

## Verify
- [ ] All the test types above have been run recently, with results recorded.
- [ ] Every "did not recover" finding has an owner.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Addressing Cascading Failures", sections "Test Until Failure and
Beyond", "Test Popular Clients" and "Test Noncritical Backends". Removed: the specific multipliers, durations, latency
targets and 1.1x figure from the template, and the Istio, Toxiproxy, Chaos Mesh, `tc` and `toxiproxy-cli` tool examples
(not on the cited page).
Method: documentation only; no commands were run.
