---
id: computing-software.cloud-infrastructure-engineering.alertmanager.core-concepts-grouping-inhibition-silences
name: core-concepts-grouping-inhibition-silences
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, concepts, deduplication, silences, inhibition]
level: intro
status: docs-checked
description: "The core Alertmanager concepts: deduplication, grouping, routing, inhibition and silences, and how Prometheus sends alerts to it."
sources: ["https://prometheus.io/docs/alerting/latest/alertmanager/", "https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alertmanager core concepts

Alertmanager handles alerts sent by client applications such as the Prometheus server. It deduplicates, groups and routes them to the correct receiver integration such as email, PagerDuty or OpsGenie, and takes care of silencing and inhibition.

- Grouping: categorizes alerts of similar nature into a single notification. Useful in large outages when hundreds or thousands of alerts fire at once. Grouping, timing and receivers are configured by the routing tree.
- Inhibition: suppresses notifications for certain alerts if certain other alerts are already firing, for example muting everything about a cluster when the alert that the whole cluster is unreachable fires. Configured in the configuration file.
- Silences: mute alerts for a given time. A silence is defined by matchers, like the routing tree. Incoming alerts are checked against all equality or regular expression matchers of an active silence; if they match, no notifications are sent. Silences are configured in the web interface.
- Client behavior: Alertmanager has special requirements for its clients, relevant only to advanced use cases where Prometheus is not the sender.
- High availability: configured with the `--cluster-*` flags. Prometheus should be pointed at a list of all Alertmanagers, not a load balancer.

```
alertmanager --config.file=alertmanager.yml
```

The README adds that Alertmanager is installed from precompiled binaries (recommended for released versions), Docker images on Quay.io or Docker Hub, or compiled from source.

## Checked

2026-11-08. Confirmed against the Alertmanager overview page (grouping, inhibition, silences, client behavior, high availability and --cluster flags, no load balancing) and the README install section (precompiled binaries recommended, Quay.io and Docker Hub images, source build).

Method: documentation only; no commands were run.
