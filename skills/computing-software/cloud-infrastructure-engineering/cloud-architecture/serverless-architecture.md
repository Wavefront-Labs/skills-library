---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.serverless-architecture
name: serverless-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, serverless-architecture, faas, event-driven-serverless, managed-services-first, serverless-patterns]
level: practitioner
status: draft
description: "Apply the serverless architecture style: managed services first, functions as glue, event sources, orchestration, limits, observability and when the style stops fitting."
sources: ["https://learn.microsoft.com/azure/architecture/guide/architecture-styles/", "https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html", "https://serverlessland.com/patterns"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serverless architecture style

## Characteristics
- No servers to manage; scale to zero; pay per use.
- Composed of managed services: API gateway, functions, queues/topics, event bus, workflow
  orchestrator, managed databases (DynamoDB, Cosmos DB serverless, Aurora Serverless), object storage.
- Event-driven: functions triggered by HTTP, queues, streams, storage events, schedules.

## Design principles
1. **Managed service first; function as glue** - prefer direct integrations (API Gateway -> SQS,
   EventBridge Pipes, Step Functions SDK integrations) over functions that only forward data.
2. **Orchestrate** multi-step flows with Step Functions / Durable Functions / Workflows instead of
   functions calling functions.
3. **Async by default**; synchronous paths kept short.
4. **Idempotent handlers** and DLQs for every async source.
5. **Least privilege per function**; config and secrets from parameter stores.
6. **Observability**: structured logs, tracing, metrics per function and per integration.
7. **IaC** for everything (SAM/CDK/Serverless Framework/Bicep/Terraform).

## When it stops fitting
Sustained high utilisation (cheaper on containers), long-running compute beyond limits,
latency-critical paths sensitive to cold starts, heavy local state, need for portability across clouds.

## Gotchas
- Distributed monolith of hundreds of functions sharing a database.
- Hidden costs: API gateway per-request, logging volume, NAT for VPC functions.

## Verify
- [ ] Cost model at expected and 10x volume; architecture review against the serverless lens.
