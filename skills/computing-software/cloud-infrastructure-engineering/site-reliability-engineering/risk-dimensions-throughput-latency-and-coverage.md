---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.risk-dimensions-throughput-latency-and-coverage
name: risk-dimensions-throughput-latency-and-coverage
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, embracing-risk, risk-dimensions, latency-tolerance, throughput, infrastructure-services]
level: advanced
status: docs-checked
description: "Break service risk into dimensions (availability, latency, throughput, durability, correctness, freshness) and give different client classes different service levels."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/sre-book/service-level-objectives/", "https://sre.google/workbook/data-processing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Risk dimensions

**Goal:** stop treating "reliability" as one number; choose indicators per system type and levels of
service per client class.

## Dimensions by system type (SRE Book, Service Level Objectives)
- User-facing serving systems: availability, latency, throughput.
- Storage systems: latency, availability, durability (is the data still there when needed).
- Big data pipelines: throughput and end-to-end latency (some also per-stage latency targets). The Workbook
  data processing chapter adds data freshness SLOs for pipelines.
- All systems: correctness (right answer, right data, right analysis). The book says it is often a property
  of the data rather than the infrastructure, so usually not an SRE responsibility to meet.
- Use a handful of representative indicators, not every metric you can track.

## Infrastructure services example (SRE Book, Embracing Risk, Bigtable)
- Services serving users directly from Bigtable need low latency and high reliability; teams using it for
  offline analysis (for example MapReduce) care more about throughput than reliability.
- Low-latency users want request queues almost always empty (inefficient queuing often causes high tail
  latency); throughput users want queues never empty so the system never idles.
- Making everything ultra-reliable is usually far too expensive. Instead partition the infrastructure into
  independent levels of service: low-latency clusters with substantial slack capacity for reduced
  contention and more redundancy, and throughput clusters run hot with less redundancy.
- Deliver explicitly delineated levels of service so clients can make their own risk and cost trade-offs
  and the cost difference is exposed to them. Example in the book: critical privacy data in a globally
  consistent store, optional data in a cheaper, less fresh, eventually consistent store.

## Applying it
1. List client classes and what each needs per dimension.
2. Set targets only for dimensions each class cares about.
3. Offer separate service levels when needs conflict, rather than one compromise target.

## Verify
- [ ] The SLO document lists dimensions per client class; conflicting needs are tiered.

## Checked
2026-11-01. Confirmed against the SRE Book Embracing Risk (Bigtable and levels of service), Service Level
Objectives (indicators by system type) and the Workbook data processing chapter (freshness). Removed: the
example SLI figures (300 ms, 10 min), the Coverage dimension, which no fetched page lists as a dimension,
and pricing and quota claims.
Method: documentation only; no commands were run.
