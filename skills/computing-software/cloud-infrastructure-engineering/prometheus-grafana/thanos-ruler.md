---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-ruler
name: thanos-ruler
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos, thanos-ruler-setup, stateless-ruler, global-alerting, recording-rules, remote-write, thanosruler-crd]
level: advanced
status: docs-checked
description: "Evaluate global rules with Thanos Ruler: query endpoints, Alertmanager targets, stateful vs stateless (remote-write) mode, partial-response strategy, and its reliability limits."
sources: ["https://thanos.io/tip/components/rule.md/", "https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.ThanosRuler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos Ruler

Use it for rules that need data from several Prometheus servers (cross-cluster SLOs, sharded Prometheus).
Keep everything else in each Prometheus: local rules don't depend on the network or Query.

```bash
thanos rule \
  --rule-file=/etc/thanos/rules/*.yaml \
  --query=dnssrv+_http._tcp.thanos-query.monitoring.svc \
  --alertmanagers.url=dnssrv+http://_web._tcp.alertmanager-operated.monitoring.svc \
  --label='ruler_cluster="global"' --label='replica="$(POD_NAME)"' \
  --alert.label-drop=replica \
  --eval-interval=1m \
  --data-dir=/var/thanos/rule --objstore.config-file=objstore.yml
```
That is stateful mode (local TSDB + upload). For stateless mode replace the last line with
`--remote-write.config-file=rw.yml` (no local blocks; output ships via remote write).

## Stateful vs stateless
| | Stateful | Stateless (`--remote-write.config-file`) |
|---|---|---|
| Recording-rule output | local TSDB, uploaded to bucket, served via StoreAPI | remote-written to Receive/Mimir |
| Alert `for` state across restarts | see the Ruler page's notes on alert state | see the Ruler page's stateless-mode limitations |
| Ops | needs local disk (`--data-dir`) | no local blocks; no StoreAPI exposed |

## Partial response
Rules are evaluated via Query; if a store is down, the result may be partial. Per group:
```yaml
groups:
  - name: global-slo
    partial_response_strategy: abort    # default 'abort': fail evaluation rather than alert on partial data
```
`warn` evaluates on what's available: risky for alerts (false resolves), acceptable for dashboards.

## Reliability notes
- The Ruler depends on Query and every store; alert on its own failures:
  `thanos_rule_evaluation_with_warnings_total` counts evaluations that returned partial-response warnings, and the mixin's `mixin/alerts/rule` group has the rest.
- Run 2 replicas and drop the replica label on alerts so Alertmanager dedups.
- Operator: `ThanosRuler` CRD with `ruleSelector`, reusing PrometheusRule objects.

## Verify
- [ ] Ruler `/rules` page shows groups healthy; alerts reach Alertmanager once (deduped).
- [ ] Recording-rule output queryable via Thanos Query with `ruler_cluster="global"` (the external label set by `--label`).

## Checked
- 2026-10-28. Confirmed against the Thanos Rule page (stateful vs stateless mode, `--remote-write.config-file` enables stateless mode and the Ruler then exposes no StoreAPI, `partial_response_strategy` `abort` default and `warn`, `--alert.label-drop`, `--label`, `--eval-interval=1m`, `thanos_rule_evaluation_with_warnings_total`).
- Removed: the `ALERTS_FOR_STATE` row, the `prometheus_rule_evaluation_failures_total` query and the PVC/Deployment claims. Hostnames and `ruler_cluster` are placeholders for your environment.
Method: documentation only; no commands were run.
