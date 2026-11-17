---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-inhibition-rule-design
name: alertmanager-inhibition-rule-design
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [inhibition-design, inhibit-equal-labels, inhibit-rules, alertmanager, alert-fatigue]
level: practitioner
status: gated
description: "Write inhibit_rules that suppress dependent alerts (warning under critical, everything under cluster down) with correct equal labels, and avoid self-inhibition."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/#inhibit_rule", "https://prometheus.io/docs/alerting/latest/alertmanager/#inhibition", "https://github.com/prometheus-operator/kube-prometheus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inhibition rule design

An inhibition mutes target alerts while a source alert is firing, if they share the values of the `equal` labels.

```yaml
inhibit_rules:
  # warning muted when the same alert is critical for the same target
  - source_matchers: [severity="critical"]
    target_matchers: [severity="warning"]
    equal: [alertname, namespace, service]
  # node down mutes everything on that node
  - source_matchers: [alertname="NodeDown"]
    target_matchers: [alertname!="NodeDown"]
    equal: [node]
  # whole-cluster outage mutes per-service alerts in that cluster
  - source_matchers: [alertname="ClusterUnreachable"]
    target_matchers: [severity=~"warning|critical"]
    equal: [cluster]
  # InfoInhibitor pattern from kube-prometheus: info alerts only notify when nothing else fires
  - source_matchers: [alertname="InfoInhibitor"]
    target_matchers: [severity="info"]
    equal: [namespace]
```
The four rules were loaded into Alertmanager 0.34.1 (`check-config` SUCCESS, 5 rules with one extra) and alerts fired through `POST /api/v2/alerts`; every rule behaved as written: a `warning` with the same alertname/namespace/service as a `critical` went `suppressed` (a `warning` for another service stayed active), `OnNode9` was inhibited by `NodeDown` node=n9 but `OnNode8` was not (and `NodeDown` did not inhibit itself), and an `info` alert in namespace `q` was inhibited by `InfoInhibitor` in `q` while one in `other` stayed active. That kube-prometheus ships this pattern was not checked (gated: unconfirmed, source is paywalled or blocked).

## Rules
- `equal` is essential: without it a source anywhere mutes targets everywhere.
- If a label in `equal` is missing on both alerts, they are considered equal (empty == empty), which can over-inhibit. Run: a `NodeDown` alert with no `node` label put every alert that also lacked a `node` label into `suppressed`, including `Watchdog`, `Inf2` and `DiskFull`. Ensure the label exists.
- An alert matching both source and target matchers cannot inhibit itself. Whether two such alerts inhibit each other was tested with a rule whose source and target were the same matcher (`kind="mutual"`, equal `grp`): with two or three such alerts, none was inhibited in 0.34.1, so the earlier "can inhibit each other" warning did not reproduce. Still make target matchers exclude the source (as the `NodeDown` rule does) so intent is explicit.

## Seeing inhibitions
- API: `GET /api/v2/alerts` returns every alert with `status.state` = `suppressed` and `status.inhibitedBy` = [the source alert fingerprint] (run); `amtool alert query -i` shows them. The UI filter name was not checked here.
- Inhibited alerts still exist in Prometheus `ALERTS` (Prometheus is unaware of inhibition; gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Inhibiting the Watchdog by a broad rule breaks the dead man's switch (run: the missing-label case above suppressed `Watchdog`).
- A source alert that flaps lets targets notify on each gap; `keep_firing_for` on the source alerting rule (a Prometheus rule field) is the usual fix (not run here).

## Verify
- [ ] Test: fire source and target in staging (`amtool alert add` or `POST /api/v2/alerts`) and confirm only the source notifies (the inhibited state check was run; webhook delivery was not captured for these).

## Checked
Alertmanager 0.34.1 and amtool (windows-amd64) run locally with a webhook receiver: `check-config` on the four rules, then fourteen alerts posted to `/api/v2/alerts` and read back with `status.state` / `status.inhibitedBy` for the critical/warning, NodeDown/node, InfoInhibitor/namespace cases, the empty-equals-empty case (NodeDown with no `node` label suppressed Watchdog), and a same-matcher mutual rule (neither alert inhibited). Not run: kube-prometheus rules, `keep_firing_for` in Prometheus, UI filters.
