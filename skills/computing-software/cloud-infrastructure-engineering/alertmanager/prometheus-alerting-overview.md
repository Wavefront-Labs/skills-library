---
id: computing-software.cloud-infrastructure-engineering.alertmanager.prometheus-alerting-overview
name: prometheus-alerting-overview
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, alerting-pipeline, prometheus-rules, setup-steps]
level: intro
status: docs-checked
description: "The two-part Prometheus alerting pipeline: rules in Prometheus send alerts to Alertmanager, with the three main setup steps."
sources: ["https://prometheus.io/docs/alerting/latest/overview/", "https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/", "https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alerting overview

Alerting with Prometheus has two parts. Alerting rules in Prometheus servers send alerts to an Alertmanager. The Alertmanager then manages those alerts: silencing, inhibition, aggregation and sending notifications via methods such as email, on-call notification systems and chat platforms.

Main setup steps:
1. Set up and configure the Alertmanager.
2. Configure Prometheus to talk to the Alertmanager.
3. Create alerting rules in Prometheus.

The rules documentation adds that Prometheus alerting rules are good at figuring out what is broken right now, but are not a fully fledged notification solution. Another layer is needed for summarization, notification rate limiting, silencing and alert dependencies. In the Prometheus ecosystem, Alertmanager takes on this role.

Prometheus can be configured to periodically send information about alert states to an Alertmanager instance, and can discover available Alertmanager instances through its service discovery integrations.

```yaml
alerting:
  alertmanagers:
  - static_configs:
    - targets: ['alertmanager:9093']
```

Install Alertmanager from precompiled binaries on prometheus.io/download (recommended for released versions), from Docker images on Quay.io or Docker Hub, or by compiling from source with Go and Node.js using `make build`.

## Checked

2026-11-08. Confirmed against the Alerting overview page (two parts, three setup steps), the Alerting rules page (Sending alert notifications paragraph) and the Alertmanager README (install options, make build with Go and Node.js, static_configs alerting example).

Method: documentation only; no commands were run.
