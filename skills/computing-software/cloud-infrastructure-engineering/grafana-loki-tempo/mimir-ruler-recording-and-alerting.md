---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-ruler-recording-and-alerting
name: mimir-ruler-recording-and-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [mimir-ruler, mimir, recording-rules, alerting-rules, ruler-storage, alertmanager-url, rule-groups]
level: practitioner
status: docs-checked
description: "Run recording and alerting rules in the Mimir ruler: internal or remote evaluation, rule storage, rule limits, Alertmanager URL and managing rules with mimirtool or the API."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/components/ruler/", "https://grafana.com/docs/mimir/latest/configure/configuration-parameters/", "https://grafana.com/docs/mimir/latest/references/http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: server-side rule evaluation that survives pod restarts.

```yaml
ruler:
  rule_path: /data/ruler
  evaluation_interval: 1m
ruler_storage:
  backend: s3          # s3, gcs, azure, swift, filesystem or local
  s3:
    bucket_name: <RULER_BUCKET>
limits:
  ruler_alertmanager_client_config:
    alertmanager_url: <ALERTMANAGER_URL>
```
`ruler.alertmanager_url` is deprecated in favour of `limits.ruler_alertmanager_client_config.alertmanager_url` (flag `-ruler.alertmanager-url`; DNS service discovery format supported). `rule_path` holds temporary rule files and need not persist (default `./data-ruler/`). Rule groups are re-synced from object storage every 10m by default (`-ruler.poll-interval`).

Evaluation modes
- Internal (default): the ruler runs its own querier against ingesters and store-gateways. No query acceleration, so very high cardinality rules can take longer than the evaluation interval and miss data points.
- Remote: set `-ruler.query-frontend.address` and the ruler evaluates through the query-frontend (query sharding applies). An `http://` or `https://` address delegates to a Prometheus-compatible server.
- Rule results are written through an internal distributor by default; `-ruler.distributor.address` pushes them to remote distributors over gRPC.

Managing rules
```
mimirtool rules load rules.yaml --address=<MIMIR_URL> --id=<TENANT_ID>
mimirtool rules list --address=<MIMIR_URL> --id=<TENANT_ID>
```
`--address`, `--id` map to `MIMIR_ADDRESS`, `MIMIR_TENANT_ID`. API (under `<prometheus-http-prefix>`): `GET /api/v1/rules` lists rules; `GET|POST|DELETE /config/v1/rules/{namespace}[/{groupName}]` read, set and delete rule groups.

Limits (per tenant, defaults): `ruler_max_rules_per_rule_group` 20, `ruler_max_rule_groups_per_tenant` 70; `ruler_min_rule_evaluation_interval` 0s, `ruler_evaluation_delay_duration` 1m.

Gotchas
- The ruler shards by rule group across a ruler hash ring, so one expensive group runs on one ruler.
- Local rule storage supports sharding only if every ruler has the same rule files (mount a ConfigMap into each pod).

## Verify
`GET <prometheus-http-prefix>/api/v1/rules` with the tenant header shows your groups; recorded series appear in queries.

## Checked
2026-11-03. Confirmed against the Mimir ruler page, the configuration parameters reference (ruler, ruler_storage, limits defaults), the mimirtool page and the HTTP API reference. Removed: the plain `ruler.alertmanager_url` setting, the Alertmanager-config-first gotcha, the `cortex_prometheus_rule_group_iterations_missed_total` metric, `lastEvaluation` claim and the curl example.
Method: documentation only; no commands were run.
