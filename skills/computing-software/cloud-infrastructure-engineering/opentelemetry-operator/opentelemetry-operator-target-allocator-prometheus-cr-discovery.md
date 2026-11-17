---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-prometheus-cr-discovery
name: opentelemetry-operator-target-allocator-prometheus-cr-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, prometheus-cr, servicemonitor-selector, podmonitor-selector, scrapeclasses, allownamespaces]
level: advanced
status: docs-checked
description: "Turn on ServiceMonitor and PodMonitor discovery with prometheusCR, set the mandatory v1beta1 selectors, scope namespaces, and use scrapeClasses."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/prometheus-cr.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus CR discovery and selectors

Prometheus does not need to be installed, but the ServiceMonitor and PodMonitor CRDs must be (they ship with prometheus-operator and can be installed standalone, for instance from the kube-prometheus-stack chart CRDs). Enable discovery with `spec.targetAllocator.prometheusCR.enabled: true`. The TA presents what it finds on its `/scrape_configs` and `/jobs` endpoints.

```yaml
targetAllocator:
  enabled: true
  serviceAccount: everything-prometheus-operator-needs
  prometheusCR:
    enabled: true
    serviceMonitorSelector: {}
    podMonitorSelector: {}
    scrapeClasses: []
```

In v1beta1 a `serviceMonitorSelector` and `podMonitorSelector` must be present even if unused. `{}` selects every monitor in every namespace; a nil selector selects none. To filter, use `matchLabels`, which must match the monitor's `metadata.labels`.

Other `prometheusCR` fields: `probeSelector`, `scrapeConfigSelector`, namespace selectors for each kind (`serviceMonitorNamespaceSelector` and siblings), `allowNamespaces` or `denyNamespaces` (mutually exclusive), `secretNamespaces` (defaults to the TA's own namespace), `scrapeInterval` and `evaluationInterval` (30s defaults; interval in a monitor overrides), `scrapeProtocols`, and `scrapeClasses`.

`scrapeClasses` refers to the prometheus-operator ScrapeClass feature: common configuration that PodMonitors and ServiceMonitors can reference.

Security warning: with `{}` on an untrusted-tenant cluster, a monitor can steal the collector's credentials; see the file-access security note.

## Checked

Method: docs-checked 2026-11-09 against the prometheus-cr page (read in full), the Target Allocator README (PrometheusCR section) and the prometheusCR entries of the OpenTelemetryCollector API reference (lines around the allowNamespaces to serviceMonitorSelector fields).
