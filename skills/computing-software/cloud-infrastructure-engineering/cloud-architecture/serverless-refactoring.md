---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.serverless-refactoring
name: serverless-refactoring
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, serverless-refactoring, lambda, azure-functions, cloud-functions, event-driven-refactor, function-granularity]
level: advanced
status: draft
description: "Refactor workloads to serverless functions: picking candidates, function boundaries, state and connection handling, limits, cold starts, observability and cost checks."
sources: ["https://docs.aws.amazon.com/lambda/latest/operatorguide/intro.html", "https://learn.microsoft.com/azure/azure-functions/functions-best-practices", "https://cloud.google.com/functions/docs/bestpractices/tips"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Refactoring to serverless

## Good candidates
Event handlers (object uploaded, message arrived), scheduled jobs, spiky APIs with idle time,
glue between services, file/image processing. Poor: long-running CPU-heavy jobs beyond time limits
(Lambda max 15 min), steady high-throughput APIs (cost), workloads needing local state or GPUs.

## Steps
1. Carve out one capability at a time (strangler fig) behind an API gateway or event source.
2. **Granularity**: one function per event type or per cohesive API resource; avoid hundreds of
   nano-functions sharing a database (distributed monolith).
3. **State**: externalise to managed stores; idempotent handlers (events are at-least-once).
4. **Connections**: initialise SDK clients outside the handler; use RDS Proxy / connection pooling
   or HTTP-based data APIs to avoid exhausting database connections at scale.
5. **Limits**: payload sizes (sync Lambda 6 MB), timeouts, concurrency quotas (reserved/provisioned
   concurrency), async retry and DLQ/on-failure destinations.
6. **Cold starts**: smaller packages, lighter runtimes, provisioned concurrency / premium plans,
   SnapStart for Java on Lambda.
7. **Observability**: structured logs, tracing (X-Ray / OpenTelemetry), metrics on errors,
   throttles, duration, iterator age.
8. **IaC**: SAM, Serverless Framework, CDK, Bicep/Terraform; per-function least-privilege roles.
9. Compare cost at expected volume vs container baseline.

## Gotchas
- Recursive triggers (function writes to the bucket that triggers it) - runaway cost.
- Synchronous chains of functions add latency and double billing; use orchestration (Step
  Functions, Durable Functions) or events.
- Unbounded concurrency overwhelms downstream; set reserved concurrency.

## Verify
- [ ] Load test shows no DB connection exhaustion and acceptable p99 including cold starts.
- [ ] Failure path (DLQ) tested.
