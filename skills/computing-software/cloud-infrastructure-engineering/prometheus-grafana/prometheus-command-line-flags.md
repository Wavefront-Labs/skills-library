---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-command-line-flags
name: prometheus-command-line-flags
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prometheus-flags, command-line-flags, storage-tsdb-path, retention-flags, web-listen-address, web-external-url, route-prefix, query-flags, enable-feature, log-level, agent-flag, flags-vs-config, systemd-unit, pca]
level: practitioner
status: gated
description: "Set the Prometheus flags that cannot live in prometheus.yml: storage path and retention, web listen/external URL, query limits, feature flags, agent mode; inspect them at runtime."
sources: ["https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://prometheus.io/docs/prometheus/latest/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus command-line flags

**Goal:** know which knobs are flags (restart required) versus config (reloadable), and set
the handful that every production instance needs.

## 1. The ones you always set
```bash
prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.listen-address=0.0.0.0:9090 \
  --web.external-url=https://prom.example.com/ \
  --web.enable-lifecycle \
  --web.config.file=/etc/prometheus/web.yml \
  --log.format=json
```
Do not put `# comment` after a trailing `\`: the shell ends the command at the backslash-space and runs the next line on its own (reproduced: `two: command not found`). Notes on the flags above: `--web.external-url` is used in alert links and when behind a path prefix; `--web.enable-lifecycle` enables `/-/reload` and `/-/quit`; `--web.config.file` carries TLS and basic auth.

In 3.15 the retention flags (`--storage.tsdb.retention.time`, `--storage.tsdb.retention.size`) and `--log.level` are marked **deprecated** in `--help`; the config file now has `storage.tsdb.retention.{time,size,percentage}` and `runtime.log_level`, and the config value takes precedence over the flag (run: flag `9d` plus config `3d` logged `TSDB retention updated duration=3d`). The flags still work, so older units keep running:
```yaml
# prometheus.yml (3.x)
storage:
  tsdb:
    retention:
      time: 15d        # and/or size: 200GB (whichever hits first)
```
Flags use Kingpin: `--flag=value` or `--flag value` (both run); booleans are `--web.enable-lifecycle` and `--no-web.enable-lifecycle` (shown as `--[no-]...` in `--help`); repeating a flag is an error (`flag ... cannot be repeated`). `prometheus --help` is authoritative for your version.

## 2. Groups worth knowing
| Flag | Default | Notes |
|---|---|---|
| `--storage.tsdb.retention.time` | 15d | deprecated in favour of the config field; units `y w d h m s ms` (`1y` is accepted) |
| `--storage.tsdb.retention.size` | 0 (off) | deprecated in favour of the config field; WAL and m-mapped chunks count toward the total but only blocks are deleted; docs say set it to at most 80-85% of the disk |
| `--storage.tsdb.wal-compression` | true | hidden flag; `/api/v1/status/flags` reports `true`; keep on |
| `--storage.tsdb.no-lockfile` | false | needed on some NFS/overlay setups; otherwise keep the lock |
| `--storage.tsdb.min-block-duration` / `max-block-duration` | 2h / 10% of retention | hidden flags; the status page showed `2h` and `1d12h` with 15d retention; setting `max=2h` for a Thanos sidecar is documented by Thanos (not run) |
| `--query.timeout` | 2m | per-query ceiling |
| `--query.max-samples` | 50,000,000 | memory guard; a query loading more fails |
| `--query.max-concurrency` | 20 | parallel queries |
| `--query.lookback-delta` | 5m | staleness window; rarely change |
| `--web.route-prefix` | from external-url | when serving under `/prometheus` |
| `--web.enable-admin-api` | false | snapshots, delete_series, clean_tombstones |
| `--web.enable-remote-write-receiver` | false | accept remote write on `/api/v1/write` |
| `--web.page-title` | `Prometheus Time Series Collection and Processing Server` | visible env name in the UI |
| `--rules.alert.for-outage-tolerance` | 1h | restore `for` state after restart within this |
| `--rules.alert.for-grace-period` | 10m | minimum `for` after restore |
| `--rules.alert.resend-delay` | 1m | min time between re-sends to Alertmanager |
| `--alertmanager.notification-queue-capacity` | 10000 | |
| `--enable-feature=` | | comma list; e.g. `exemplar-storage,memory-snapshot-on-shutdown` (`native-histograms` is now a logged no-op; set `scrape_native_histograms` in config) |
| `--agent` | | agent mode (see `prometheus-agent-mode-operations`); changes which `--storage.agent.*` flags apply |
| `--config.auto-reload` + `--config.auto-reload-interval` | off / 30s | polling self-reload; the interval alone does nothing, `--config.auto-reload` must be set (run: with only the interval the file change was ignored; with both the log said `Configuration file change detected`) |

## 3. Flags vs config, and how to see what's running
Everything above is a flag → restart. Scrape targets, rules, remote write, external labels →
config → reload. Inspect a running instance:
```bash
curl -s localhost:9090/api/v1/status/flags     # effective flags as JSON under .data
curl -s localhost:9090/api/v1/status/config    # loaded config as a YAML string under .data.yaml
```
The `/flags` page in the UI shows the same. Useful when the systemd unit, a wrapper script
and the Helm values disagree.

## 4. systemd unit skeleton
```ini
# (gated: unconfirmed, source is paywalled or blocked) systemd is Linux-only and was not run here
[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus --storage.tsdb.retention.time=30d --web.enable-lifecycle
ExecReload=/bin/kill -HUP $MAINPID
TimeoutStopSec=600       # let shutdown finish; after a SIGKILL the next start replays the WAL (slower start, data protected by the WAL)
LimitNOFILE=65536
Restart=on-failure
```

## Gotchas
- `--web.external-url` with a path (`https://host/prom`) sets the route prefix too; probes
  must then hit `/prom/-/ready`.
- Retention size counts the WAL and m-mapped chunks but only persistent blocks are deleted, so a
  `retention.size` below the WAL size leaves nothing but the head (storage docs; not reproduced here).
- `--storage.tsdb.retention.time=1y` is valid in 3.15 (run: `TSDB retention updated duration=1y`).
- Changing `--storage.tsdb.path` to an empty dir starts a fresh database silently.
- `--enable-feature` flags are version-specific; a removed/graduated flag (`native-histograms`) logs a
  no-op warning, and a mistyped one also only logs `Unknown option for --enable-feature` and the server still starts, so read the startup log.

## Verify
- [ ] `/api/v1/status/flags` shows the retention and query limits you intended.
- [ ] A reload (`curl -X POST .../-/reload`, or `systemctl reload` where systemd is used) logs "Completed loading of configuration file".
- [ ] Stopping the service takes seconds and the next start logs no WAL corruption.

## Checked
Prometheus 3.15.1 (windows-amd64 release) run locally: `--help` output read for every flag and default in the table; `/api/v1/status/flags` compared (page title, wal-compression, block durations, notification queue, query limits, rules.alert.* defaults); `1y` retention, flag-versus-config retention precedence, space-separated flag values, `--config.auto-reload` with and without the interval flag, `--web.external-url` with a path (`/prom/-/ready` 200, `/-/ready` 404), `native-histograms` and a bogus feature name, and the shell backslash-comment trap. Docs read: storage.md and configuration.md at tag v3.15.1. Not run: systemd unit, `retention.size` below the WAL, Thanos block-duration advice.
