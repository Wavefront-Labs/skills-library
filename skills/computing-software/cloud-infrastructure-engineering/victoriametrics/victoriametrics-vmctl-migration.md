---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmctl-migration
name: victoriametrics-vmctl-migration
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmctl, migration, prometheus-snapshot, influxdb, vm-native, rate-limit, verify-block]
level: practitioner
status: docs-checked
description: "Migrate data into VictoriaMetrics with vmctl from Prometheus snapshots, InfluxDB and other VictoriaMetrics clusters."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmctl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmctl migration

vmctl subcommands: `prometheus`, `influx`, `opentsdb`, `remote-read`, `mimir`, `thanos`, `vm-native`, `verify-block`.

```text
./vmctl prometheus --vm-addr=<victoriametrics-addr>:8428 --prom-snapshot=/path/to/snapshot
./vmctl influx --influx-addr=http://localhost:8086 --influx-database=mydb --vm-addr=http://localhost:8428
```

Influx flags: `--influx-addr` (default `http://localhost:8086`), `--influx-user` (env `INFLUX_USERNAME`), `--influx-database`.

Destination flags: `--vm-addr`; `--vm-user` and `--vm-password` (env `VM_USERNAME`, `VM_PASSWORD`); `--vm-account-id` for a cluster tenant (point `--vm-addr` at vminsert, `http://<vminsert-addr>:8480`); `--vm-concurrency` (each worker can use about one vCPU); `--vm-batch-size` (50k to 500k recommended); `--vm-rate-limit` in bytes per second per worker; `--vm-round-digits`; `--vm-significant-figures`; `--vm-extra-label label=value` (repeatable, overrides existing labels).

Other flags: `-s` silent mode skips the confirmation prompt; `-disable-progress-bar`.

Rate limiting alternatives: `--vm-rate-limit`, or run vmagent as a proxy with `-remoteWrite.rateLimit`.

Verify exported native blocks:

```text
curl localhost:8428/api/v1/export/native -g -d 'match[]={__name__!=""}' -o exported_data_block
./vmctl verify-block exported_data_block
```

Monitor a migration (from v1.135.0) with `--pushmetrics.url=http://localhost:8428/api/v1/import/prometheus` and `--pushmetrics.extraLabel='job="vmctl"'`. Per-mode flags for OpenTSDB, remote-read, Thanos and Mimir live on dedicated vmctl subpages.

Prefer explicit values for the flags above in scripts so the same restore command can be rerun after an interruption.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
