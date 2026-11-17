---
id: computing-software.cloud-infrastructure-engineering.metallb.alert-rules
name: alert-rules
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, alert-rules, prometheusrule, stale-config, pool-exhausted, bgp-session-down, extraalerts]
level: practitioner
status: docs-checked
description: "Prometheus alert rules for MetalLB: stale config, config not loaded, pool exhausted, BGP session down; Helm PrometheusRule toggle and FRR-K8s metric prefix."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/prometheus-metrics/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alert rules

Alert on stale config, failed config load, exhausted pools and down BGP sessions. The manifests include no rules. Helm can emit a `PrometheusRule` when `prometheus.prometheusRule.enabled` is true (default false; needs the Prometheus Operator CRD), and offers per-rule toggles plus `extraAlerts` there. For manifest installs, write your own or adapt the chart template `charts/metallb/templates/prometheusrules.yaml`.

Equivalent expressions (each `for: 1m`):
```yaml
groups:
  - name: metallb
    rules:
      - alert: MetalLBStaleConfig
        expr: metallb_k8s_client_config_stale_bool == 1
        labels: {severity: warning}
      - alert: MetalLBConfigNotLoaded
        expr: metallb_k8s_client_config_loaded_bool == 0
        labels: {severity: critical}
      - alert: MetalLBAddressPoolExhausted
        expr: metallb_allocator_addresses_in_use_total >= metallb_allocator_addresses_total
        labels: {severity: critical}
      - alert: MetalLBBGPSessionDown
        expr: metallb_bgp_session_up == 0
        labels: {severity: critical}
```
Add `for: 1m` under each alert (omitted above for brevity) as in the docs.

In FRR-K8s mode (the default) BGP session metrics use the `frrk8s_` prefix, e.g. `frrk8s_bgp_session_up`, unless you relabel (`computing-software.cloud-infrastructure-engineering.metallb.metrics-relabeling`). Adjust the BGP expression to the names you scrape.

## Checked

2026-11-04. Confirmed against the MetalLB Prometheus Metrics page (sample alert rules, frrk8s_ prefix note, Helm extraAlerts) and the Installation page (Prometheus manifests carry no alert rules; prometheus.prometheusRule.enabled defaults to false and needs the PrometheusRule CRD; chart rule template path). Removed the generic Verify line.

Method: documentation only; no commands were run.
