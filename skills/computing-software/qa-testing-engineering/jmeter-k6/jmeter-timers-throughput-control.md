---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-timers-throughput-control
name: jmeter-timers-throughput-control
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [constant-throughput-timer, precise-throughput-timer, jmeter-timers-pacing, think-time-jmeter, throughput-shaping]
level: practitioner
status: docs-checked
description: "Control JMeter think time and throughput with Constant, Random, Constant Throughput and Precise Throughput timers and the Throughput Shaping plugin, plus scope rules."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#timers
  - https://jmeter.apache.org/usermanual/component_reference.html#Precise_Throughput_Timer
  - https://jmeter-plugins.org/wiki/ThroughputShapingTimer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timers (constant throughput, precise throughput, random)

## How timers apply
A timer delays **each sampler in its scope**, executed before the sampler (after pre-processors). Several timers in scope add up. Put a think-time timer as a child of a specific sampler (or in a Flow Control Action sampler) to avoid delaying every request.

## Think time
- Constant Timer: fixed delay.
- Uniform Random Timer: constant offset + random up to range.
- Gaussian Random Timer: constant offset plus a Gaussian-distributed value (mean 0, standard deviation 1) times the deviation you specify.

## Throughput targets
**Constant Throughput Timer**: target samples per *minute*, calculated per "this thread only", "all active threads in current thread group", "all active threads" (each other Thread Group then needs its own timer with the same settings) or the "(shared)" variants (more accurate overall rate; the non-shared variants spread transactions more evenly across threads). Pauses threads to hold the target; it cannot create load beyond what threads can produce. Do not change the target too often during a test; changes take a while to take effect.

**Precise Throughput Timer**: models a Poisson arrivals schedule to keep total throughput close to the target; it does not generate threads. "Test duration (seconds)" is a hint that lets it produce an exact number of samples over that period (it does not limit the test). It works best below 36000 requests/hour; place it under the first element in a test loop, and set ramp-up and delay to 0 as the manual recommends. The manual notes the Open Model Thread Group is often a better way to get a load profile.

**Throughput Shaping Timer** (plugin `jpgc-tst`): an RPS schedule; pair with the **Concurrency Thread Group** and `${__tstFeedback(tst-name,1,100,10)}` so threads scale to meet the RPS.

## Sizing threads for a target
Threads needed are roughly target RPS x (response time + think time) (Little's law). If threads are too few, the timer target is unreachable: check actual throughput in results.

## Gotchas
- Constant Throughput Timer's unit is per minute (60 = 1/s); common mistake.
- A timer at Thread Group level applies to every sampler in the group; scope it with a parent element when only some requests should be paced.
- Timers apply to samplers; the Transaction Controller option "Include duration of timer and pre-post processors in generated sample" affects the reported transaction time.

## Verify
Aggregate Report throughput matches the target during steady state.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01; latest release 5.6.3) and the JMeter Plugins wiki sources (undera/jmeter-plugins, site/dat/wiki, last commit 2026-10-23). Confirmed: timer scoping and summation, Gaussian timer formula, Constant Throughput Timer unit and calculation modes, Precise Throughput Timer behaviour and recommendations, `__tstFeedback` arguments, jpgc-tst id. Removed the unconfirmed Precise Throughput Timer version claim.

Method: documentation only; no commands were run.
