---
id: computing-software.software-engineering.software-architecture.serverless-architecture-trade-offs
name: serverless-architecture-trade-offs
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, serverless-architecture, faas, aws-lambda, cold-starts, event-driven-architecture]
level: practitioner
status: draft
description: "Decide when a serverless (FaaS plus managed services) architecture fits: cold starts, limits, cost crossover, state, observability, lock-in and testing strategy."
sources:
  - https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html
  - https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
  - https://martinfowler.com/articles/serverless.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serverless architecture trade-offs

Serverless = functions (AWS Lambda, Azure Functions, Google Cloud Run functions, Cloudflare Workers) plus managed backing services (queues, object storage, DynamoDB/Firestore, API gateways), billed per use, scaled to zero by the platform.

## Good fit
- Spiky or low, unpredictable traffic (scale to zero saves money).
- Event-driven glue: S3 upload -> thumbnail, queue consumer, scheduled jobs, webhooks.
- Small teams that want no servers to patch.

## Poor fit
- Steady high throughput: per-request pricing exceeds a reserved container/VM. Do the cost crossover maths: requests/month x avg duration x memory vs an always-on service; include API Gateway per-request fees.
- Long-running work beyond the limit (Lambda max 15 min; HTTP via API Gateway ~29 s default integration timeout).
- Latency-critical paths that cannot tolerate cold starts.
- Heavy stateful connections (websockets at scale, connection-pooled relational DBs - use RDS Proxy or a serverless-friendly DB).

## Cold starts
Caused by new execution environments (scale-out, after idle, after deploy). Mitigate: smaller packages and fewer init-time dependencies, initialise clients outside the handler (reused across warm invocations), choose runtimes with fast start (Node/Python/Go/Rust over JVM; or Java with SnapStart / GraalVM native), provisioned concurrency for critical paths.

## Design rules
- Functions are stateless; state lives in managed stores. Nothing on local disk survives (Lambda `/tmp` is per-environment scratch).
- Make handlers idempotent: event sources deliver at least once (SQS, EventBridge, S3 events).
- Configure concurrency limits (reserved concurrency) so a burst does not exhaust downstream DB connections; put queues between bursts and fragile dependencies.
- Dead-letter queues / on-failure destinations for async invocations; alert on DLQ depth.
- Avoid function-to-function synchronous chains (paying twice, timeouts compound); use Step Functions / Durable Functions / Workflows for orchestration.

## Observability and testing
- Structured logs with request ids, distributed tracing (X-Ray / OpenTelemetry Lambda layers), metrics on throttles, errors, duration, iterator age (streams).
- Unit test handler logic as plain functions; integration test against real cloud resources in an ephemeral stack (emulators like LocalStack cover only part of behaviour).

## Lock-in
Business logic in plain modules, thin handler adapters per platform (hexagonal). IaC (SAM, CDK, Terraform, Serverless Framework) to make environments reproducible.

## Verify
- [ ] Cost model compared against a container baseline at expected and 10x traffic.
- [ ] p99 latency including cold starts measured under realistic traffic.
