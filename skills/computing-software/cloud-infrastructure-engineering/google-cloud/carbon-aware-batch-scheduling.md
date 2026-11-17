---
id: computing-software.cloud-infrastructure-engineering.google-cloud.carbon-aware-batch-scheduling
name: carbon-aware-batch-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sustainability, carbon-aware-batch-scheduling, time-shifting-workloads, location-shifting, cloud-batch, cloud-scheduler]
level: practitioner
status: draft
description: "Shift flexible batch work in time or location to lower-carbon grid periods using intensity signals, Cloud Scheduler, Batch and Workflows, without missing deadlines."
sources: ["https://cloud.google.com/architecture/framework/sustainability", "https://cloud.google.com/blog/topics/sustainability/how-carbon-aware-computing-reduces-emissions", "https://learn.greensoftware.foundation/carbon-awareness/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Carbon-aware batch scheduling

## What can move
- **Time-shifting**: jobs with flexible deadlines (nightly ETL with a 24 h window, ML training,
  reindexing, backups, report generation).
- **Location-shifting**: stateless compute whose data is small or replicated (rendering, CI builds,
  training on public datasets) to a region with higher CFE%.
Not: latency-sensitive serving, jobs pinned to data residency.

## Signals
- Annual region CFE% / intensity (Google region-carbon data) for location choice.
- Hourly/forecast grid intensity from third-party APIs (Electricity Maps, WattTime, national grid
  operators like UK Carbon Intensity API) for time choice. Google does not expose real-time
  per-region CFE via a public API; treat third-party data as the signal.

## Implementation pattern
1. Tag jobs with `deadline` and `allowed_regions`.
2. A Cloud Run job or Workflow runs hourly: fetch forecast intensity for allowed regions, pick the
   lowest-intensity slot before the deadline, and create/schedule the Batch job then.
   ```bash
   gcloud batch jobs submit etl-$(date +%s) --location=$BEST_REGION --config=job.json
   ```
3. Fallback: if no low-carbon slot before deadline, run at the deadline (never miss SLAs).
4. Record chosen region/time and intensity for reporting.

## Trade-offs
- Spot capacity and price vary by region and hour; combine signals (cost x carbon).
- Moving large datasets cross-region costs egress and time; prefer moving compute to data.
- Measure: Carbon Footprint (location-based) is monthly and per region/product; expect results at that granularity.

## Verify
- [ ] Monthly report shows share of deferrable compute run in low-intensity windows/regions without SLA misses.
