---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-exposing-metrics-instrumentation
name: prometheus-operator-exposing-metrics-instrumentation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [instrumentation, client-libraries, instance-exporters, cluster-state-exporters, pushgateway, sidecar-exporter]
level: intro
status: docs-checked
description: "Choose between native instrumentation, instance exporters (sidecars), cluster-state exporters and the Pushgateway for Prometheus on Kubernetes."
sources:
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/exposing-metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
How to get metrics out of an application so Prometheus can scrape them.

- **Natively instrumented software:** exposes metrics over HTTP. Client libraries exist for many languages; use one when you instrument your own code.
- **Instance exporters:** expose metrics about a single instance of an application and are deployed as a **sidecar** in the same pod. Example: the `dnsmasq` metrics sidecar converts dnsmasq proprietary DNS-based metrics into the Prometheus format on HTTP.
- **Cluster-state exporters:** expose metrics about a whole system, deployed as a normal Deployment. Example: `kube-state-metrics`, which reports Kubernetes cluster state.
- **Short-lived jobs:** a `CronJob` that runs only seconds cannot be scraped reliably; the Pushgateway exists for that. The docs recommend avoiding it where possible and point to the Prometheus guidance on when pushing is appropriate.

See the running-exporters skill for scraping an exporter with a ServiceMonitor.

## Checked

2026-11-08. Read the exposing metrics page in full. Categories, the dnsmasq and kube-state-metrics examples and the Pushgateway advice match. Removed an unsourced Operator wiring paragraph.

Method: documentation only; no commands were run.
