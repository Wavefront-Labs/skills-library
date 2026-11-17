---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataflow-cost-optimization-and-resource-usage
name: dataflow-cost-optimization-and-resource-usage
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataflow, dataflow-cost-optimization, dataflow-resource-usage, flexrs, streaming-engine]
level: advanced
status: docs-checked
description: "Cut Dataflow spend: read the job cost and resource metrics, choose machine types, Streaming Engine vs at-least-once mode, FlexRS for batch, autoscaling caps and shuffle choices."
sources: ["https://cloud.google.com/dataflow/docs/optimize-costs", "https://cloud.google.com/dataflow/docs/guides/flexrs", "https://cloud.google.com/dataflow/docs/guides/streaming-modes", "https://cloud.google.com/dataflow/pricing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataflow cost optimisation

## 1. See where money goes
- The **Cost** page in the Dataflow monitoring interface shows the estimated cost of jobs; it can differ from the actual cost (for example contractual discounts).
- Export Cloud Billing data to BigQuery for cost analysis, and create monitoring alerts when a job exceeds a threshold.
- Use Metrics Explorer and the job monitoring interface to find slow or stuck stages; Cloud Profiler helps with CPU-intensive code.

## 2. Levers
| Lever | When |
|---|---|
| **FlexRS** (`--flexrs_goal=COST_OPTIMIZED`) | Batch jobs that are not time-critical: the job is queued and starts within six hours; uses a mix of preemptible and regular VMs and Dataflow Shuffle |
| Right machine type (`--worker_machine_type`) | Use the smallest machine type that fits; pick machine families to match CPU- or memory-bound work |
| `--max_num_workers` / `--num_workers` | Cap autoscaling to limit cost; set an initial worker count if you know it |
| Streaming **at-least-once** mode (`--dataflow_service_options=streaming_mode_at_least_once`) | Workloads that tolerate duplicates; can significantly reduce cost and latency; enables Streaming Engine with resource-based billing |
| Streaming Engine | Recommended for streaming jobs |
| Dataflow Shuffle | Batch jobs use it by default; keep it on |
| `max_workflow_runtime_walltime_seconds` service option | Stop jobs that run longer than expected |

## 3. Pipeline-level savings
- Filter and project early; combine before GroupByKey (`Combine.perKey`), avoid fat side inputs.
- Fix hot keys (`.withHotKeyFanout`) instead of adding workers.
- In at-least-once streaming mode, BigQueryIO `FILE_LOADS` is incompatible: use the `STORAGE_API_AT_LEAST_ONCE` write method or stay in exactly-once mode.
- Avoid running many very small jobs; fewer jobs over larger datasets avoid repeated worker start-up cost.

## Gotchas
- FlexRS supports batch only, does not support GPUs or Compute Engine reservations, and takes a concurrent-job quota while queued; make sure you have preemptible CPU quota.
- Per-element logging in high-volume pipelines hurts performance and is subject to logging limits.

## Verify
- [ ] Cost per run (Cost page or billing export) drops after the change with the same output row counts; test changes on a subset of data first.

## Checked
2026-10-27. Confirmed against Dataflow optimize-costs, FlexRS and streaming-modes pages: Cost page, billing export, FlexRS goal flags and six-hour scheduling window, batch only, no GPUs, preemptible quota, Shuffle default, max/initial workers options, at-least-once service option and its Streaming Engine resource-based billing requirement, FILE_LOADS incompatibility, max_workflow_runtime_walltime_seconds. Removed: all pricing and discount statements (see the Dataflow pricing page), job-label attribution, metric names, machine-family names, --disk_size_gb advice, vertical autoscaling claim. The hot-key fanout transform names were confirmed on the common-errors page.
Method: documentation only; no commands were run.
