---
id: computing-software.data-engineering.databricks.autoscaling-and-auto-termination
name: autoscaling-and-auto-termination
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, auto-termination, autoscaling, cluster-policies, cost-control]
level: practitioner
status: docs-checked
description: "Configure Databricks autoscaling and auto termination: min/max workers, idle timeouts, job compute, and limits enforced by compute policies."
sources:
  - https://docs.databricks.com/aws/en/compute/configure#autoscaling
  - https://docs.databricks.com/aws/en/compute/configure#automatic-termination
  - https://docs.databricks.com/aws/en/admin/clusters/policy-definition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscaling and auto termination

**Goal:** compute that matches load and stops when idle, so you do not pay for empty clusters.

## Auto termination
```json
{ "autotermination_minutes": 30 }
```
- Compute terminates when the time since the last command run exceeds the inactivity period in minutes. A value of 15-60 is a sensible choice for interactive compute.
- Job compute is created for a run and goes away after it: prefer it over all-purpose compute for scheduled work.

## Autoscaling
```json
{ "autoscale": { "min_workers": 2, "max_workers": 10 } }
```
- Databricks adds and removes workers between the min and max to suit the workload; good for variable batch loads. Not available for spark-submit jobs.
- Premium-plan workspaces use optimized autoscaling (scales up from min to max in at most 2 events; on job compute scales down after 40 seconds of underutilization, on all-purpose compute after 150 seconds). Standard-plan workspaces use standard autoscaling (starts by adding 8 nodes, scales down when 90% of nodes are not busy for 10 minutes).
- Do not enable Spark Dynamic Allocation (`spark.dynamicAllocation.enabled`) on autoscaling compute.
- Autoscaling has limitations scaling down for Structured Streaming; Databricks recommends Lakeflow pipelines with enhanced autoscaling for streaming.
- Set `min_workers` to cover the steady baseline; max to a cost ceiling.

## Enforce with cluster policies
```json
{
  "autotermination_minutes": { "type": "range", "minValue": 10, "maxValue": 60, "defaultValue": 30 },
  "autoscale.max_workers": { "type": "range", "maxValue": 20 },
  "custom_tags.team": { "type": "unlimited", "isOptional": false }
}
```
Grant users only policies, not unrestricted cluster creation.

## Pools
When attaching compute to a pool, keep the requested size at or below the pool's minimum idle instances and the maximum size at or below the pool's maximum capacity (otherwise creation fails).

## Verify
Each all-purpose compute resource shows an Automatic termination value in its configuration; billing shows no compute running overnight without jobs.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: autoscaling min/max workers, optimized versus standard autoscaling behaviour and timings, no autoscaling for spark-submit, the Dynamic Allocation warning, streaming guidance, automatic termination as an inactivity period, and the policy attributes `autotermination_minutes`, `autoscale.max_workers`, `custom_tags.*` with `range`/`unlimited` and `isOptional` (compute configuration and policy definition pages).

Removed or corrected: the 'UI default is often 120' figure, the claim about idle detection ignoring background activity, the cheaper job DBU rate, and the system.compute.clusters verify step (not on the pages read). The pool sentence was replaced with the pool sizing rule from the compute configuration page.

Method: documentation only; no commands were run.
