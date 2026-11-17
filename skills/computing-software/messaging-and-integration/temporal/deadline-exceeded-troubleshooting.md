---
id: computing-software.messaging-and-integration.temporal.deadline-exceeded-troubleshooting
name: deadline-exceeded-troubleshooting
category: computing-software
field: messaging-and-integration
product: temporal
tags: [deadline-exceeded, troubleshooting, grpc-health-probe, resource-exhausted, clock-skew, cluster-health, keepalive]
level: practitioner
status: docs-checked
description: "Diagnose Temporal Context deadline exceeded: clock skew, Frontend health probes, resource_exhausted metrics, bad targets, mTLS and keepAliveMaxConnectionAge."
sources:
  - https://docs.temporal.io/troubleshooting/deadline-exceeded-error
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Context: deadline exceeded` means a gRPC request from a Client or Worker to the Temporal Service did not finish in time. Causes include network interruptions, timeouts, server overload and Query errors. Work through these checks.

1. Clock skew. If a Worker clock drifts behind the Service by more than an Activity's Start-To-Close Timeout, you also see `Activity complete after timeout`. Synchronize all hosts to NTP.

2. Frontend health. Cloud users cannot see these logs and should open a support ticket with the Namespace name and sample Workflow IDs. For open source, run:

    temporal operator cluster health --address 127.0.0.1:7233

Probe each service with grpc-health-probe, using `-service=temporal.api.workflowservice.v1.WorkflowService` (frontend), `...MatchingService` and `...HistoryService`. Frontend logs also reveal failed Query requests.

3. Metrics. `resource exhausted` can surface as deadline exceeded. Chart errors by cause (`RpsLimit`, `ConcurrentLimit`, `SystemOverloaded`):

    sum(rate(service_errors_resource_exhausted{}[1m])) by (resource_exhausted_cause)

Look for high latency in a specific service and check that service.

4. Targets. Missing or invalid server names, host addresses or certificates in Client and Worker config also give `connection refused`.

Scenario notes:
- After enabling mTLS: run the health command, add missing web UI environment variables, and make server names and certificates match between Frontend and internode.
- After a restart: wait for reconnection, then recheck all services, History and server logs.
- When starting or scheduling Workflows: raise `frontend.keepAliveMaxConnectionAge` so requests finish before the connection closes, and watch server load afterward.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: troubleshooting/deadline-exceeded-error (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
