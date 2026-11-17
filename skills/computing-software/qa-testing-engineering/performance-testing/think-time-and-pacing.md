---
id: computing-software.qa-testing-engineering.performance-testing.think-time-and-pacing
name: think-time-and-pacing
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [pacing, think-time, workload-modelling, load-testing, iteration-pacing]
level: practitioner
status: verified
description: "Design think time and pacing for load tests: realistic think-time distributions, fixed-interval pacing to hit target rates, and computing users needed with Little's law."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#Constant_Throughput_Timer
  - https://docs.locust.io/en/stable/writing-a-locustfile.html#wait-time-attribute
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Think time and pacing design

## Definitions
- **Think time**: pause between user actions within a session (reading, typing). Models user behaviour.
- **Pacing**: the interval between the start of consecutive iterations of a virtual user. Controls throughput per user.

## Think time
- Derive from analytics (time on page) or session recordings; use a range or distribution, not a constant (`sleep(randomBetween(3, 8))`), so users do not synchronise. In k6 use `randomIntBetween(3, 8)` from `https://jslib.k6.io/k6-utils/1.4.0/index.js` (there is no `randomBetween`).
- Exclude think time from transaction timings: k6 `sleep()` is outside `http_req_duration` (a 1 s paced iteration had an average request time of 0.18 ms), and JMeter timers are processed before each sampler in their scope.
- Zero think time turns users into stress generators; label such tests as throughput tests.

## Pacing
Iteration interval = target time per iteration; tool waits the remainder after each iteration.
```python
# Locust: each user starts a task every 10 s regardless of response time (if response < 10 s)
wait_time = constant_pacing(10)
# Or constant_throughput(0.1) = 0.1 tasks/s per user
```
JMeter: Constant Throughput Timer / Precise Throughput Timer (throughput given in samples per minute; the timer does not create threads, so throughput stays lower if there are too few). k6: prefer arrival-rate executors instead of manual pacing; for VU executors compute `sleep(Math.max(0, pace - elapsed))` (three iterations with `pace = 1` each took 1.00 s).
Measured in Locust with one user: `constant_pacing(1)` against a 2 ms endpoint gave 5 requests in 6 s; `constant_pacing(1)` against a 300 ms endpoint gave 5; `constant_pacing(0.2)` against the 300 ms endpoint (response longer than the pacing) gave 16, about one per response time, so the pacing silently stopped working; `constant_throughput(5)` gave 26. Locust applies wait time per task, not per request, so a task making two requests with `constant_throughput(2)` yields 4 requests/s per user (docs).

## Sizing users (Little's law)
```
Users (concurrency) = throughput (iterations/s) x iteration duration (s)
Iteration duration = sum of response times + sum of think times (or the pacing interval)
e.g. target 5 checkouts/s, each checkout session paced at 60 s -> 300 virtual users
```
If response times grow beyond the pacing interval, the target throughput is no longer achieved: report achieved throughput.

## Checklist
- Think time per step documented with its source.
- Pacing or arrival rate set to produce the modelled throughput.
- Ramp-up long enough that users are desynchronised (or randomised start offsets).

## Gotchas
- Fixed think times create lockstep waves of requests.
- Pacing shorter than iteration duration silently degrades to no pacing.

## Verify
Achieved throughput matches the workload model at target users, and think time distributions are visible in the script with documented sources.

## Checked
Locust 2.47.0 and k6 v1.4.0 on Windows against a local HTTP server.
- Run: Locust `constant_pacing` and `constant_throughput` counts quoted above (1 user, 6 s each); k6 paced loop with `sleep(Math.max(0, pace - elapsed))` (3 iterations of 1.00 s) and the `randomIntBetween` import from k6-utils 1.4.0 loaded and ran; k6 summary showed `http_req_duration` avg 180 microseconds vs `iteration_duration` 1 s.
- Computed: 5 checkouts/s x 60 s pacing = 300 users (Little's law as written).
- Fetched: JMeter component reference (Constant Throughput Timer, Precise Throughput Timer, timers processed before each sampler), k6 docs for k6-utils (`randomIntBetween`, version 1.4.0 import), Locust writing-a-locustfile page (`constant_pacing`, `constant_throughput`, per-task semantics).
