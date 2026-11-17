---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimirtool-rules-analyze-and-alertmanager
name: mimirtool-rules-analyze-and-alertmanager
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [mimirtool, mimir, mimirtool-analyze, rules-sync, alertmanager-load, unused-metrics]
level: practitioner
status: docs-checked
description: "Use mimirtool to sync and check rule files, load Alertmanager config, and analyse which metrics dashboards and rules actually use."
sources: ["https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: GitOps for rules and data-driven cleanup of unused metrics.

Connection: `MIMIR_ADDRESS` (`--address`), `MIMIR_TENANT_ID` (`--id`), `MIMIR_API_KEY` (`--key`), `MIMIR_API_USER` (`--user`), `MIMIR_AUTH_TOKEN`/`--auth-token`, TLS via `MIMIR_TLS_CA_PATH` etc. With the default `-server.path-prefix` of `/`, give only the host for `--address` (not `/alertmanager`).
```
export MIMIR_ADDRESS=<MIMIR_URL>
export MIMIR_TENANT_ID=<TENANT_ID>

mimirtool rules check rules/*.yaml      # best-practice check, no cluster access
mimirtool rules lint rules/*.yaml       # reformats YAML and PromQL IN PLACE; -n for a dry run
mimirtool rules diff rules/*.yaml       # compare with the cluster
mimirtool rules sync rules/*.yaml       # apply the differences to the cluster
mimirtool rules prepare -i rules/*.yaml # add the cluster label to aggregations
mimirtool alertmanager load config.yaml templates/*.tpl
mimirtool alertmanager get --output-dir=am   # writes config.yaml and *.tpl
```
`rules load <file>...` overwrites existing groups of the same name; `rules list|print|get|delete` inspect and remove groups. `diff` and `sync` accept one of `--namespaces`, `--ignored-namespaces`, `--namespaces-regex`, `--ignored-namespaces-regex`.

Find unused metrics
```
mimirtool analyze grafana --address=<GRAFANA_URL> --key=<API_KEY>   # metrics-in-grafana.json
mimirtool analyze ruler --address=<MIMIR_URL> --id=<TENANT_ID>      # metrics-in-ruler.json
mimirtool analyze prometheus --address=<URL> --id=<TENANT_ID> \
  --grafana-metrics-file=metrics-in-grafana.json --ruler-metrics-file=metrics-in-ruler.json
```
Offline alternatives: `analyze dashboard <file>...` and `analyze rule-file <file>`. The `prometheus` step output (`prometheus-metrics.json`) reports `total_active_series`, `in_use_active_series`, `additional_active_series` and per-metric counts. It requests every active series, so it is slow on large instances.

Gotchas
- `rules check` flags recording rules whose names do not follow `level:metric:operation`.
- Keep API keys in CI secrets.

## Verify
`mimirtool rules diff` shows no differences after a sync.

## Checked
2026-11-03. Confirmed against the Mimirtool page (configuration tables, rules, alertmanager and analyze sections). Removed: `rules sync` deletes-groups claim (the page says it applies any differences), the `CORTEX_` env var remark, the `--prometheus-http-prefix=/` example value, the backfill tag and the relabeling advice.
Method: documentation only; no commands were run.
