---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.continuous-resilience
name: continuous-resilience
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resilience-testing, continuous-resilience, chaos-in-ci, resilience-regression, automated-experiments, pipeline-chaos]
level: practitioner
status: draft
description: "Run resilience experiments continuously: chaos steps in CI/CD pipelines, scheduled production experiments with guardrails, and tracking resilience regressions over time."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/what-is.html", "https://learn.microsoft.com/azure/chaos-studio/chaos-studio-overview", "https://principlesofchaos.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous resilience testing in CI/CD

## Levels
1. **Build/CI**: unit and integration tests with fault-injecting fakes (timeouts, errors).
2. **Pre-production pipeline stage**: run a standard experiment suite after deploy (kill pods,
   inject dependency latency, AZ network disruption) while a load test runs; fail the pipeline on
   SLO breach.
3. **Production, scheduled**: low-blast-radius experiments on a schedule (weekly) with stop
   conditions tied to alarms (FIS stop conditions on CloudWatch alarms; Chaos Studio with
   permissions scoped to targets).
4. **Game days** for larger scenarios quarterly.

## Steps
1. Define experiment templates as code (FIS templates, Chaos Studio experiments, Chaos Mesh CRDs)
   in the service repo.
2. Each template: hypothesis, steady-state metrics, fault, scope, duration, stop conditions.
3. Wire into pipelines with the load generator; collect results as artefacts.
4. Track pass/fail trend per service; new failure = regression ticket.

## Gotchas
- Experiments without automated stop conditions in production.
- Test environments too small to reproduce real failure modes (single replica).
- Results not reviewed; the suite becomes noise.

## Verify
- [ ] Pipeline fails on a deliberately removed timeout (proves the suite detects regressions).
