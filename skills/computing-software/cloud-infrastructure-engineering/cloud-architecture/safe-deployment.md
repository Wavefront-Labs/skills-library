---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.safe-deployment
name: safe-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, safe-deployment, progressive-delivery, canary-deployment, blue-green, automated-rollback]
level: practitioner
status: docs-checked
description: "Deploy safely with progressive exposure: one-box and canary stages, bake times, alarm-driven rollback, wave-based regional rollout, time windows and feature flags."
sources: ["https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/", "https://learn.microsoft.com/azure/well-architected/operational-excellence/safe-deployments", "https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe deployment practices

## Principles
- Limit the scope of each deployment. Amazon's stated objective is to prevent negative impact to multiple
  Regions at the same time and to multiple Availability Zones in one Region; production is split into
  many stages, then into single Availability Zones or cells within a Region.
- Hands-off: deployments are monitored by alarms and rolled back automatically, not by someone watching.

## Pipeline as Amazon describes it
1. **Pre-production**: code review before merge, integration tests against real APIs on real
   infrastructure in each pre-production stage, positive and negative cases, optional fuzz and short load tests.
2. **One-box stage** at the start of each production wave: one VM, one container or a small share of
   Lambda invocations. Amazon says the one box typically serves at most ten percent of requests for the
   Region or Availability Zone. One-box stages also roll back on alarms scoped to the one box, because
   its small traffic share may not trip the service-wide alarm.
3. **Rolling deployment** after the one box: typically at most 33 percent of boxes replaced at a time,
   keeping at least 66 percent of capacity healthy; some teams deploy as little as five percent at a time
   and use faster rollbacks at 33 percent.
4. **Waves**: groups of Regions of increasing size. Wave 1 targets a Region with few requests, one
   Availability Zone or cell at a time; wave 2 a Region with many requests, so new code paths get exercised.
   Amazon's sample pipeline uses three Regions in wave 3, up to 12 in wave 4, the rest in wave 5.
5. **Bake time** before promoting: the pipeline keeps watching the aggregate alarm for slow-burning
   problems. A typical pipeline waits at least one hour after each one-box stage, at least 12 hours after the
   first regional wave and two to four hours after the later waves, and can require a number of data
   points (for example 100 requests to an API). Earlier waves bake longer. Default bake times mean a
   change reaches all Regions in about four or five business days.
6. **Automatic rollback** when the high-severity alarm (fault rate, latency, CPU and similar) goes into
   alarm, including aggregate alarms across the team's services and canaries.
7. **Blockers and time windows**: the pipeline refuses to start a deployment while the aggregate alarm is
   in alarm (developers can override to recover), and allows starts only in windows chosen so on-call is
   quickly reachable; many teams exclude nights, weekends, holidays, Fridays and late afternoon.
8. **Configuration changes** (rate limits, feature flags) go through their own pipeline with the same
   automatic rollback.

## Other sources
- Azure Well-Architected: use feature flags to control exposure and roll back quickly; version build
  artifacts so you can roll back and forward; App Service staging slots support blue-green; many Azure
  database services offer point-in-time restore as a rollback aid.
- Google SRE Workbook: a canary exposes part of production traffic first; the population must receive
  enough traffic to be representative, and slower metrics such as queue depth may need more time or a larger population.

## Gotchas
- A rollback of code does not undo data changes; check what restore options your database offers.
- A small canary hides its errors inside overall traffic; evaluate canary-scoped metrics.

## Verify
- [ ] A seeded fault in a test deployment triggers automatic rollback.
- [ ] The pipeline deploys to a one-box or canary, then a low-traffic Region, then the remaining Regions.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Amazon Builders' Library article (ten percent, 33 and 66 percent, five percent, bake
times, wave sizes, blockers, time windows, configuration pipeline), the Azure safe deployments page and
the Google SRE Workbook canarying chapter. Removed as not stated there: "1-5 percent" canary sizing,
CodeDeploy, Argo Rollouts, Flagger, expand-contract migrations and deployment freezes by name.
