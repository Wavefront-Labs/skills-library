---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slo-document-reporting-and-review
name: slo-document-reporting-and-review
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [slo, sli, slo-document, reporting, sre]
level: practitioner
status: docs-checked
description: "Write, report on and review an SLO document following the Google SRE Workbook example: SLI table, rationale, error budget, caveats, approvers and review date."
sources: ["https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/slo-document/", "https://sre.google/sre-book/service-level-objectives/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLO document, reporting and review

## SLI choice by service type (SRE Book "Service Level Objectives")
- User-facing serving systems: availability, latency, throughput.
- Storage systems: latency, availability, durability.
- Data processing pipelines: throughput and end-to-end latency.
- The Workbook's example SLO document also uses freshness, correctness (a prober injecting synthetic data) and completeness for a score pipeline.
The Workbook says to make SLIs consistent in style (numerator, denominator, threshold) so tooling can be reused.

## Measurement point
The Workbook's example measures request SLIs at the load balancer and states the caveat: this may miss cases where user requests never reached the load balancer. Only HTTP 5XX counted as errors in that example.

## Targets
- The Workbook derives starting SLOs from measured history and rounds: availability down to two significant figures, latency up to 50 ms. Its example SLO document rounded availability down to the nearest 1% and latency up to the nearest 50 ms from a four-week measurement period.
- The SRE Book: insisting SLOs be met 100% of the time is unrealistic and undesirable; allow an error budget and track it daily or weekly, with monthly or quarterly assessments for management. Choose "just enough" SLOs; separate objectives per workload class are appropriate for heterogeneous users.
- The Workbook notes SLOs may be documented even when not strongly evidence-based, with that fact stated (the example's rationale says no attempt was made to verify correlation with user experience).

## The document (Workbook example structure)
Header (status, author, date, reviewers, approvers, approval date, revisit date); service overview and window; SLI and SLO table with SLI implementations; rationale; error budget (each objective has its own budget, 100% minus the goal); clarifications and caveats.

The implementing-SLOs chapter says the document should record the authors, reviewers (technical accuracy) and approvers (the business decision), approval and next-review dates, SLI implementation details and how the budget is calculated and consumed, and be kept somewhere other teams can review.

## Reporting
The Workbook recommends reports and dashboards giving in-time snapshots of SLO compliance, and SLI trend dashboards showing a higher-than-usual budget burn. It also suggests weekly summaries and quarterly reports.

## Review
Compare outages and ticket spikes against SLI dips: those not captured in any SLO, or SLO misses that do not map to user-facing issues, show poor SLO coverage. The Workbook says SLIs and SLOs should change over time and not be feared to refine. The review date is set in the document header.

## Verify
- [ ] The SLO document has approvers, approval date and revisit date.
- [ ] Reports and dashboards are available to other teams.

## Checked
Confirmed against the Workbook "Example SLO Document" and "Implementing SLOs" and the SRE Book "Service Level Objectives" (SLI types by system, error budget, 100% comment). Removed: the "good events / valid events" universal rule, the measurement-source pros and cons table, "slightly below history" target advice, 28/30-day window claim, the first-quarter monthly review rule and the Verify wording on tier-1 services.
Method: docs-only read of cited pages, 2026-11-08
