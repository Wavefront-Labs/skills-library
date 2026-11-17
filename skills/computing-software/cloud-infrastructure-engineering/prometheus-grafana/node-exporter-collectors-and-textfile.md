---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.node-exporter-collectors-and-textfile
name: node-exporter-collectors-and-textfile
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [node-exporter, node-exporter-collectors, collector-flags, textfile-collector-usage, cron-metrics-textfile, systemd-collector, linux-monitoring]
level: practitioner
status: docs-checked
description: "Tune node_exporter collectors (enable/disable flags, filesystem and netdev excludes) and publish cron/script metrics through the textfile collector with atomic writes."
sources: ["https://raw.githubusercontent.com/prometheus/node_exporter/master/README.md", "https://raw.githubusercontent.com/prometheus-community/node-exporter-textfile-collector-scripts/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# node_exporter collectors and the textfile collector

## Collector flags
```bash
node_exporter \
  --collector.disable-defaults --collector.cpu --collector.meminfo --collector.filesystem \
  --collector.netdev --collector.diskstats --collector.loadavg --collector.textfile \
  --collector.systemd --collector.systemd.unit-include='(nginx|postgresql|docker)\.service' \
  --collector.filesystem.mount-points-exclude='^/(dev|proc|run|sys|var/lib/docker/.+|var/lib/kubelet/.+)($|/)' \
  --collector.netdev.device-exclude='^(veth.*|cali.*|lo)$' \
  --collector.textfile.directory=/var/lib/node_exporter/textfile
```
- `--collector.<name>` enables, `--no-collector.<name>` disables a default-enabled collector;
  `--collector.disable-defaults --collector.<name> ...` enables only the ones you name.
- Disabled by default (README lists them with reasons such as high cardinality, long runtime or heavy host load):
  `systemd`, `processes`, `tcpstat` (the README warns of potential performance issues in high-load situations),
  `ethtool`, `interrupts`, `perf`, `slabinfo`, among others.
- Enable extra collectors with caution: one at a time, test on a non-production system, then on a single production
  node, and watch `scrape_duration_seconds` and `scrape_samples_post_metric_relabeling`.
- Include and exclude flags are mutually exclusive on a collector that supports both. Collectors with them include
  `arp`, `diskstats`, `ethtool`, `filesystem` (`fs-types`, `mount-points`), `hwmon`, `interrupts`, `netdev`,
  `qdisc`, `sysctl` (include only) and `systemd` (`unit-include`, `unit-exclude`).
- `node_scrape_collector_success` and `node_scrape_collector_duration_seconds` are the per-collector meta-metrics. A
  collector that cannot find a file in `/proc` or `/sys` reports success 0 on purpose, to expose failed drivers.
- In a container, run with host networking and host PID, bind-mount `/` read-only at `/host` and set
  `--path.rootfs=/host` (the README's Docker example uses `--net="host"`, `--pid="host"` and `-v "/:/host:ro,rslave"`).

## Textfile collector
Set `--collector.textfile.directory`; the collector parses all files in it matching `*.prom` in the Prometheus text
format. Timestamps are not supported. It is for metrics tied to a machine (batch job completion, static roles); the
README says service-level metrics belong in the Pushgateway.
```bash
#!/bin/sh
# /etc/cron.daily/backup-metrics  (runs after the backup job)
DIR=/var/lib/node_exporter/textfile
cat <<EOF > "$DIR/backup.prom.$$"
# HELP backup_last_success_timestamp_seconds Last successful backup.
# TYPE backup_last_success_timestamp_seconds gauge
backup_last_success_timestamp_seconds{job_name="pg-nightly"} $(date +%s)
backup_size_bytes{job_name="pg-nightly"} $(stat -c %s /backups/latest.dump)
EOF
mv "$DIR/backup.prom.$$" "$DIR/backup.prom"      # atomic rename: never expose half-written files
```
The write-to-a-temp-name-then-`mv` pattern is the README's own. The example scripts repo recommends piping into
`sponge` (from moreutils) instead; it cannot write atomically if `TMPDIR` is on a different filesystem from the target.
Alert on staleness of your own timestamp metric with `time() - backup_last_success_timestamp_seconds > <seconds>`.

## Verify
- [ ] `node_scrape_collector_success == 1` for all enabled collectors.
- [ ] The `.prom` file appears in the directory and its metrics show on the node_exporter `/metrics` page.

## Checked
Checked against the node_exporter README (collector flags, include and exclude table, enabled and disabled collector
tables, meta-metrics, Docker example, textfile section) and the textfile collector scripts README (`sponge`). Removed
unconfirmed claims: `node_textfile_scrape_error` and `node_textfile_mtime_seconds`, the duplicate-HELP parse error,
the do-not-add-`instance`/`job`-labels rule, the `arp`/`netclass`/`hwmon` noisy-defaults remark, the Kubernetes
DaemonSet field names and the 26-hour alert figure.

Method: docs-only read of cited pages, 2026-11-08
