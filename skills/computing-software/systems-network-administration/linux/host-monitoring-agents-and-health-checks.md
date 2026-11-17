---
id: computing-software.systems-network-administration.linux.host-monitoring-agents-and-health-checks
name: host-monitoring-agents-and-health-checks
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, monitoring, monitoring-agent, node-exporter, health-checks, collectd, telegraf, prometheus, textfile-collector, smartmon, systemd-metrics, alerting, disk-full-alert, dead-mans-switch, blackbox-exporter, zabbix-agent, netdata, capacity-planning, lpic-2, sysadmin, systemd-watchdog]
level: practitioner
status: gated
description: "Instrument Linux hosts: node_exporter (or Telegraf/collectd/Zabbix) as a locked-down service, textfile-collector metrics, host alerts that matter, scriptable health checks."
sources:
  - https://github.com/prometheus/node_exporter
  - https://prometheus.io/docs/alerting/latest/alertmanager/
  - https://docs.influxdata.com/telegraf/v1/
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Host monitoring agents and health checks — know before the users do

**Goal:** every host exports CPU/memory/disk/network/systemd metrics to the central
system, custom numbers you care about are one file away, alerts fire on symptoms not
noise, and services expose a health endpoint something can act on.

## 1. node_exporter (Prometheus ecosystem — the default today)
```bash
dnf install golang-github-prometheus-node-exporter   # Fedora/EPEL; Debian: apt install prometheus-node-exporter
# or the upstream tarball:
useradd -r -s /sbin/nologin node_exporter
# download the linux-amd64 tarball from the node_exporter GitHub releases page, then copy the node_exporter binary to /usr/local/bin
```
```ini
# /etc/systemd/system/node_exporter.service
[Unit]
Description=Prometheus node exporter
After=network-online.target
[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter \
  --web.listen-address=10.0.10.21:9100 \
  --collector.systemd --collector.processes \
  --collector.textfile.directory=/var/lib/node_exporter/textfile \
  --collector.filesystem.mount-points-exclude='^/(dev|proc|sys|run|var/lib/docker|var/lib/containers)($|/)' \
  --web.config.file=/etc/node_exporter/web.yml
Restart=on-failure
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
ReadWritePaths=/var/lib/node_exporter
[Install]
WantedBy=multi-user.target
```
`web.yml` → `tls_server_config: {cert_file: …, key_file: …}` and `basic_auth_users:` (bcrypt) so (gated: unconfirmed, source is paywalled or blocked)
metrics aren't world-readable; or bind to the management IP and firewall `9100/tcp` to the
Prometheus servers only (`firewall-cmd --add-rich-rule='rule family=ipv4 source address=10.0.0.5 port port=9100 protocol=tcp accept' --permanent`).
`curl -s localhost:9100/metrics | grep -E '^node_(filesystem_avail_bytes|load1|memory_MemAvailable)'` to check.

Custom metrics via the textfile collector (any cron/timer writes `*.prom` atomically):
```bash
# /usr/local/sbin/backup-metrics.sh (run at end of backup job)
cat > /var/lib/node_exporter/textfile/backup.prom.$$ <<EOF
# HELP backup_last_success_timestamp_seconds Unix time of last successful backup
# TYPE backup_last_success_timestamp_seconds gauge
backup_last_success_timestamp_seconds $(date +%s)
EOF
mv /var/lib/node_exporter/textfile/backup.prom.$$ /var/lib/node_exporter/textfile/backup.prom
```
Community collections of textfile scripts exist (SMART, pending updates, RAID); check the metric names they emit before alerting on them. Keep each file small.

## 2. Alternatives when the stack is different
- **Telegraf** (InfluxDB/anything via outputs): `/etc/telegraf/telegraf.d/*.conf` with
  `[[inputs.cpu]] [[inputs.mem]] [[inputs.disk]] [[inputs.systemd_units]] [[inputs.smart]]`
  and `[[outputs.prometheus_client]]` or `[[outputs.influxdb_v2]]`; `telegraf --test` to print one sample.
- **collectd** (legacy, tiny): `LoadPlugin cpu/memory/df/interface/load/processes` in `collectd.conf`,
  `write_prometheus` or `network` output; `collectd -t` config test.
