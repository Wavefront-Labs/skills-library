---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.moire-load-and-staggered-schedules
name: moire-load-and-staggered-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [moire-load-pattern, staggered-schedules, thundering-herd, cron, data-pipelines, jitter]
level: practitioner
status: docs-checked
description: "Find and fix Moire load patterns and thundering herds from periodic pipelines: plot shared-resource usage, stagger schedules, add retry jitter, and prefer continuous processing."
sources: ["https://sre.google/sre-book/data-processing-pipelines/", "https://sre.google/sre-book/distributed-periodic-scheduling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moire load patterns and staggered schedules

SRE Book "Data Processing Pipelines":
- **Thundering herd**: in a large periodic pipeline, thousands of workers can start work at the same moment each
  cycle. Too many workers, misconfiguration or faulty retry logic overwhelm the servers, shared cluster services and
  network. Without retry logic, dropped work causes correctness problems; naive retry compounds the overload.
  Adding more workers when a job runs late makes it worse.
- **Moire load pattern**: two or more pipelines run at once and their execution sequences occasionally overlap, so
  they simultaneously consume a shared resource. It can occur in continuous pipelines too, though less often when
  load arrives evenly. It is most apparent in plots of pipeline usage of a shared resource; the book's stacked plot
  shows the on-call pain at the aggregate peak.

## Find it
- Plot the usage of each shared dependency by pipeline, stacked, and look for sharp periodic peaks.
- List all schedules and plot a histogram of start times; any start time with many jobs is a herd.

## Spread it
- Deterministic offsets: derive the start minute from a hash of the job name.
- Startup jitter inside jobs, and jitter on retries, so failed jobs do not retry at the same instant.
- Concurrency limits at the shared resource, so only K pipelines use it at once.
- Do not respond to a slow job by adding workers.
- The book's remedy for data that is or will become continuous: use continuous processing (Google's Workflow)
  instead of a periodic pipeline.

## Gotchas
- Spreading jobs changes when outputs are ready; check downstream freshness SLOs.

## Verify
- [ ] No more than N jobs start in any single minute (report from schedules).
- [ ] Shared dependency peak-to-mean ratio drops after staggering.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Data Processing Pipelines": thundering herd and Moire load pattern definitions, retry correctness issue, adding workers amplifying the problem, continuous pipelines as remedy.
Removed: the PromQL queries, Python hashing sketch, Jenkins `H` syntax and Airflow pool lines (not read), the claim that humans choose round times, and the Jenkins source.
Method: documentation only; no commands were run.
