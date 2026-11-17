---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-managed-alert-rules
name: grafana-managed-alert-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-alerting, grafana-managed-alerts, unified-alerting, alert-rules, alert-rule-groups, evaluation-group, pending-period, keep-firing-for, expressions, reduce-expression, math-expression, threshold-expression, classic-condition, no-data, error-state, alert-state, grafana-alerting-ha, alerting-ha, state-history, recording-rules-grafana, provisioning-alerts, alerting-api, datasource-managed-rules]
level: advanced
status: gated
description: "Build Grafana-managed alert rules that behave: query + Reduce/Threshold expressions, evaluation groups and pending periods, NoData/Error handling, routing labels, HA alerting, state history."
sources: ["https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-grafana-managed-rule/", "https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/", "https://grafana.com/docs/grafana/latest/alerting/set-up/configure-high-availability/", "https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana-managed alert rules

**Goal:** alert rules that evaluate predictably across any data source, carry the labels
notification policies need, and never surprise you with NoData pages at 3 a.m.

## 1. Grafana-managed vs data-source-managed
| | Grafana-managed | Data-source-managed (Mimir/Loki/Prometheus ruler) |
|---|---|---|
| Evaluated by | Grafana (any data source, multi-source expressions) | the ruler in the backend, PromQL/LogQL only |
| Scale | each evaluation is a query to the data source | ruler scales horizontally; cheaper for huge rule sets (scale and recording-rule capabilities not tested here) (gated: unconfirmed, source is paywalled or blocked) |
| Recording rules | Grafana-managed recording rules write via remote write (not run here) | native |
| Use when | mixed sources, SQL/cloud sources, teams working in the UI | Prometheus-native shops, GitOps PrometheusRule CRs |
Both can coexist; data-source-managed rules still route through Grafana's notification
policies if the ruler's Alertmanager is Grafana's (or you use an external Alertmanager).

## 2. Anatomy of a rule
1. **Queries** (A, B…) over a relative range (`now-5m to now`), *Instant* or Range.
2. **Expressions**: `Reduce` (`Last`/`Max` ran; mode must be `dropNN` or `replaceNN`, `strict` is rejected in alert rules), `Math`
   (`$A / $B > 0.05`, `abs($S) > 0.05 && $S < 1000`), `Threshold` (`gt`, `within_range`), `Resample` (needs its own `relativeTimeRange` when provisioned). The **alert condition** is the expression that
   decides; a threshold returns 1 (alerting) or 0 (normal) per series.
3. **Evaluation group** (folder + name + interval): all rules in a group are evaluated
   sequentially at that interval; put noisy/expensive rules in their own group.
4. **Pending period** (`for`): time the condition must hold before Firing (`0s` for
   immediate); **Keep firing for** (`keepFiringFor` in files, `keep_firing_for` in the API; ran with `5m`) to debounce flapping resolution: the instance shows `Recovering` meanwhile.
5. **Labels**: `severity`, `team`, `service` — these are what notification policies match.
6. **Annotations**: `summary`, `description`, `runbook_url`; templates use `$labels`,
   `$values.B` (reduced values by refId), `$value` (string of all).
7. **No data / Error** handling (API values): `noDataState` `NoData`, `OK`, `Alerting`, `KeepLast`; `execErrState` `Error`, `OK`, `Alerting`, `KeepLast` (all eight ran).

```yaml
# provisioning (file or API) — same shape as the export
apiVersion: 1
groups:
  - orgId: 1
    name: api-5m
    folder: payments
    interval: 1m
    rules:
      - uid: api-error-ratio
        title: API 5xx ratio high
        condition: C
        data:
          - refId: A
            relativeTimeRange: { from: 600, to: 0 }
            datasourceUid: prom-prod
            model: { expr: 'sum(rate(http_requests_total{job="api",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="api"}[5m]))', instant: true, refId: A }
          - refId: C
            datasourceUid: __expr__
            model: { type: threshold, expression: A, conditions: [{ evaluator: { type: gt, params: [0.05] } }], refId: C }
        for: 10m
        keepFiringFor: 5m
        noDataState: OK          # a ratio with no traffic is not an incident; pair with a separate "no traffic" rule
        execErrState: Error
        labels: { severity: page, team: payments }
        annotations: { summary: "API 5xx ratio {{ $values.A.Value | humanizePercentage }}", runbook_url: "https://runbooks/api-5xx" }
```

## 3. NoData and Error, decided deliberately
- A rule whose query legitimately returns nothing when healthy (`up == 0` with filtering,
  `absent()`-style tricks) must use `NoData → OK`, else it pages as "NoData" forever.
- Data-source outages produce `Error` alerts for every rule on that source; route the
  reserved labels `alertname=DatasourceError` / `DatasourceNoData` to the platform team
  via a dedicated policy, not to every service owner.
- Set `Keep last state` for rules over flaky sources only if you also alert on the flakiness.

## 4. Multi-dimensional rules
One rule with `sum by (pod)` yields one alert instance per pod, each with its own state
and pending timer; labels from the query become alert labels. Keep dimensions to what the
responder needs (`pod`, `instance`), not `request_id`.

## 5. HA and reliability
- Run ≥ 2 Grafana instances with the same database and enable the alerting gossip:
  `[unified_alerting] ha_peers=grafana-0:9094,grafana-1:9094`, `ha_listen_address`,
  `ha_advertise_address`, `ha_redis_address` (alternative to gossip): all four keys exist in `[unified_alerting]` of Grafana 13.2.4 `defaults.ini` (`ha_listen_address` defaults to `0.0.0.0:9094`). That every instance evaluates and the embedded Alertmanager cluster dedupes notifications needs two instances, which were not run (gated: unconfirmed, source is paywalled or blocked).
- State history is configured in `[unified_alerting.state_history]`: `enabled = true` by default; `backend` is `annotations` (default), `loki`, `prometheus` or `multiple`; `loki_remote_url` for Loki (from `defaults.ini`).
- Metrics to watch: `grafana_alerting_rule_evaluation_failures_total`,
  `grafana_alerting_rule_evaluation_duration_seconds`, `grafana_alerting_schedule_*`,
  `grafana_alerting_alertmanager_*`.

## 6. Provision and test
```bash
# export everything as provisioning files
curl -H "Authorization: Bearer $SA_TOKEN" https://grafana/api/v1/provisioning/alert-rules/export?format=yaml
# Terraform: grafana_rule_group ; file provisioning: conf/provisioning/alerting/*.yaml (rules, contact points, policies, templates, mute timings)
```
Provisioned rules are locked against API edits (409 `alerting.provenanceMismatch`, see the export skill); treat the files as source of truth. The rule editor's **Preview** and the state history view are UI features not exercised here (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Range queries into a Reduce(Mean) smooth away short spikes; use instant queries with the
  window inside the PromQL (`rate(...[5m])`).
- Changing a rule resets its state: updating a firing rule through the API returned it to `Normal` at once (observed) and it fires again on the next evaluation.
- Every rule needs `severity` and an owner label or the default policy swallows it.
- An unbounded `by (request_id)` rule creates one alert instance per value; keep `by (...)` to responder-relevant labels.

## Verify
- [ ] Preview shows one instance per intended dimension and the condition value you expect.
- [ ] Simulate NoData (filter to a non-existent label) and confirm the configured state, not a page.
- [ ] Stop one Grafana replica: alerts still fire once and only once.
- [ ] `grafana_alerting_rule_evaluation_failures_total` stays 0 and each group's evaluation duration < interval/2.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Prometheus 3.15.1, local webhook receivers.
- Ran the skill's provisioning YAML (data source uid and folder adapted): it loaded (`keepFiringFor`, `noDataState: OK`, `execErrState: Error`), annotation templates `{{ $values.A.Value | humanizePercentage }}` rendered `5.213%`, one instance per `service` for `sum by`, the eight NoData/Error values, `DatasourceNoData`/`DatasourceError` alerts, `Recovering`. `ha_*` and `state_history` keys read from `conf/defaults.ini` shipped with Grafana. Metrics names confirmed in `/metrics`: `grafana_alerting_rule_evaluation_failures_total`, `grafana_alerting_rule_evaluation_duration_seconds_*`, `grafana_alerting_schedule_*`, `grafana_alerting_alertmanager_*`.
- Two-instance HA behaviour and the UI features were not run (gated markers), so the skill is `gated`.
