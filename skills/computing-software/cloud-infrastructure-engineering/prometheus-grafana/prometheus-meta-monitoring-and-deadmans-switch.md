---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-meta-monitoring-and-deadmans-switch
name: prometheus-meta-monitoring-and-deadmans-switch
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-meta-monitoring, deadmans-switch, watchdog-alert, prometheus, alertmanager, meta-monitoring]
level: practitioner
status: docs-checked
description: "Monitor the monitoring: prometheus-mixin self-alerts, a second Prometheus watching the first, and the always-firing Watchdog alert routed to an external dead man's switch."
sources: ["https://prometheus.io/docs/prometheus/latest/getting_started/", "https://github.com/prometheus-operator/kube-prometheus/blob/main/manifests/kubePrometheus-prometheusRule.yaml", "https://monitoring.mixins.dev/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Meta-monitoring and the dead man's switch

A Prometheus cannot alert that it is down. Cover it from outside.

## Layers
1. Self alerts from the prometheus-mixin (listed on monitoring.mixins.dev/prometheus): `PrometheusBadConfig`,
   `PrometheusRuleFailures`, `PrometheusNotificationQueueRunningFull`, `PrometheusErrorSendingAlertsToAnyAlertmanager`
   (more than 3% errors sending alerts), `PrometheusNotConnectedToAlertmanagers`, `PrometheusTSDBCompactionsFailing`,
   `PrometheusRemoteWriteBehind`, `PrometheusTargetSyncFailure`. Mixin severities: `critical` for `PrometheusBadConfig`,
   `PrometheusRuleFailures`, `PrometheusRemoteWriteBehind`, `PrometheusTargetSyncFailure` and
   `PrometheusErrorSendingAlertsToAnyAlertmanager`; `warning` for `PrometheusNotificationQueueRunningFull`,
   `PrometheusNotConnectedToAlertmanagers` and `PrometheusTSDBCompactionsFailing`.
2. Cross-watch: a second Prometheus in another cluster or region scrapes the first one's `/metrics` endpoint (Prometheus
   serves its own metrics there, as the getting-started guide shows) and alerts on `up` for that job being 0.
3. Dead man's switch: an always-firing alert proves the whole path (Prometheus, rules, Alertmanager, receiver) works.

## Watchdog alert (as shipped in kube-prometheus)
```yaml
- alert: Watchdog
  expr: vector(1)
  labels:
    severity: none
  annotations:
    summary: An alert that should always be firing to certify that Alertmanager is working properly.
```
The kube-prometheus description says the alert should always be firing in Alertmanager and always fire against a
receiver, and that integrations exist which notify when it is not firing, for example the "DeadMansSnitch" integration
in PagerDuty. Route it to such an external heartbeat receiver; the heartbeat service pages when the pings stop. See the
Alertmanager configuration reference (not covered by the pages checked here) for route and receiver syntax and
`repeat_interval`.

## Related alert in the same file
kube-prometheus also ships `InfoInhibitor` (severity `none`): it fires for namespaces with `severity="info"` alerts and
no firing `warning` or `critical` alert, and is meant to be routed to a null receiver and used to inhibit `info` alerts.
Take care that inhibition rules written for `severity: none` do not also catch Watchdog.

## Verify
- [ ] Stopping Alertmanager makes the external heartbeat service raise its page within its configured window.
- [ ] Mixin alerts are loaded: rules appear on the Prometheus rules page.

## Checked

Checked 2026-11-08 against the prometheus-mixin alert list on monitoring.mixins.dev, the kube-prometheus
`kubePrometheus-prometheusRule.yaml` (Watchdog and InfoInhibitor) and the Prometheus getting-started page. Corrected
`PrometheusConfigReloadFailed` to `PrometheusBadConfig`, which is the name in the mixin list. Removed because the cited
pages do not state them: the Alertmanager route snippet, specific heartbeat vendors other than the PagerDuty
integration named in the rule, heartbeat interval arithmetic and per-cluster id advice.
Method: docs-only read of cited pages, 2026-11-08
