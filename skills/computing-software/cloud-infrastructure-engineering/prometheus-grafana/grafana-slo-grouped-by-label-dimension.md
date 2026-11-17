---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-slo-grouped-by-label-dimension
name: grafana-slo-grouped-by-label-dimension
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-slo, grafana-slo-group-by, slo-dimensions, multi-dimensional-slo, cardinality]
level: advanced
status: docs-checked
description: "Decide when to use multi-dimensional Grafana SLOs (one objective per label value), with the cost, traffic and alert-routing trade-offs the docs describe."
sources: ["https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/create/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/best-practices/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/introduction/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grouped (multi-dimensional) SLOs

**Goal:** see that one region or tier is burning budget even when the aggregate SLO looks fine.

## What the docs say
- Grafana SLO supports multidimensional SLIs: they let you filter consumption and set alerts for each dimension (for example every cluster or probe). Decide between aggregated, multidimensional, or both.
- The docs have a multidimensional example for the Ratio query option and one for probes using a classic histogram; follow those for the exact query shape and field names.
- An SLI query must still be a success ratio (numerator / denominator) between 0 and 1.

## Cost and limits
- Each SLO creates 10 to 12 Prometheus recording rules with at least one series per rule; multidimensional SLIs create multiple series per recording rule. Each generated series produces one data point every 60 seconds (1 DPM) and is billed as metrics usage. See the vendor's metrics pricing page for figures.
- Default limit: 70 SLOs per Grafana instance (raise through a support request).
- So group only on labels with a small, bounded set of values.

## Traffic and alerts
- Target services with good traffic. Low traffic gives noisy alerts and disproportionate irregularities, which applies per group too.
- Minimum Failures (an advanced setting) sets the number of failures needed before an alert fires. It applies to all alerting windows of the SLO, the smallest being 1 hour.
- Alert labels route notifications; SLO labels group and filter SLOs. Keep labels limited. Send fast-burn alerts to on-call and slow-burn alerts to the team in working hours.
- Fast-burn alerts evaluate short periods (budget used over minutes or hours); slow-burn alerts longer ones (hours or days).

## Checked
2026-11-08. Confirmed in the Grafana SLO introduction (recording rules per SLO, 1 DPM, 70 SLO limit), best-practices (multidimensional SLIs, traffic, Minimum Failures, labels, alert routing) and Create SLOs pages (ratio requirement, fast and slow burn). Removed: the Group by UI field description, the dashboard group variable, the sum by example, the dimension table (region yes, customer ID no) and the "tens of groups" guidance, none of which the pages state; the sre.google source (not read in full) and the Verify checklist.
Method: documentation only; no commands were run.
