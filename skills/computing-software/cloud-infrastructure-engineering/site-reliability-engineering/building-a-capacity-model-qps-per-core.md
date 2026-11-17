---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.building-a-capacity-model-qps-per-core
name: building-a-capacity-model-qps-per-core
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, capacity-planning, capacity-model, qps-per-core, load-testing, resource-estimation]
level: advanced
status: docs-checked
description: "Build a capacity model from load tests and production data: QPS per core and per instance, resource ratios, headroom, and converting demand forecasts into instance counts."
sources: ["https://sre.google/sre-book/software-engineering-in-sre/", "https://sre.google/sre-book/addressing-cascading-failures/", "https://sre.google/workbook/managing-load/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a capacity model

**Goal:** turn "expected traffic next quarter" into a defensible number of instances/cores.

## 1. Find the per-unit capacity
- Couple capacity planning with performance testing to find the load at which the service fails (SRE Book, Addressing Cascading Failures). Load test with a production-like traffic mix until the SLO breaks, and record the QPS and resource usage at that point.
- Cross-check with production: plot QPS per instance vs CPU per instance over weeks and fit the slope (requests per CPU-second is QPS per core).
- Identify the **limiting resource** (CPU, memory, connections, downstream quota). Capacity is set by whichever hits its limit first.

## 2. Model
```
peak_qps_forecast         = Q
qps_per_core_at_slo       = C   (from tests, with a safety margin you choose)
cores_needed              = Q / C
instances                 = ceil(cores_needed / cores_per_instance)
with redundancy (N+2)     = instances + 2 per failure domain plan
with headroom for growth  = x (1 + growth_buffer)
```
Example: Q = 12,000 QPS, C = 150 QPS/core, 4 cores per instance: 80 cores, 20 instances, +2 for N+2 = 22; per-region split if serving from 3 regions with one down: each surviving region carries 50%, so each region needs capacity for 6,000 QPS.

## 3. Keep it honest
- Re-measure C after major releases (efficiency regressions are common).
- Track model vs actual utilisation monthly; adjust.
- Separate organic growth from launches (inorganic demand) in the forecast.
- Include non-QPS drivers: batch jobs, caches warming, failover load.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Addressing Cascading Failures (capacity planning coupled
with performance testing to find the breaking point; N + 2 example) and Software Engineering in SRE (capacity
planning is a never-ending cycle). The worked example is arithmetic. Removed: the PromQL query and the 80% margin
figure; sources not read (Handling Overload, Service Best Practices) were dropped.
Method: documentation only; no commands were run.

## Verify
- [ ] Capacity sheet lists C with test date and version, limiting resource, forecast source, redundancy plan; production peak utilisation stays below the planned headroom.
