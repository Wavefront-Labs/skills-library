---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slo-sli-design
name: slo-sli-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, slo, sli, slo-design, sli-specification, sli-implementation, critical-user-journeys, cuj, user-journey, measurement-point, load-balancer-logs, synthetic-monitoring, client-side-telemetry, latency-threshold, percentile, histogram-buckets, availability-sli, freshness-sli, correctness-sli, coverage-sli, slo-document]
level: advanced
status: docs-checked
description: "Design SLIs and SLOs from critical user journeys: SLI specification vs implementation, where to measure, starter SLOs from data, and pipeline SLI types."
sources: ["https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLO and SLI design

**Goal:** a small set of SLIs that reflect user experience, each with a written specification, an implementation and a target derived from measured data.

Budget math, error-budget policy and burn-rate alerting live in `computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets`. This skill is the design work before them.

## 1. Start from critical user journeys
A critical user journey is a sequence of tasks that is a core part of a user's experience and an essential aspect of the service (for shopping: search for a product, add to cart, complete a purchase). Write SLOs in terms of user-centric actions. Journeys rarely map onto existing SLIs; once you can measure a journey event (by joining log events, JavaScript probing or client-side instrumentation) it becomes just another SLI.

## 2. Specification, then implementation
- SLI specification: the assessment of service outcome that matters to users, independent of how it is measured. Example: ratio of home page requests that loaded in < 100 ms.
- SLI implementation: the specification plus a way to measure it. One specification can have several implementations with different quality, coverage and cost:
  - Server log latency column: misses requests that fail to reach the backend.
  - Probers running JavaScript in a browser on a VM: catch requests that cannot reach your network but may miss issues affecting only a subset of users.
  - Instrumentation in the page JavaScript reporting to a telemetry service: closest to user experience, but needs code changes and its own reliable recording infrastructure.
- Prefer SLIs of the form good events / valid events: 0% means nothing works, 100% means nothing is broken, and error budget = 100% minus the SLO.

## 3. Where to measure
Candidate sources named by the Workbook: application server logs, load balancer monitoring, black-box monitoring, client-side instrumentation. For first SLIs choose what needs the least engineering work (if logs exist and probes would take weeks, use the logs). The Workbook's example uses load balancer metrics because they are already available and closer to the user than application logs.

## 4. SLI types by service shape
- Request-driven: availability (proportion of successful requests), latency (proportion faster than a threshold), quality (proportion of responses served undegraded).
- Pipeline: freshness (proportion of data updated more recently than a threshold; ideally counted per user access), correctness (proportion of input records producing the correct output), coverage (batch: proportion of jobs processing above a target amount of data; streaming: proportion of records processed within a window).
- Storage: durability, the proportion of written records that can be read. Beware that the data the user wants may be a small part of what is stored.
- Choose a small number (five or fewer) of SLI types for the most critical functionality.
- Freshness implementations: periodic query counting fresh vs total records (treats every stale record equally), or clients check a watermark on each request and increment counters (correlates better with user experience).
- Correctness implementations: inject data with known outputs and count matches, or sample input/output pairs and verify with an independent method. Curated test data must be representative of real data.

## 5. Starter SLOs from data
Measure the SLI over a period (the Workbook example uses four weeks), then round down to manageable numbers (two significant figures of availability, latency to about 50 ms). Example: 97.123% successful requests became a 97% availability SLO, and p90 432 ms became "90% of requests < 450 ms". Treat these as a starting point to refine.

## 6. Different classes of request
Do not give every request the same SLO. Bucket by adding labels to SLIs and applying different SLOs per label, for example by customer tier (premium 99.99% vs free 99.9% in the Workbook's table) or by expected responsiveness (interactive requests that block page load vs others).

## 7. Revisit
If outages or ticket spikes are not captured by any SLI, or SLO misses do not map to user-facing issues, the SLO lacks coverage. Change the SLO target, or change the implementation: measure closer to the user (load balancer or client instead of server), or capture more interactions (a health-check that exercises more functionality instead of a simple GET).

## Document
Record the SLO details: objectives and SLI implementations (the Workbook includes an example SLO document).

## Verify
- [ ] Each SLI traces to a named user journey.
- [ ] Each has a written specification, an implementation and its known blind spots.
- [ ] Starting targets came from measured data over a stated period.

## Checked
Method: docs-checked 2026-11-09 against the SRE Workbook chapter "Implementing SLOs" (read in full). The Hidalgo book and OpenSLO specification were not read and were dropped as sources. Removed the measurement-point table of RUM/synthetic trade-offs, the "target below what you achieved" rule, the histogram bucket alignment rule, the composite-SLO and dependency claims, the OpenSLO/Sloth/Pyrra guidance, the 3-SLOs-per-service smell and the gotchas, none of which are stated on that page.
