---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.serverless-suitability
name: serverless-suitability
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, serverless-suitability, faas, lambda, azure-functions, cloud-run-functions, cold-starts, execution-limits, event-driven-compute]
level: practitioner
status: docs-checked
description: "Assess whether a workload fits serverless functions: traffic shape, duration and resource limits, cold-start tolerance, state, connections, concurrency and observability."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html", "https://learn.microsoft.com/azure/azure-functions/functions-scale", "https://cloud.google.com/functions/docs/concepts/execution-environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serverless / FaaS suitability assessment

## Good fit
- Event-driven glue (object uploads, queue messages, webhooks, schedules).
- Spiky or low-average traffic APIs.
- Short, stateless units of work.

## Check the limits (verify current values)
| Constraint | Typical values |
|---|---|
| Max duration | AWS Lambda 900 s (15 min); Azure Functions Consumption plan 10 min maximum (Flex Consumption and Premium enforce none), but an HTTP-triggered function must respond within 230 s |
| Memory / CPU | Lambda 128 MB to 10,240 MB; CPU is allocated in proportion to memory |
| Payload | Lambda 6 MB each for synchronous request and response; 1 MB asynchronous |
| Concurrency | Lambda concurrent executions default 1,000 per Region, increasable (new accounts can start lower) |
| Ephemeral storage | Lambda `/tmp` between 512 MB and 10,240 MB |

## Assess
1. **Cold starts**: acceptable latency on first request? Mitigate with provisioned concurrency /
   min instances and smaller packages, or choose containers.
2. **Connections**: many concurrent functions × DB connections → use a connection pooler or
   an HTTP-based data API.
3. **State**: none in the function; use external stores and workflows (Step Functions, Durable Functions).
4. **Steady high load**: compare cost to containers (see serverless cost model).
5. **Local dev and testing**: emulators and infrastructure as code for the platform.
6. **Observability**: structured logs and tracing built in from the start.

## Checked
2026-10-28. Confirmed against the Lambda quotas page (900 s timeout, 128-10,240 MB memory with proportional CPU, 6 MB sync payload, 1 MB async, 1,000 concurrent executions default and increasable, `/tmp` 512-10,240 MB, reduced quotas on new accounts) and the Azure Functions scale page (Consumption 10 min, no maximum on Flex Consumption and Premium, 230 s HTTP response limit). Removed: the Cloud Run functions 60 min figure, SnapStart, RDS Proxy and the tool names (not in the fetched sources).
Method: documentation only; no commands were run.

## Verify
- [ ] Limits checked against p99 duration/payload with margin.
- [ ] Cold-start impact measured at expected traffic.
