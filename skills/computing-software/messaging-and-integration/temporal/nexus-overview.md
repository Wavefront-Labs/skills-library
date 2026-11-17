---
id: computing-software.messaging-and-integration.temporal.nexus-overview
name: nexus-overview
category: computing-software
field: messaging-and-integration
product: temporal
tags: [nexus, nexus-endpoint, nexus-service, nexus-registry, nexus-machinery, cross-namespace, sync-operation, async-operation]
level: practitioner
status: docs-checked
description: "Temporal Nexus model: services, operations, endpoints and registry, sync versus async operations, handler deadline of 10 seconds, nexus machinery and multi-level calls."
sources:
  - https://docs.temporal.io/nexus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nexus connects Temporal applications across (and within) isolated Namespaces, so each team keeps its own Namespace while exposing a service contract.

Building blocks:
- Nexus Service: a named collection of Operations. An Operation hides whether it starts a Workflow, sends a Signal, runs a Query or other reliable code. For one cross-Namespace call without orchestration, use a Standalone Nexus Operation.
- Nexus Endpoint: a reverse proxy that routes to a target Namespace and Task Queue. Callers use only the Endpoint name. Managed in the Nexus Registry via UI, CLI or Cloud Ops API; in Cloud an Endpoint also belongs to a Project (management rights only). Runtime access is the Endpoint's allowlist of caller Namespaces.

Operation modes:
- Asynchronous: starts a Workflow (optionally with Eager Start) or a Standalone Activity, or sends an Update (pre-release). The handler returns an Operation token and the backing execution delivers the result; maximum Schedule-to-Close is 60 days in Cloud.
- Synchronous: must finish within the 10-second handler deadline; use for Signals, Queries, Updates or other highly reliable low-latency calls through the SDK Client.

Handlers run in Workers polling the Endpoint's Task Queue for Nexus Tasks, either collocated with what they wrap or in a dedicated router Worker (router-queue pattern).

Nexus Machinery delivers with at-least-once semantics: exponential-backoff retries, rate and concurrency limits, circuit breaking (trips after 5 consecutive retryable errors), load balancing. It speaks Nexus RPC on the wire; you only use the SDK.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: nexus (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
