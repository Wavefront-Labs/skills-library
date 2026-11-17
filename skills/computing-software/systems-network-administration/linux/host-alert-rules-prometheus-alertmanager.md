---
id: computing-software.systems-network-administration.linux.host-alert-rules-prometheus-alertmanager
name: host-alert-rules-prometheus-alertmanager
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, alertmanager, host-alert-rules, prometheus-rules, node-exporter, promtool, alert-routing]
level: practitioner
status: draft
description: "Write host alert rules for Linux fleets with node_exporter metrics: disk, memory, load, systemd and clock alerts, for and severity labels, Alertmanager routing and testing."
sources:
  - https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
  - https://prometheus.io/docs/alerting/latest/configuration/
  - https://samber.github.io/awesome-prometheus-alerts/rules#host-and-hardware
  - https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Host alert rules in Prometheus/Alertmanager

## Rules that page for real problems
```yaml
# /etc/prometheus/rules/host.yml
groups:
- name: host
  rules:
  - alert: HostDown
    expr: up{job="node"} == 0
    for: 3m
    labels: { severity: critical }
    annotations: { summary: "{{ $labels.instance }} unreachable for 3m" }

  - alert: HostDiskWillFillIn24h
    expr: |
      predict_linear(node_filesystem_avail_bytes{fstype!~"tmpfs|overlay|squashfs"}[6h], 24*3600) < 0
      and node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.2
      and node_filesystem_readonly == 0
    for: 30m
    labels: { severity: warning }
    annotations: { summary: "{{ $labels.mountpoint }} on {{ $labels.instance }} fills within 24h" }

  - alert: HostOutOfMemory
    expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes < 0.05
    for: 5m
    labels: { severity: critical }

  - alert: HostOomKill
    expr: increase(node_vmstat_oom_kill[15m]) > 0
    labels: { severity: warning }

  - alert: HostSystemdUnitFailed
    expr: node_systemd_unit_state{state="failed"} == 1      # needs --collector.systemd
    for: 5m
    labels: { severity: warning }

  - alert: HostClockSkew
    expr: abs(node_timex_offset_seconds) > 0.05 or node_timex_sync_status == 0
    for: 10m
    labels: { severity: warning }

  - alert: HostHighCpuSaturation
    expr: node_load15 / count without (cpu, mode) (node_cpu_seconds_total{mode="idle"}) > 2
    for: 30m
    labels: { severity: warning }
```
Principles: alert on symptoms and imminent exhaustion (predictive disk), not on "CPU > 80%"; always use `for:` to absorb blips; put actionable text and a runbook URL in annotations.

## Test before deploying
```bash
promtool check rules /etc/prometheus/rules/host.yml
promtool test rules tests/host_test.yml       # unit tests with synthetic series
curl -X POST localhost:9090/-/reload          # needs --web.enable-lifecycle
```
```yaml
# tests/host_test.yml
rule_files: [../rules/host.yml]
tests:
- interval: 1m
  input_series:
  - series: 'up{job="node",instance="a"}'
    values: '0x5'
  alert_rule_test:
  - eval_time: 4m
    alertname: HostDown
    exp_alerts: [{ exp_labels: { severity: critical, job: node, instance: a } }]
```

## Alertmanager routing
```yaml
route:
  receiver: team-email
  group_by: [alertname, instance]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
  - matchers: [severity="critical"]
    receiver: pager
inhibit_rules:
- source_matchers: [alertname="HostDown"]
  target_matchers: [severity=~"warning|critical"]
  equal: [instance]          # host down silences its other alerts
receivers:
- name: pager
  pagerduty_configs: [{ routing_key: "<key>" }]
- name: team-email
  email_configs: [{ to: ops@example.com }]
```
```bash
amtool check-config alertmanager.yml
amtool config routes test --config.file=alertmanager.yml severity=critical alertname=HostDown
amtool silence add instance=web1:9100 --duration=2h --comment="maintenance"
```

## Verify
- [ ] Stopping node_exporter on a test host fires HostDown and pages; other alerts for it are inhibited.
- [ ] `promtool test rules` runs in CI.
