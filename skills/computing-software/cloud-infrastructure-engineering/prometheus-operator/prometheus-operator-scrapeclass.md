---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-scrapeclass
name: prometheus-operator-scrapeclass
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [scrapeclass, scrape-class-default, tlsconfig-merge, istio-mtls, shared-scrape-settings]
level: advanced
status: docs-checked
description: "Define shared scrape settings once as a ScrapeClass on Prometheus or PrometheusAgent and reference it from monitors, including default classes and tlsConfig merging."
sources: ["https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/developer/scrapeclass.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ScrapeClass` (operator newer than v0.73.0) holds common configuration applied across `PodMonitor`, `ServiceMonitor`, `ScrapeConfig` and `Probe` objects, much like a StorageClass. The motivating case is scraping every pod in an Istio mesh with strict mTLS: instead of repeating certificate paths in each monitor, define them once.

## Define
Add `spec.scrapeClasses` to the `Prometheus` or `PrometheusAgent` resource: a list of named classes, each carrying settings such as `tlsConfig`. Set `default: true` on one class to apply it to all scrape objects that do not name a class. Only one default may exist; with several the operator fails reconciliation and reports it in the resource status.

## Use
Monitors reference a class with `spec.scrapeClass: <name>`.

## Errors
If a monitor names a class that the selecting Prometheus does not define, the operator rejects the monitor and emits an event such as `scrapeClass "istio" not found in Prometheus scrapeClasses`.

## Precedence
Class settings apply only where the monitor has not set the field. For `tlsConfig` the operator merges field by field: values set on the monitor win, unset fields inherit from the class.

## Checked

2026-11-08. Read scrapeclass.md in full from the operator repo. Default-class rule, status error, missing-class event and field-by-field tlsConfig merge match.

Method: documentation only; no commands were run.
