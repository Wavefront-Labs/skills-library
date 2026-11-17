---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.nalsd-single-machine-design
name: nalsd-single-machine-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [single-machine-design, is-it-possible, nalsd, system-design, back-of-the-envelope]
level: advanced
status: docs-checked
description: "NALSD's 'is it possible?': design on one machine, check storage, IOPS and RAM against the requirements, and find the bottleneck that forces distribution."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-machine design first

Workbook NALSD: the first question is "Is it possible?": ignoring RAM, CPU and network limits, what design would
satisfy the requirements? Start with the entire application on one computer, then test the numbers. The step is not
wasted even when the design fails: it shows how to reason about the system's constraints.

## Steps
1. **Algorithm**: describe the simplest correct approach. Workbook example: build a data structure on the one
   machine as logs arrive (an SQL database indexed on `query_id` and `search_term`), join the query log and click
   log on `query_id`, group by `search_term` to report click-through rate.
2. **Resource check**: size each record, then compute volume and IO. Workbook figures for its example:
   - Volume: 86.4 TB/day, rounded up to about 100 TB for one day of log data with index overhead.
   - IOPS: a common 4 TB HDD might sustain 200 IOPS; at one disk write per log entry,
     `(5 x 10^5 queries/s) / (200 IOPS/disk) = 2,500 disks`. Batching 10:1 still leaves several hundred HDDs.
   - RAM: with a standard machine of 16 cores, 64 GB RAM and 1 Gbps, holding 100 TB in RAM needs
     `100 TB / 64 GB = 1,563 machines`.
3. **Identify the bottleneck**: here, IOPS and capacity. The Workbook chose to skip other media such as SSD for
   simplicity.
4. **Evaluate failure**: ask what happens when each component fails. A single machine has many single points of
   failure (CPU, memory, storage, power, network, cooling), so even a power cycle would hurt the SLOs.
5. **Decide**: if the one-machine design fails, the bottleneck says what to distribute (see
   `nalsd-distributed-design-iteration`).

## Why this matters
- Prevents premature distribution complexity.
- Makes the reason for each distributed component explicit.

## Gotchas
- Use realistic hardware numbers (see `latency-numbers-and-resource-estimation`), not marketing peaks.
- A single machine is a thinking tool; the chapter rejects it on availability grounds regardless of the numbers.

## Verify
- [ ] One-machine design written with a resource table and the identified bottleneck(s).

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design": "Is it possible?" question, the one-machine SQL design, 86.4 TB/day rounded to about 100 TB, 200 IOPS per 4 TB HDD, 2,500 disks, 10:1 batching, 16 cores/64 GB/1 Gbps machine, 1,563 machines, single-points-of-failure evaluation.
Removed: the invented 64-core/512 GB machine, 55 GB working set, 40 MB/s ingest and CPU cost figures.
Method: documentation only; no commands were run.
