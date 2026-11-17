---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.upgrading-prometheus-2-to-3
name: upgrading-prometheus-2-to-3
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-3-migration, prometheus-upgrade, prometheus, utf8-metric-names, scrape-protocols, breaking-changes]
level: advanced
status: verified
description: "Upgrade Prometheus 2.x to 3.x: go via 2.55, review breaking changes (left-open ranges, le normalisation, regex dot, removed flags) and validate rules."
sources: ["https://prometheus.io/docs/prometheus/latest/migration/", "https://prometheus.io/blog/2024/11/14/prometheus-3-0/", "https://github.com/prometheus/prometheus/releases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Prometheus 2.x to 3.x

## Path
1. Upgrade to the latest 2.55.x first. Per the migration guide the TSDB format changed slightly in 2.55, so a v3 TSDB can only be read by v2.55 or newer; you can downgrade to 2.55 but not lower without losing persistent data, and upgrading to 2.55 first is the suggested safety step (source: the migration guide; there was no 2.x binary to try).
2. Fix deprecation warnings from 2.55 logs and `promtool check config`.
3. Upgrade one replica of an HA pair, compare for a day, then the other.

## Breaking changes to review (migration guide)
Each item below was reproduced on Prometheus 3.15.1 unless noted.
- Feature flags removed (now default): `promql-at-modifier`, `promql-negative-offset`, `new-service-discovery-manager`, `expand-external-labels`, `no-default-scrape-port`, `auto-gomaxprocs`, `auto-gomemlimit`. `--enable-feature=agent` becomes `--agent`; `remote-write-receiver` becomes `--web.enable-remote-write-receiver`. Passing the old names does NOT stop startup: all nine produced `Unknown option for --enable-feature` WARN lines and the server started (the migration guide also says it logs a warning). Clean them from the unit/Helm values anyway, because the behaviour they used to gate (agent mode, remote-write receiver) is not switched on by them any more. Effects: `expand-external-labels` is now always on (run: `external_labels: {envvar: '${FOO}'}` with `FOO=expanded` showed `envvar: expanded`); `no-default-scrape-port` is now default (run: target `localhost` was scraped as `http://localhost/good`, no `:80` added); `--[no-]auto-gomaxprocs` and `--[no-]auto-gomemlimit` are flags that default to true.
- Range selectors and lookback are left-open: a sample exactly at the range start is excluded. Run in `promtool test rules`: with samples one minute apart, `count_over_time(x[5m])` returned 5 and a subquery `count_over_time(x[1m:1m])` returned 1, so `rate`/`increase` over `foo[1m:1m]` has no data; `x[2m:1m]` returned 2 (the migration guide's fix).
- `le` and `quantile` label values are normalised to floats at ingestion (`le="1"` becomes `le="1.0"`, `quantile="1"` becomes `1.0`, run against a text-format target). Queries or relabel rules matching `le="1"` literally must change; the migration guide recommends fixing the references rather than relabelling back.
- Regex `.` now matches newlines too (run: `label_replace(..., "x", "a\nb" ...)` matched the regex `a.b`; `a[^\n]b` did not, which is the v2 behaviour recipe in the guide).
- Scrapes are stricter about `Content-Type`; targets with missing/invalid headers fail unless `fallback_scrape_protocol` is set on the job. Run: no header gave `non-compliant scrape target sending blank Content-Type and no fallback_scrape_protocol specified for target`; `text/x-whatever` gave `received unsupported Content-Type "text/x-whatever" and no fallback_scrape_protocol specified for target`; the same target with `fallback_scrape_protocol: PrometheusText0.0.4` was `up`.
- UTF-8 metric and label names accepted by default (`global.metric_name_validation_scheme: utf8` showed in `/api/v1/status/config`); set `legacy` globally or per scrape job to keep the old validation (migration guide).
- `holt_winters` renamed `double_exponential_smoothing` and moved behind `promql-experimental-functions` (run: `holt_winters` is `unknown function`, `double_exponential_smoothing` is `not enabled` without the flag).
- Alertmanager v1 API no longer supported (run: `promtool check config` rejected `api_version: v1` with `expected Alertmanager api version to be one of [v2] but got v1`); needs Alertmanager 0.16 or later (migration guide).
- Other config changes from the guide: `scrape_classic_histograms` was renamed `always_scrape_classic_histograms` (run: the old key is rejected, `field scrape_classic_histograms not found`), and `http_config.enable_http2` for `remote_write` now defaults to false. From 3.9 the `native-histograms` feature flag is a no-op (run: logged as one); scraping them needs `scrape_native_histograms`.
- Logging moved to slog; log field names changed (run: lines are `time=... level=INFO source=main.go:...`), update log parsing/alerts.
- New UI; old UI via `--enable-feature=old-ui` during transition (`old-ui` is in the 3.15.1 `--help` list; the UI itself was not opened).

## Validation
```bash
promtool check config prometheus.yml
promtool check rules rules/*.yml
promtool test rules tests/*.yml
```
Compare key recording rules between old and new replica: `abs(new - old) / old` over a day.

## Gotchas
- Thanos/Mimir sidecars and remote-write receivers must support the versions; check their compatibility notes.
- If Prometheus is deployed from a Helm chart or an operator, read that chart's upgrade notes and CRD updates before bumping the image tag.

## Verify
- [ ] No `target down` regressions on the targets page after upgrade.
- [ ] Rule unit tests pass and dashboards using `le="..."` literals were updated.

## Checked
Prometheus 3.15.1, promtool and a small local exposition server (Python) run on Windows: the nine removed feature flags (WARN, startup continues), env expansion in external_labels, default scrape port, left-open range selectors and subqueries (`promtool test rules`), `le`/`quantile` normalisation from a text target, regex newline matching, Content-Type strictness with and without `fallback_scrape_protocol`, `holt_winters` and `double_exponential_smoothing`, Alertmanager `api_version: v1`, the renamed histogram option. Docs read: the Prometheus 3.0 migration guide (docs/migration.md at tag v3.15.1).
