---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.data-pipeline-slos
name: data-pipeline-slos
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [pipeline-slos, freshness-correctness-slo, data-freshness, data-correctness, data-pipelines, slo]
level: practitioner
status: docs-checked
description: "Define pipeline SLOs for freshness, correctness, data isolation and end-to-end measurement; use golden data, measure the sum of stages, and plan for dependency failure."
sources: ["https://sre.google/workbook/data-processing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data pipeline SLOs

SRE Workbook, Data Processing Pipelines: pipeline SLOs are about the data your customers consume. Sections:
data freshness, data correctness, data isolation/load balancing, end-to-end measurement, plus planning for
dependency failure.

## SLO forms (Workbook)
- **Freshness**: "X% of data processed in Y time"; "the oldest data is no older than Y"; or "the pipeline job
  has completed successfully within Y". Example from the book: 99% of user actions reflected in the scoreboard
  within 30 minutes.
- **Correctness**: where no predefined correct output exists, generate "golden data" (for example from test
  accounts) and compare expected and actual output with threshold alerts; or set backward-looking targets such
  as a maximum share of incorrect invoices per quarter, or hours of bad data served.
- **Isolation**: tighter SLOs for high-priority data need it processed first when resources are constrained,
  for example via separate queues or jobs.
- **End-to-end**: measure the sum of stages, not each stage alone; per-stage correctness can miss corruption
  between stages.

## Instrumentation
Export newest-processed data age (watermark lag) and validated/failed record counts, and reconcile counts per
partition between source and sink (see `out-of-band-data-validation`).

## Alerting
Alert on SLO burn (lag rising past threshold, completeness dropping), not on individual job failures.
A failed job that retries and still meets freshness should not page. The Workbook recommends notifications
when you are in danger of exceeding your error budget.

## Gotchas
- "Job succeeded" is not freshness: a job can succeed on empty input.
- End-to-end measurement beats per-stage measurement for SLOs (Workbook); per-stage metrics are for debugging.
- Define what happens to late data (allowed lateness) or freshness looks perfect while data is missing.

## Verify
- [ ] Watermark and validation metrics exported for every pipeline with an SLO.
- [ ] A deliberately delayed input triggers the freshness alert.

## Checked
2026-11-01. Confirmed in the SRE Workbook Data Processing Pipelines chapter (freshness formats and the 30-minute example, golden data, backward-looking correctness, isolation, end-to-end measurement, error budget notifications). Removed: the invented example SLO table (completeness, throughput and batch deadlines), metric names, the PromQL alert, and the good/total freshness recipe. The implementing-slos source was not read.
Method: documentation only; no commands were run.
