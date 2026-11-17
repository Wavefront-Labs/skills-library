---
id: computing-software.software-engineering.software-architecture.graceful-degradation-and-fallbacks
name: graceful-degradation-and-fallbacks
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, resilience, graceful-degradation, fallbacks, load-shedding, feature-flags]
level: practitioner
status: draft
description: "Design graceful degradation: classify features by criticality, define fallbacks (cache, defaults, queue for later), shed load deliberately, and test degraded modes."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Graceful degradation and fallbacks

## Classify features
For each user journey list dependencies and mark: **critical** (checkout must work), **degradable**
(recommendations, reviews, personalisation), **deferrable** (emails, analytics, search index updates).

## Fallback options (per dependency)
| Strategy | Example |
|---|---|
| Serve stale cache | last good product price list, with `stale-if-error` |
| Static default | generic "popular items" instead of personalised |
| Hide the component | omit reviews widget; page still renders |
| Queue for later | accept order, process payment capture asynchronously |
| Reduced quality | lower-resolution images, fewer search results, simpler ranking |
| Read-only mode | allow browsing while writes are disabled during DB failover |

## Rules
- Fallbacks must be **simpler and more reliable** than the primary path, exercised regularly.
  AWS warns that rarely-used fallback code is itself a source of outages; prefer designs where the
  "fallback" is the normal path (e.g. always push data ahead of time instead of fetching on failure).
- Trigger via circuit breakers and timeouts, not after the user has waited 30 s.
- Make degraded state visible: metrics per fallback, a header or UI notice, alerts if fallback rate
  rises.
- **Load shedding**: under overload reject low-priority work early (429/503) to keep critical
  traffic within SLO. Priority from request class (health checks < batch < interactive < checkout).
- Kill switches / feature flags to disable expensive features manually during incidents.

## Test
Game days and chaos experiments: block each degradable dependency (toxiproxy, fault injection in the
mesh) and verify the journey still meets its SLO and the right fallback metric moves.
