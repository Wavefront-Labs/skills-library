---
id: computing-software.messaging-and-integration.temporal.server-services-and-shards
name: server-services-and-shards
category: computing-software
field: messaging-and-integration
product: temporal
tags: [temporal-server, frontend-service, history-service, matching-service, worker-service, history-shard, ringpop, ports]
level: advanced
status: docs-checked
description: "Temporal Server architecture: Frontend, History, Matching and Worker services, ports, history shards and sizing ratios, ringpop membership and support policy."
sources:
  - https://docs.temporal.io/temporal-service/temporal-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Server is four independently scalable services; production should run each separately (a real deployment might be 5 Frontend, 15 History, 17 Matching, 3 Worker). They find each other, including scaled instances, through Ringpop membership.

Frontend: stateless gateway exposing the Proto API; rate limits (per host and per namespace), authorizes, validates and routes Namespace CRUD, external events, Worker polls, Visibility requests, CLI calls and cross-cluster replication calls. Every workflow-related call carries a Workflow ID that is hashed for routing. Ports: gRPC 7233, membership 6933.

History: persists workflow state and Event History and adds Tasks when a workflow can progress. gRPC 7234, membership 6934. Processes range from 1 up to the shard count; start at about 1 process per 500 shards.

History Shard: the unit of concurrent workflow throughput; each maps to one persistence partition with one operation at a time. The count must be set in the persistence config before first use and cannot change afterwards. Executions map to shards by hashing Workflow ID and Namespace. Each shard keeps history, mutable state, and internal Transfer (to Matching), Timer, Replicator and Visibility queues.

Matching: hosts user-facing Task Queues and pairs Workers with Tasks. gRPC 7235, membership 6935.

Worker Service: internal background work (replication queue, system workflows); membership port 6939.

Retention Period: closed-workflow data lifetime per Namespace; minimum 1 day, set at registration, CLI default 3 days (the API errors if unset, and 0 errors). Changes apply only to executions closing later.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: temporal-service/temporal-server (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
