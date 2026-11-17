---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cold-start
name: cold-start
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, cold-start, provisioned-concurrency, snapstart, min-instances, startup-time, jvm-startup]
level: practitioner
status: draft
description: "Measure and mitigate cold starts for functions and containers: package size, runtime choice, init work, provisioned concurrency, min instances, SnapStart and startup probes."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html", "https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html", "https://cloud.google.com/run/docs/tips/general#start_containers_quickly", "https://learn.microsoft.com/azure/azure-functions/functions-premium-plan"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cold-start mitigation

## Measure first
- Lambda: `Init Duration` in REPORT log lines; X-Ray initialization segment.
- Cloud Run / Container Apps: container startup latency metrics; request latency when instance count rises.
- Determine what % of requests hit cold starts (often < 1% at steady traffic, high at low traffic).

## Mitigations (cheapest first)
1. **Reduce init work**: lazy-load rarely used clients, avoid network calls at startup, trim
   dependencies, smaller images (distroless, multi-stage builds).
2. **Runtime**: Go/Rust/Node start faster than JVM/.NET without tuning; for Java use SnapStart
   (Lambda), CRaC, GraalVM native image, or tiered compilation flags.
3. **Memory/CPU**: more memory = more CPU on Lambda = faster init; Cloud Run "startup CPU boost".
4. **Keep warm capacity**: Lambda provisioned concurrency (with autoscaling schedule), Cloud Run
   `min-instances`, Azure Functions Premium always-ready instances, Container Apps min replicas.
5. **Architecture**: move latency-sensitive paths off scale-to-zero; async for the rest.

## Gotchas
- Provisioned concurrency billed even when idle; schedule it for business hours.
- Scheduled "ping" warmers keep one instance warm, not the N needed under bursts.
- VPC-attached functions had large cold starts historically; now much reduced (Hyperplane ENIs).

## Verify
- [ ] p99 latency including cold starts meets SLO under a burst test from zero.
