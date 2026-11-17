---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.pipeline-development-lifecycle
name: pipeline-development-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [pipeline-development-lifecycle, pipeline-prototyping, data-pipelines, canarying, staging-environments, release-engineering]
level: practitioner
status: docs-checked
description: "Move a data pipeline change from prototype through 1% dry run, staging, canary, partial deployment and production, following the SRE Workbook lifecycle."
sources: ["https://sre.google/workbook/data-processing/", "https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline development lifecycle

The SRE Workbook "Data Processing Pipelines" chapter says the lifecycle of a pipeline, or of a change to one, is not too different from other systems, and walks a release through these stages.

## Stages
| Stage | What the Workbook says |
|---|---|
| Prototyping | Verify semantics and that you can express the business logic. Choosing a language or programming model (for example Dataflow versus MapReduce, batch versus streaming) happens here. For a feature added to an existing pipeline, add the code and run unit tests at this stage. |
| 1% dry run | Run a small setup on the full stack using production data, for example a 1% dry run in a nonproduction environment. Scale up gradually and track performance for bottlenecks. Once the product has launched to customers, run performance tests. |
| Staging | Preproduction data should be as close to production as possible: a full copy or at least a representative subset. Let data flow end to end, and run an A/B comparison of newly generated data against previously generated known-good data using unit and integration tests. |
| Canarying | Partially deploy the pipeline and monitor the results. Canarying is tied to the entire pipeline, not one process. Process the same real production data as the live pipeline but skip writes to production storage (two-phase mutation can help), then compare canary results with the live pipeline. |
| Partial deployment | Useful for a major feature launch that could change performance or resource use. Implement it as a flag or config option that accepts an allowed subset of data: start with one or two accounts, then ramp up (the Workbook example is about 1%, 10%, 50%, then 100%). |
| Production | Be able to restore quickly to a known good state (for example roll back binaries) and mark potentially broken data as bad: replace it with data from a previous backup version, make sure no jobs read it, and reprocess if necessary. |

## Points to carry into practice
- Unit tests will not catch all pipeline issues, so end-to-end data flow in staging matters.
- You often have to wait for the complete cycle of processing to finish before customer-impacting issues show up in a canary.
- Gradual per-task or per-region canary progression is not always possible: pipelines using replicated data (the Workbook names Dataproc and Dataflow) support regional endpoints and cannot reload one cell in isolation. Roll out to a small percentage of data first, or roll out in dry-run mode.
- Verify a canary or preproduction run with the same metrics you use to track SLOs; this verification lends itself to automation.
- Avoid promoting a corrupt set of data to low-latency frontends. Partial deployments can fail because input data is incorrect or delayed, processing has a bug, or final storage has an error.
- Related skills: `canarying-batch-and-non-interactive-systems`, `idempotent-and-two-phase-mutations`, `data-pipeline-slos`.

## Checked
- 2026-11-08: stage names and their descriptions, the 1%/10%/50%/100% ramp example, the regional-endpoint limit and the rollback and bad-data handling were confirmed on the Workbook "Data Processing Pipelines" page ("Map Your Development Lifecycle").
- Removed: the per-stage "gate" column, the pre-production requirements list, the parameterisation and backfill-entrypoint advice, and the "quadratic costs" claim, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