- **Zabbix agent 2**: `Server=`/`ServerActive=`/`Hostname=` in `zabbix_agent2.conf`, `UserParameter=` for
  custom checks; firewall 10050/tcp from the server.
- **Netdata**: one-command install, per-second dashboards; great for a single box, chatty at fleet scale.
- Cloud agents (CloudWatch agent, Google Ops Agent, Azure Monitor) when the host lives there.
One agent per concern; two agents reading the same counters doubles the noise, not the insight.

## 3. Alerts that matter on a host (PromQL, Alertmanager rules)
```yaml
groups:
- name: host
  rules:
  - alert: HostDown
    expr: up{job="node"} == 0
    for: 3m
  - alert: DiskWillFillIn4h
    expr: predict_linear(node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"}[1h], 4*3600) < 0 and node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.2
    for: 15m
  - alert: DiskInodesLow
    expr: node_filesystem_files_free / node_filesystem_files < 0.05
  - alert: MemoryPressure
    expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes < 0.1
    for: 10m
  - alert: HighLoadPerCore
    expr: node_load5 / count without(cpu,mode) (node_cpu_seconds_total{mode="idle"}) > 2
    for: 15m
  - alert: SystemdUnitFailed
    expr: node_systemd_unit_state{state="failed"} == 1
    for: 5m
  - alert: BackupStale
    expr: time() - backup_last_success_timestamp_seconds > 36*3600
  - alert: ClockSkew
    expr: abs(node_timex_offset_seconds) > 0.1
```
Principles: alert on **symptoms with a runbook** (disk will fill, service failed), not on
every threshold; `for:` to avoid flapping; route by `severity` label; a **dead-man's switch**
(`Watchdog` alert always firing → external receiver expects it) proves the pipeline is alive.

## 4. Health checks services can expose
- Scriptable local check (for cron, load balancers, systemd):
  ```bash
  #!/bin/bash   # /usr/local/sbin/healthcheck.sh — exit 0 healthy, 1 not
  set -euo pipefail
  curl -fsS --max-time 2 http://127.0.0.1:8080/healthz >/dev/null
  systemctl is-active --quiet postgresql
  [ "$(df --output=pcent / | tail -1 | tr -dc 0-9)" -lt 90 ]
  ```
- systemd watchdog: `WatchdogSec=30` + the app calling `sd_notify("WATCHDOG=1")` restarts a hung
  service; `Restart=on-failure` + `StartLimitIntervalSec` prevents loops. `OnFailure=alert@%n.service`
  sends a notification.
- Load balancer/K8s style: `/healthz` (process alive) vs `/readyz` (dependencies OK) — don't
  make liveness depend on the database or you restart the app when the DB blips.
- Blackbox exporter from outside: `probe_success`, `probe_ssl_earliest_cert_expiry`, ICMP/TCP/HTTP modules.
- Push for jobs that can't be scraped: Pushgateway (last value only) or healthchecks.io-style pings.

## Failure modes
- Exporter listening on 0.0.0.0 without auth → metrics (hostnames, versions, mounts) leak to anyone.
- Mount-point exclusions missing → thousands of overlay/container filesystem series per host.
- Textfile `.prom` written in place (not `mv`) → half-written files, parse errors, gaps.
- Alert on `node_load1 > N` without per-core normalisation → noise on big boxes, silence on small.
- Monitoring host monitors itself only → `up` can't be 0 when it's dead; the dead-man's switch must terminate elsewhere.

## Verify
- [ ] `curl -s host:9100/metrics | grep -c '^node_'` > 500 and Prometheus `up{instance="host:9100"} == 1`.
- [ ] Fill a tmp filesystem to 95 % and the disk alert fires within `for:`; stop a unit and `SystemdUnitFailed` fires.
- [ ] The textfile metric from the backup job appears and `BackupStale` fires when the job is skipped for a day.

## Checked

2026-11-02

- Confirmed: node_exporter README, the Prometheus Alertmanager overview and the Telegraf docs index were fetched.
- Removed or gated: Collector flag names (web.listen, collector.processes), web.yml and the systemd hardening directives are not stated on the fetched pages; gated, confirm in the node_exporter README and systemd.exec man page.

Method: documentation only; no commands were run.
