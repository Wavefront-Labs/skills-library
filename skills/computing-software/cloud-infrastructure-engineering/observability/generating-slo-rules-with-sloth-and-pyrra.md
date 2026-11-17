---
id: computing-software.cloud-infrastructure-engineering.observability.generating-slo-rules-with-sloth-and-pyrra
name: generating-slo-rules-with-sloth-and-pyrra
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [slo, sloth-usage, pyrra-usage, slo-alerts-at-scale, generated-slo-rules, dependency-slo-alerting, alerting-on-dependencies, prometheus-rules]
level: practitioner
status: draft
description: "Generate multiwindow burn-rate recording and alert rules for many services with Sloth or Pyrra, and decide how (not) to alert on dependencies' SLOs."
sources: ["https://sloth.dev/", "https://github.com/pyrra-dev/pyrra", "https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating SLO rules with Sloth and Pyrra

Hand-writing 4 burn windows x recording rules x services doesn't scale. Generate them from a spec.

## Sloth
```yaml
# slos/checkout.yml
version: prometheus/v1
service: checkout
labels: {team: payments}
slos:
  - name: requests-availability
    objective: 99.9
    sli:
      events:
        error_query: sum(rate(http_requests_total{job="checkout",code=~"5.."}[{{.window}}]))
        total_query: sum(rate(http_requests_total{job="checkout"}[{{.window}}]))
    alerting:
      name: CheckoutAvailability
      page_alert: {labels: {severity: page}}
      ticket_alert: {labels: {severity: ticket}}
```
```bash
sloth generate -i slos/ -o rules/slo-generated.yml        # CI step; commit or deploy the output
```
Kubernetes: `PrometheusServiceLevel` CRD with the Sloth controller, which emits PrometheusRule objects.
Output: `slo:sli_error:ratio_rate5m..30d`, `slo:error_budget:ratio`, `slo:objective:ratio`, plus page/ticket
alerts using the Workbook's windows (1h/5m, 6h/30m, 3d/6h).

## Pyrra
```yaml
apiVersion: pyrra.dev/v1alpha1
kind: ServiceLevelObjective
metadata: {name: checkout-errors, namespace: monitoring, labels: {prometheus: k8s, role: alert-rules}}
spec:
  target: "99.9"
  window: 4w
  indicator:
    ratio:
      errors: {metric: 'http_requests_total{job="checkout",code=~"5.."}'}
      total: {metric: 'http_requests_total{job="checkout"}'}
```
Pyrra also serves a UI with budget burn graphs; it generates the rules and alerts (`ErrorBudgetBurn`).

## Alerting on dependencies
From the Workbook: don't page service A's on-call because dependency B burns *its* budget. A's SLO already
includes B's impact on A's users. Instead:
- Each dependency owner alerts on their own SLO.
- A dashboards B's SLO for context, and may use B's alert as an inhibition source to avoid A's team chasing it.
- Only if A has a mitigation it controls (failover, feature flag) does an A-side alert on B make sense.

## Verify
- [ ] `promtool check rules` on generated output in CI.
- [ ] Generated alerts fire in `promtool test rules` with a synthetic full outage.
