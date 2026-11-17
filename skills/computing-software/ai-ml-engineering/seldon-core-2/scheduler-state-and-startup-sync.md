---
id: computing-software.ai-ml-engineering.seldon-core-2.scheduler-state-and-startup-sync
name: scheduler-state-and-startup-sync
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, scheduler, badgerdb, startup-sync, scheduler-ready-timeout, control-plane]
level: advanced
status: docs-checked
description: "How the single Seldon Core 2 Scheduler persists state and why control plane operations pause at restart while it waits for model servers to reconnect."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/architecture/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scheduler state and restart synchronisation

The Scheduler is the main control plane component of Seldon Core 2. It manages loading and unloading of Models, Pipelines and Experiments on the relevant services and matches Models to Servers.

## Single instance
The current design allows exactly one Scheduler instance, because its internal state is persisted on disk.
## Restart behaviour
When the Scheduler (re)starts it runs a synchronisation flow. It waits for the expected model servers to connect before it proceeds with control plane operations. This protects ongoing data plane operations from interruption.

The consequence is a delay on any control plane operation (load, unload, status changes) until the flow finishes, including control plane resource status updates.

## Tuning the wait
On Kubernetes the wait is bounded by the helm value `scheduler.schedulerReadyTimeoutSeconds`. The synchronisation process has a timeout, default 10 minutes, set through the helm seldon-core-v2-components value.

## Data plane impact
The control and data planes are separate, so when control plane services such as the Scheduler are down, data plane inference can still be served.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/architecture/README.md (Scheduler and resilience sections read in full). Dropped unsupported storage-sizing, Envoy-routing and Controller-queueing statements.
