---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.enforcing-series-limits
name: enforcing-series-limits
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, series-limits, enforcing-cardinality-limits, sample-limit, max-global-series-per-user, mimir, per-tenant-limits, guardrails]
level: advanced
status: verified
description: "Put hard cardinality guardrails in place: per-scrape sample/label limits, per-job defaults, Mimir per-tenant series limits, and alerting before a limit drops data."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://grafana.com/docs/mimir/latest/configure/configure-metrics-storage-retention/", "https://grafana.com/docs/mimir/latest/references/configuration-parameters/#limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enforcing series limits

## Layer 1: per scrape (Prometheus)
```yaml
global:                                    # defaults for every job (these keys are in the 3.15 global block)
  sample_limit: 50000
  label_limit: 40
  label_value_length_limit: 512
scrape_configs:
  - job_name: noisy-app
    sample_limit: 200000                   # exception, documented
```
Exceeding `sample_limit` fails the **whole scrape** (`up` = 0, `sample limit exceeded`). That's intended: a
loud, attributable failure instead of silent TSDB growth (target error `sample limit exceeded`). Prometheus Operator:
`spec.enforcedSampleLimit` overrides a monitor's `sampleLimit` unless that is greater than zero and lower.

## Layer 2: per tenant (Mimir / Cortex)
```yaml
limits:                          # Mimir configuration; per-tenant overrides go in its runtime configuration
  max_global_series_per_user: 1500000
  max_global_series_per_metric: 200000
  ingestion_rate: 200000         # samples/s per tenant (default 10000)
  max_label_names_per_series: 30
```
These limit names and the default come from the Mimir configuration reference (not run here). Mimir rejects excess series (runbook
entries `err-mimir-max-series-per-user` and `err-mimir-max-series-per-metric`): **data is dropped**, so alert early.

## Alert before the cliff
```promql
# scrape close to limit
scrape_samples_post_metric_relabeling / on(job, instance) (scrape_sample_limit > 0) > 0.8
# Mimir: the limit is exported as cortex_limits_overrides{limit_name="max_global_series_per_user"}; the Mimir runbook compares
# tenant series with it, see the err-mimir-max-series-per-user runbook entry for the exact query
```
(`scrape_sample_limit` is exposed when `extra_scrape_metrics: true` is set globally or per job; the `extra-scrape-metrics` feature
flag still works but is deprecated in 3.15. A job with `sample_limit: 20` and 5 samples gave `0.25` for the ratio; the `> 0` filter drops targets without a limit, whose `scrape_sample_limit` is 0 and would give `+Inf`.)

## Process
Limits need an owner and an exception path: a ticket to raise a limit should include what the new series
are for. Review exceptions quarterly.

## Verify
- [ ] A test target exposing too many series shows `up=0` with the limit error, nothing else affected.
- [ ] 80 % warnings route to the owning team.
- [ ] Mimir discarded-sample metrics are flat in normal operation (see its runbook).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), jq 1.8.2, Git Bash tar; Mimir facts from its documentation only.
- Prometheus layer: the global and per-job YAML passes `promtool check config`; a job over `sample_limit` went `up 0` with `sample limit exceeded` while other jobs stayed up; the alert expression with `on(job, instance) (scrape_sample_limit > 0)` returned 0.25 for a 5-of-20 job and nothing for targets without a limit (the test server also held remote-written series with a `sender` label, so the check was run with `{sender=""}` selectors; the `> 0.8` form returned nothing because 0.25 < 0.8) with `extra_scrape_metrics: true`.
- Prometheus global block keys and the deprecation note on the `extra-scrape-metrics` flag: 3.15 configuration and feature-flag pages. `enforcedSampleLimit` override rule: Prometheus Operator API reference.
- Mimir layer: limit names `max_global_series_per_user`, `max_global_series_per_metric`, `ingestion_rate` (default 10000, samples per second), `max_label_names_per_series` in the Mimir configuration reference; `cortex_limits_overrides{limit_name="max_global_series_per_user"}` and the `err-mimir-max-series-per-user` / `-per-metric` entries in the Mimir runbooks. Mimir was not run; the unconfirmed metric names and status code from the draft were removed.
