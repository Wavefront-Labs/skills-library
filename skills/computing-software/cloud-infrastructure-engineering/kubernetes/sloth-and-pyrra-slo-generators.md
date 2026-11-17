---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sloth-and-pyrra-slo-generators
name: sloth-and-pyrra-slo-generators
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, slo, sloth, pyrra, burn-rate, prometheus, prometheusrule]
level: practitioner
status: docs-checked
description: "Generate SLO recording rules and multi-window burn-rate alerts from short specs with Sloth or Pyrra on Kubernetes, and validate the generated PrometheusRules."
sources: ["https://sloth.dev/", "https://sloth.dev/introduction/", "https://sloth.dev/usage/cli/", "https://github.com/slok/sloth", "https://github.com/pyrra-dev/pyrra", "https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sloth and Pyrra SLO generators

Hand-written multi-window, multi-burn-rate alerts are long and error-prone. Both tools take an SLI and an
objective and generate the recording rules and alerts.

## Sloth
Default (CLI) spec:
```yaml
version: "prometheus/v1"
service: "checkout"
labels: {team: payments}
slos:
  - name: "requests-availability"
    objective: 99.9
    sli:
      events:
        error_query: sum(rate(http_requests_total{job="checkout",code=~"5.."}[{{.window}}]))
        total_query: sum(rate(http_requests_total{job="checkout"}[{{.window}}]))
    alerting:
      name: "CheckoutAvailability"
      page_alert:
        labels: {severity: "page"}
      ticket_alert:
        labels: {severity: "ticket"}
```
```bash
sloth generate -i checkout-slo.yaml -o checkout-rules.yaml
```
`generate` detects the spec type: the default spec produces vanilla Prometheus rules (deploy them like any
rule file, for example from a ConfigMap if you do not run the Prometheus Operator); a Kubernetes spec
produces Prometheus Operator PrometheusRule objects and needs those CRDs in the cluster. If the input and
output are directories, Sloth discovers SLOs recursively (useful in CI). By default it optimises
long-window (30 day) rules at some cost in precision; `--disable-optimized-rules` turns that off.
`{{.window}}` is the placeholder Sloth replaces in each query for every window it needs. Generated series
include `slo:sli_error:ratio_rate5m` with `sloth_service` and `sloth_slo` labels.
Check the Sloth docs for the Kubernetes spec and controller before relying on them.

## Pyrra
```yaml
apiVersion: pyrra.dev/v1alpha1
kind: ServiceLevelObjective
metadata: {name: checkout-availability, namespace: shop, labels: {prometheus: k8s, role: alert-rules}}
spec:
  target: "99.9"
  window: 2w
  indicator:
    ratio:
      errors: {metric: 'http_requests_total{job="checkout",code=~"5.."}'}
      total:  {metric: 'http_requests_total{job="checkout"}'}
```
Pyrra takes **counter metric selectors**, not rate expressions; it builds the rates. Run with the
`kubernetes` argument, Pyrra watches ServiceLevelObjectives and creates PrometheusRule objects that the
Prometheus Operator picks up; with `--config-map-mode=true` it works without the operator. The UI shows
SLOs and their budget.

## Choosing
- Sloth: CLI-first, fits GitOps rule generation in CI.
- Pyrra: has a UI for teams and a simple ratio spec.

## Gotchas
- PrometheusRule labels must match the Prometheus `ruleSelector`, or rules are never loaded.
- Low-traffic services: burn-rate alerts flap on a handful of errors; add a minimum request-rate condition
  or use longer windows.
- Changing the objective changes the budget view; record the change in the SLO doc.

## Verify
```bash
kubectl get prometheusrules -n shop
promtool check rules checkout-rules.yaml
# in Prometheus: slo:sli_error:ratio_rate5m{sloth_service="checkout"} (Sloth) exists
```

## Checked
2026-10-28. Confirmed: the `prometheus/v1` spec, `error_query`/`total_query`, `{{.window}}`,
`page_alert`/`ticket_alert`, `sloth generate -i ... -o ...`, spec-type detection, directory discovery,
`--disable-optimized-rules`, `slo:sli_error:ratio_rate5m` and the `sloth_service`/`sloth_slo` labels
against the Sloth README, introduction and CLI pages; the Pyrra apiVersion, kind, labels, `target`,
`window`, `ratio.errors/total.metric` form, operator mode and `--config-map-mode` against the Pyrra README;
the burn-rate method against the Google SRE workbook. Removed: the `PrometheusServiceLevel` CRD example and
its camelCase fields, `sloth validate`, the Grafana dashboard id, the window list, "plugin SLIs", Pyrra
`latency` and `bool_gauge` indicator claims, and the `4w` window example (not on the pages read).
Method: documentation only; no commands were run.
