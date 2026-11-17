---
id: computing-software.devops-ci-cd.spinnaker.prometheus-metrics-integration
name: prometheus-metrics-integration
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [prometheus, grafana, monitoring, metrics, metric-stores, pushgateway, polling]
level: practitioner
status: docs-checked
description: "Wire Spinnaker metrics into Prometheus and Grafana: direct polling (preferred) versus gateway push, ports 9090 and 3000, and hal config metric-stores prometheus enable."
sources:
  - https://github.com/spinnaker/spinnaker.github.io/blob/master/setup/monitoring/prometheus.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prometheus pairs with Grafana (the integration treats them as one system). A typical, recommended setup has a Prometheus server that **polls** its targets rather than having them push. That means Prometheus must know each Spinnaker Monitoring Daemon, which in turn polls its microservices and translates the data model for Prometheus.

**Two delivery modes:**
1. **Direct polling** is the preferred default; nothing more is needed in Halyard, but Prometheus must be configured to discover each Spinnaker service (Prometheus documentation covers EC2, Azure and other discovery).
2. **Gateway** for special cases where Prometheus cannot find the endpoints: the daemons push to a gateway at a fixed known address, and Prometheus polls the gateway. Downsides: the data is stale, and timestamps are those of retrieval, so the timeline can be off by as much as a minute, which hurts correlation with logs. Counters and long-term trends stay accurate. Use direct polling when possible.

**Ports:** Prometheus 9090 and Grafana dashboard 3000. Your browser needs both (you may need to tunnel them as for Gate and Deck).

**Install placement:** the server (with Grafana) normally runs on its own machine, with client-side configuration beside each daemon; a single-instance deployment can run everything together. The install script supports a simple single-VM prototype or a multi-VM high-availability layout on Google Cloud Platform.

**Enable in Halyard:**

```bash
hal config metric-stores prometheus enable
```

For the gateway mode, pass the gateway URL with `hal config metric-stores prometheus edit --push-gateway=<url>`. Changes are picked up the next time you run `hal deploy apply`.

This page is from the archived (2021) spinnaker.github.io repository and describes the spinnaker-monitoring daemon. The current spinnaker.io monitoring page instead recommends attaching the OpenTelemetry Java agent to each microservice and sending data to an OpenTelemetry Collector, so prefer that for new deployments.

## Checked

Method: docs-checked 2026-11-09 against the full archived spinnaker.github.io Prometheus page and the current spinnaker.io Monitoring page. Confirmed polling versus gateway trade-offs, ports 9090 and 3000, placement, the enable command and the push-gateway flag; added the note that current docs recommend OpenTelemetry.
