---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-thread-groups
name: jmeter-thread-groups
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, thread-groups, jmeter-test-plan, concurrency-thread-group, arrivals-thread-group, open-model, ramp-up]
level: practitioner
status: docs-checked
description: "Choose and configure JMeter thread groups: standard ramp-up/loop/duration, setUp/tearDown, and plugin Concurrency/Arrivals/Ultimate thread groups for open workloads."
sources:
  - https://jmeter.apache.org/usermanual/test_plan.html#thread_group
  - https://jmeter.apache.org/usermanual/component_reference.html#Thread_Group
  - https://jmeter.apache.org/usermanual/component_reference.html#Open_Model_Thread_Group
  - https://jmeter-plugins.org/wiki/ConcurrencyThreadGroup/
  - https://jmeter-plugins.org/wiki/ArrivalsThreadGroup/
  - https://jmeter-plugins.org/wiki/ThroughputShapingTimer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMeter thread groups

**Goal:** a load profile that matches the workload model.

## Standard Thread Group
- Number of threads (users), ramp-up period (seconds to start all threads: 10 threads over 100 s start 10 s apart), loop count or "Infinite", and "Specify Thread lifetime" (duration, startup delay); the thread group ends at whichever of loops or duration comes first, and the end is only checked between samples.
- "Same user on each iteration": when selected, cookie and cache data are reused; when not, a new connection is opened between iterations.
- "Delay Thread creation until needed" creates threads only when their share of the ramp-up has elapsed.
- Action after sampler error: Continue / Start Next Thread Loop / Stop Thread / Stop Test / Stop Test Now.
- Closed model: throughput depends on response times; slow responses reduce load.

## setUp / tearDown Thread Groups
Run before/after the main groups: create test data, obtain tokens, clean up.

## Open Model Thread Group (core, experimental)
A built-in thread group driven by an arrival schedule, for example `rate(0) random_arrivals(1 min) rate(10/sec)` ramps from 0 to 10 requests per second over a minute; `pause(2 sec)` adds a gap. The manual marks it experimental and says it may change.

## Plugin thread groups (jmeter-plugins.org, install via Plugins Manager)
- **Concurrency Thread Group**: maintains a level of concurrency by starting additional threads at runtime when too few are running, with a schedule preview graph.
- **Arrivals Thread Group**: an "arrival" is a thread iteration start; new threads are created when all are busy, so load does not drop when the SUT slows (open model). Constant arrival rate means growing concurrency, so use its Concurrency Limit field as a safety valve against running out of memory.
- **Free-Form Arrivals** (same idea with a free-form schedule) and **Ultimate Thread Group** (any number of schedule records, each with its own ramp-up, shutdown and flight time).
- All four come from the `jpgc-casutg` plugin.
- Combine Concurrency TG with **Throughput Shaping Timer** and replace Target Concurrency with `${__tstFeedback(tst-name,1,100,10)}` (timer name, starting threads, max threads, spare threads) so the thread count follows the RPS schedule.

## Parameterise
`${__P(threads,10)}`, `${__P(rampup,60)}`, `${__P(duration,600)}` and pass `-Jthreads=200` on the command line, so the same .jmx serves smoke and load runs.

## Gotchas
- A ramp-up of 0 or very small with many threads starts them all at once and gives an unwanted load spike (the Precise Throughput Timer docs make the same point); too long a ramp-up leaves too few threads at the start.
- Duration is clearer than loop count for long tests, but the thread group only stops between samples, so the end can be delayed.
- Set the Arrivals Thread Group concurrency limit.

## Verify
Active Threads Over Time and Transactions per Second graphs in the dashboard match the planned profile.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01; latest release 5.6.3) and the JMeter Plugins wiki sources (undera/jmeter-plugins, site/dat/wiki, last commit 2026-10-23). Confirmed: Thread Group fields and error actions, ramp-up arithmetic, scheduler end condition, Delay Thread creation, Open Model Thread Group syntax and experimental status, Concurrency, Arrivals, Free-Form Arrivals and Ultimate thread group descriptions, `__tstFeedback` arguments, jpgc-casutg id.

Method: documentation only; no commands were run.
