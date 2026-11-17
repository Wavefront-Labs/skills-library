---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.splitting-config-with-scrape-config-files
name: splitting-config-with-scrape-config-files
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [scrape-config-files, split-prometheus-config, scrape-config, prometheus, config-reload, promtool]
level: practitioner
status: verified
description: "Split a large prometheus.yml into per-team scrape job files with scrape_config_files globs, validation with promtool and safe reloads."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/", "https://prometheus.io/docs/prometheus/latest/command-line/promtool/", "https://prometheus.io/docs/prometheus/latest/management_api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitting config with scrape_config_files

Since Prometheus 2.43 (changelog entry under 2.43.0), the top-level `scrape_config_files` lists globs of files that each contain a `scrape_configs:` list. They are merged with any inline `scrape_configs` (run on 3.15.1: an inline `inline` job and a `payments-api` job from `scrape.d/payments.yml` were both scraped).

```yaml
# prometheus.yml
global: {scrape_interval: 30s}
rule_files: [/etc/prometheus/rules/*.yml]
scrape_config_files:
  - /etc/prometheus/scrape.d/*.yml
```
```yaml
# /etc/prometheus/scrape.d/payments.yml
scrape_configs:
  - job_name: payments-api
    static_configs: [{targets: ["payments-1:8080", "payments-2:8080"]}]
```

## Rules
- `job_name` must be unique across all files; duplicates fail the whole load (run: `found multiple scrape configs with job name "payments-api", first found in ...dup.yml`).
- Each file may contain only `scrape_configs` (no globals, no rules): a file with `global:` failed with `field global not found in type config.ScrapeConfigs`, and one with `rule_files:` the same for that key (run).
- Relative paths resolve against the main config file's directory (run: `promtool check config run/sc/prometheus.yml` from a different working directory loaded `scrape.d/*.yml` and passed).
- Reload (`SIGHUP` or `POST /-/reload`) rereads matched files; new files matching the glob are picked up on reload, not automatically (run: a new `newteam.yml` was absent from `/api/v1/targets` until `POST /-/reload`, then present).

## Workflow per team
1. Team PR adds `scrape.d/<team>.yml` (CODEOWNERS per file).
2. CI: `promtool check config prometheus.yml` (it follows `scrape_config_files`: its duplicate-job and bad-key errors above came from the included files).
3. Deploy file, then reload; check `prometheus_config_last_reload_successful == 1` (the gauge updates at the next scrape).

## Alternatives
- `file_sd_configs` when only targets change (no reload needed, picked up on file change; run: adding a second target to the JSON file showed up in `/api/v1/targets` after about 8 s with no reload).

## Gotchas
- A broken file blocks every reload, so all teams' changes stop applying; gate with CI. Run: with a `broken.yml` (`scrape_configs: [oops`) in `scrape.d/`, `POST /-/reload` returned 500 `failed to reload config: one or more errors occurred while applying the new configuration`, and a later valid `another.yml` was not applied either.
- Keep globs strict (`*.yml`): a loose glob such as `*` would match editor backup files like `payments.yml~`.

## Verify
- [ ] `promtool check config` passes in CI on every change.
- [ ] New job appears under Status > Targets after reload (checked through `/api/v1/targets`).

## Checked
Prometheus 3.15.1 and promtool (windows-amd64) run locally: `check config` on a main file with `scrape_config_files` and an inline job, duplicate `job_name` across files, `global:` and `rule_files:` inside a scrape file, relative-path resolution from another working directory; a running server for reload pickup of a new file, a broken file blocking reload, and `file_sd_configs` picking up a changed JSON without reload. Source: Prometheus CHANGELOG (2.43.0 entry for `scrape_config_files`) and configuration.md at v3.15.1.
