---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-scrapeconfig-crd-and-selection
name: prometheus-operator-scrapeconfig-crd-and-selection
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [scrapeconfig, scrapeconfig-selector, external-targets, service-discovery-tiers, static-config]
level: practitioner
status: docs-checked
description: "Use the ScrapeConfig CRD to scrape external or unusual targets: select it from Prometheus, scope namespaces, and understand tier-1 versus tier-2 service discovery."
sources: ["https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/developer/scrapeconfig.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ScrapeConfig` (operator newer than v0.65.1, CRD installed and operator restarted afterwards) scrapes targets outside the cluster, or builds configurations that `ServiceMonitor`, `PodMonitor` and `Probe` cannot.

## Selecting
Set `scrapeConfigSelector` on `Prometheus` or `PrometheusAgent` to a label match, for example `matchLabels: {prometheus: system-monitoring-prometheus}`. Without `scrapeConfigNamespaceSelector` only the same namespace is searched. Use `scrapeConfigNamespaceSelector: {}` for all namespaces, or `matchLabels` for namespaces with given labels.

## Service discovery support
- Tier 1 (fully supported): Kubernetes, File, Static, DNS and HTTP service discovery.
- Tier 2 (maintainers review but do not actively maintain): cloud providers such as Azure, EC2, GCE and DigitalOcean, listed in the ScrapeConfig graduation proposal.

## Static targets
`staticConfigs` with `targets` lists host:port values. Example from the docs: scrape `http://prometheus.demo.do.prometheus.io:9090` by listing `prometheus.demo.do.prometheus.io:9090`.

The full field list lives in the API reference for `monitoring.coreos.com/v1alpha1.ScrapeConfig`. Prefer the higher-level monitors where they suffice.

## Checked

2026-11-08. Read scrapeconfig.md in full from the operator repo. Claims match; no changes needed.

Method: documentation only; no commands were run.
