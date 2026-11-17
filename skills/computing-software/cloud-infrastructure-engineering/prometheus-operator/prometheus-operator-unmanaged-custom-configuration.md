---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-unmanaged-custom-configuration
name: prometheus-operator-unmanaged-custom-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [custom-configuration, unmanaged-config, prometheus-yaml-gz, disable-unmanaged-configuration]
level: advanced
status: docs-checked
description: "Supply your own full Prometheus configuration instead of operator-generated config, and know which spec fields stop working."
sources:
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/custom-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page carries a warning that custom (unmanaged) configuration will be deprecated in favor of the additional scrape config option. It is not the operator main goal and operator changes may break such setups.

## When
- Service discovery other than Kubernetes (AWS, Azure and so on).
- Cases the operator does not yet support well, such as blackbox probes (at the time this was written).

## How it is triggered
Specify **neither** `serviceMonitorSelector` nor `podMonitorSelector`. When both are empty the operator does not manage the Secret holding the configuration. That Secret is named `prometheus-<name-of-prometheus-object>` in the same namespace, and the configuration lives under the key `prometheus.yaml.gz`.

## What stops working
Anything that feeds the generated configuration has no effect, so set it by hand: `serviceMonitorSelector` itself (monitors no longer configure Prometheus), `alerting` (Alertmanager discovery), `scrapeInterval`, `scrapeTimeout`, `evaluationInterval`, `externalLabels`.

## Checked

2026-11-08. Read custom-configuration.md in full. Corrected the deprecation wording (the page says will be deprecated in favor of additional scrape config) and removed an unsourced operator flag section.

Method: documentation only; no commands were run.
