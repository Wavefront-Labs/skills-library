---
id: computing-software.cloud-infrastructure-engineering.alertmanager.ha-prometheus-and-disable
name: ha-prometheus-and-disable
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, high-availability, prometheus-alerting-config, disable-ha]
level: practitioner
status: docs-checked
description: "Pointing Prometheus at every Alertmanager peer (no load balancer) and turning clustering off with an empty --cluster.listen-address."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md", "https://prometheus.io/docs/alerting/latest/alertmanager/", "https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus to HA Alertmanagers, and disabling HA

Point Prometheus 1.4 or later at all Alertmanager instances in `prometheus.yml`:

```yaml
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager1:9093
      - alertmanager2:9093
      - alertmanager3:9093
```

Important: do not load balance traffic between Prometheus and its Alertmanagers. The implementation expects all alerts to be sent to all Alertmanagers to ensure high availability. The Alertmanager overview page repeats this: point Prometheus to a list of all Alertmanagers. The Alerting rules page adds that Prometheus can discover Alertmanagers through its service discovery integrations.

Start a peer set by giving each node the others via `--cluster.peer`. The README suggests running three peers on one machine with `goreman` and the Procfile in the repository:

```
goreman start
```

Turning off HA: if clustered mode is not wanted, set `--cluster.listen-address=` (empty). This prevents Alertmanager from listening to incoming peer requests.

The README notes that Alertmanager high availability is in production use at many companies.

## Checked

2026-11-08. Confirmed against the Alertmanager README (High Availability section, goreman, Prometheus alerting example, --cluster.listen-address= to turn off), the Alertmanager overview page and the Alerting rules page. Removed: the --cluster.tls-config remark, which these pages do not state.

Method: documentation only; no commands were run.
