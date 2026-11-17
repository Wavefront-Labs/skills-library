---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.request-criticality-propagation
name: request-criticality-propagation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [criticality-propagation, request-criticality-levels, handling-overload, load-shedding, priority, grpc-metadata]
level: advanced
status: docs-checked
description: "Tag requests with one of four criticality values (CRITICAL_PLUS to SHEDDABLE), propagate it to downstream calls, set it near the client edge, and reject lower criticality first."
sources: ["https://sre.google/sre-book/handling-overload/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request criticality propagation

Source: SRE Book, "Handling Overload", section "Criticality".

## The four values
- **CRITICAL_PLUS**: reserved for the most critical requests, those that will result in serious user-visible impact if they fail.
- **CRITICAL**: the default for requests sent from production jobs. User-visible impact, possibly less severe than CRITICAL_PLUS. Services are expected to provision enough capacity for all expected CRITICAL and CRITICAL_PLUS traffic.
- **SHEDDABLE_PLUS**: traffic for which partial unavailability is expected. The default for batch jobs, which can retry requests minutes or even hours later.
- **SHEDDABLE**: traffic for which frequent partial unavailability and occasional full unavailability is expected.

The book says four values proved robust enough to model almost every service, and that adding more would require more resources to operate the criticality-aware systems.

## How the book uses it
- When a customer runs out of global quota, a backend task rejects requests of a given criticality only if it is already rejecting all requests of all lower criticalities. Per-customer limits can be set per criticality.
- A task that is itself overloaded rejects requests of lower criticalities sooner. Task-level overload protection is utilization-based (often CPU rate, sometimes memory too): as utilization approaches configured thresholds, requests are rejected by criticality, with higher thresholds for higher criticalities.
- The adaptive throttling system keeps separate stats for each criticality.
- Criticality is orthogonal to latency requirements: search suggestions shown while the user types are highly sheddable but have stringent latency requirements.

## Propagation
- Google's RPC system propagates criticality automatically: if request A causes outgoing requests B and C, they use A's criticality by default.
- Before standardizing, many systems had ad hoc, mutually incompatible notions of criticality. Standardizing and propagating it means overloaded dependencies abide by the high-level criticality however deep they are in the RPC stack.
- The stated practice is to set criticality as close as possible to the browsers or mobile clients, typically in the HTTP frontends that produce the HTML, and override it only where it makes sense at a specific point in the stack.
- Whatever transport you use (the book does not prescribe one), make the value part of the RPC layer so no hop drops it.

## Checked
- 2026-11-08: all points above were confirmed on the SRE Book Handling Overload page ("Criticality" and "Utilization Signals").
- Removed: the sample gRPC interceptors and header name, the W3C baggage suggestion, the example admission thresholds, the example mapping of products to values, the edge-overwrite advice and the checklists. The gRPC metadata and Envoy pages were dropped from sources because no claim depends on them.
Method: docs-only read of cited pages, 2026-11-08
