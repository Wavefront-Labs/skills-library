---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.reliability-testing-chaos-and-dr-exercises
name: reliability-testing-chaos-and-dr-exercises
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, reliability-testing, chaos-engineering, disaster-recovery-testing, steady-state-hypothesis, blast-radius, fault-injection]
level: advanced
status: docs-checked
description: "Test reliability before users do: the SRE testing hierarchy, chaos experiments built on a steady-state hypothesis and bounded blast radius, and testing disaster tooling."
sources: ["https://sre.google/sre-book/testing-reliability/", "https://principlesofchaos.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reliability testing, chaos engineering and DR exercises

**Goal:** learn how the system fails on your schedule, and show that recovery tooling works before it is needed.

## 1. Testing for reliability (SRE Book)
- Test levels: unit, integration, system (smoke, performance, regression) for undeployed software; production tests
  (configuration tests, stress tests, canaries) against the live service. Tests have costs: unit tests take
  milliseconds, bringing up a full server with dependencies can take minutes to hours.
- Passing tests do not prove reliability; failing tests generally prove its absence. Each test that passes before and
  after a change reduces the uncertainty the reliability analysis must allow for.
- Stress tests find the limits of a service and its components, which often fail catastrophically instead of degrading.
- Statistical techniques named in the chapter: Lemon (fuzzing), Chaos Monkey and Jepsen (distributed state). They are
  not necessarily repeatable, so rerunning after a code change does not prove the fault is fixed. Log the random choices
  (for example the seed), turn the log into a release test, and replay it a few times: the rate of non-failure on replay
  tells you how hard it will be to show the fault is fixed.
- Testing disaster: many recovery tools can be designed to operate offline: compute a checkpoint state equivalent to
  cleanly stopping the service, push it so existing non-disaster validation tools can load it, and use the usual release
  barrier tools to trigger a clean start. Tests are easy to write when those constraints hold and much harder when
  broken. Online repair tools operate outside the mainstream API and must be tested against eventual consistency; offline
  tools usually assume instant consistency, and a unified instrumented binary may be needed.
- SRE tools and automation need tests too. Barrier defence for risky software: place a barrier in the replication
  config so the replica fails its health check and is not released to users, make the risky software check for the
  barrier at start-up and only touch unhealthy replicas, and remove the barrier with the same validating tool used for
  black-box monitoring.

## 2. Chaos experiments (Principles of Chaos Engineering)
Chaos engineering is experimenting on a system to build confidence it can withstand turbulent production conditions.
Steps: define a steady state as a measurable output; hypothesise it continues in both control and experimental
groups; introduce variables reflecting real events (servers crash, disks malfunction, connections severed); try to
disprove the hypothesis by looking for a difference between the groups. Advanced principles:
- Build the hypothesis around steady-state output (throughput, error rates, latency percentiles), not internal
  attributes: verify that the system works, not how.
- Vary real-world events, prioritised by impact or estimated frequency, including software failures like malformed
  responses and non-failure events such as traffic spikes or scaling events.
- Run experiments in production, because behaviour depends on environment and traffic; real traffic is the way to
  capture the actual request path.
- Automate experiments and run them continuously.
- Minimise blast radius: some short-term impact is allowed but the engineer must contain the fallout.
Systemic weaknesses the page lists: improper fallbacks when a service is unavailable, retry storms from badly tuned
timeouts, outages when a downstream dependency receives too much traffic, cascading failures from a single point of
failure.

## Verify
- [ ] Each experiment has a written steady-state hypothesis in measurable output terms and a way to stop it.
- [ ] Random-fault runs are logged with seeds so failures can be replayed.
- [ ] Disaster tooling is tested for its offline, checkpoint, loadable, barrier and clean-start phases.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Testing for Reliability chapter and principlesofchaos.org. Removed:
the Chaos Mesh, AWS Fault Injection Service (docs.aws.amazon.com not readable) and Workbook non-abstract-design sources
and every Chaos Mesh YAML, FIS action, Istio fault and toxiproxy claim, the game-day roles and scoring, the DiRT
description and its restore and failover drill schedule, RTO/RPO scorecards, and the list of what usually breaks, none
of which appear on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
