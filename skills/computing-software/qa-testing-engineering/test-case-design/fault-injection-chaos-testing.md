---
id: computing-software.qa-testing-engineering.test-case-design.fault-injection-chaos-testing
name: fault-injection-chaos-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [reliability-testing, fault-injection, chaos-testing, chaos-engineering, toxiproxy, litmus, steady-state-hypothesis]
level: practitioner
status: docs-checked
description: "Test fault tolerance with fault injection and chaos experiments: steady-state hypothesis, Toxiproxy for network faults, killing pods, blast radius and abort conditions."
sources:
  - https://principlesofchaos.org/
  - https://github.com/Shopify/toxiproxy
  - https://litmuschaos.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fault injection and chaos testing

**Goal:** verify the system tolerates the failures it will meet in production. Principles of Chaos Engineering.

## Experiment structure
1. **Steady state**: a measurable normal (e.g. a checkout success rate and a latency percentile, with thresholds you choose).
2. **Hypothesis**: "if one Redis replica dies, steady state holds".
3. **Inject** the fault, smallest blast radius first (test env, one instance, small traffic %).
4. **Observe** metrics vs steady state; **abort** conditions defined up front.
5. **Learn**: fix weaknesses, add regression tests, repeat with larger scope.

## Tools
- **Toxiproxy** (in tests/CI): proxy between app and dependency, add latency, timeouts, connection resets.
  ```bash
  toxiproxy-cli create -l localhost:26379 -u redis:6379 redis
  toxiproxy-cli toxic add -t latency -a latency=2000 redis
  ```
- **Kubernetes**: LitmusChaos, a CNCF-hosted chaos engineering platform that manages chaos declaratively.

## Faults worth testing
Dependency slow (worse than down), dependency down, partial failures (5% errors), DNS failure, disk full, clock skew, node/AZ loss, message broker unavailable, certificate expiry.

## What to check
Timeouts set and shorter than the caller's; retries with backoff and jitter, bounded; circuit breakers open and close; fallbacks degrade gracefully; no data loss/duplication; alerts fire.

## Gotchas
- Running chaos in production without observability and abort automation is just an outage.
- Retries without timeouts multiply load during incidents (retry storms).

## Verify
Each experiment has a recorded hypothesis, result and follow-up; repeated experiments pass after fixes.

## Checked

2026-10-28 Confirmed against: Principles of Chaos Engineering (steady state, hypothesis, minimise blast radius, automate, production); Toxiproxy README (`toxiproxy-cli create -l ... -u ...`, `toxic add -t latency -a latency=...`, toxic types including timeout and reset_peer); LitmusChaos site (CNCF-hosted, Kubernetes). Removed or generalised: the ISTQB section number, the numeric steady-state thresholds, the `timeout=0` blackhole line, Testcontainers, Chaos Mesh, AWS FIS and Azure Chaos Studio (not in the fetched pages).

Method: documentation only; no commands were run.
