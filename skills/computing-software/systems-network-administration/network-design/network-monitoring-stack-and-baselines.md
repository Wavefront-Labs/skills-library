---
id: computing-software.systems-network-administration.network-design.network-monitoring-stack-and-baselines
name: network-monitoring-stack-and-baselines
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-monitoring, baseline, network-baseline, librenms, zabbix, prometheus, snmp-exporter, alert-thresholds, interface-utilization, polling-interval, availability-monitoring, grafana, observability]
level: practitioner
status: docs-checked
description: "Stand up network monitoring that pages for the right things: what to poll, LibreNMS/Zabbix/Prometheus snmp_exporter, baselines, and low-noise alert thresholds."
sources:
  - https://docs.librenms.org/
  - https://github.com/prometheus/snmp_exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network monitoring stack and baselines

## What to collect
| Signal | Source |
|---|---|
| Device up / reachability | ICMP + SNMP sysUpTime |
| Interface status, traffic (64-bit HC counters), errors, discards | SNMP IF-MIB or streaming telemetry |
| CPU, memory, temperature, PSU/fan | vendor MIBs |
| Routing neighbours (BGP/OSPF state) | SNMP traps + polling |
| Logs | syslog to a collector |
| Flows (who uses bandwidth) | NetFlow/IPFIX/sFlow |
| Synthetic tests (DNS, HTTP, latency to key sites) | probes |

Choose polling intervals per signal: short for up/down and routing state, longer for slow-moving
values such as temperature. Shorter intervals cost more storage and device CPU.

## Tool options
- **LibreNMS**: auto-discovery, alerting rules (with templates and transports) and an API.
  A quick win for most multi-vendor estates.
- **Zabbix**: template-driven monitoring with flexible triggers.
- **Prometheus + snmp_exporter + Grafana**: fits teams already on Prometheus. The exporter listens
  on port 9116 and is scraped at `/snmp?target=<device>`; the `module` and `auth` URL parameters
  select what to walk and how to authenticate (defaults: module `if_mib`, auth `public_v2`, both
  must exist in `snmp.yml`). `snmp.yml` is generated, not hand-edited: use the generator with the
  MIBs you need. Scrape per device through relabelling:
  ```yaml
  - job_name: snmp
    static_configs: [{targets: [10.0.0.5, 10.0.0.6]}]
    metrics_path: /snmp
    params: {module: [if_mib], auth: [nms_v3]}
    relabel_configs:
      - {source_labels: [__address__], target_label: __param_target}
      - {source_labels: [__param_target], target_label: instance}
      - {target_label: __address__, replacement: snmp-exporter:9116}
  ```
  Turn the HC octet counters into bits/s with `rate()` over a window several times the scrape
  interval, multiplied by 8. `nms_v3` is a name you define in your own `snmp.yml`.

## Baselines
Collect long enough to see daily and weekly cycles before setting thresholds: normal peaks per
link, error rates, CPU. Record them and revisit after major changes. Alerts should fire on
deviation from normal, not just fixed numbers.

## Alert thresholds that work
- Device/link down: alert after several failed polls, not one (avoid single-poll flaps).
- Utilisation: alert on sustained high use of WAN/uplink capacity; use 95th-percentile reporting
  for capacity planning. Pick the level and duration from the baseline.
- Errors: any sustained rise in CRC/input errors, and discards as a share of packets.
- CPU high for a sustained period; memory trending upward (leak) as a trend alert.
- BGP/OSPF neighbour down: immediate (traps), confirmed by polling.
- Route alerts to owners with runbook links; every alert must be actionable or deleted.

## Verify
- [ ] Every device and uplink monitored; new devices discovered automatically.
- [ ] Baseline report exists for core/WAN links.
- [ ] A test (shut a lab uplink) produces one actionable alert, not a storm.

## Checked
2026-10-28. Confirmed against the prometheus/snmp_exporter README: port 9116, `/snmp?target=`,
`auth` and `module` parameters with defaults `public_v2` and `if_mib`, relabelling of
`target`/`auth`/`module`, generated `snmp.yml`. Confirmed against the LibreNMS docs index:
auto discovery, alerting rules/templates/transports, API. Removed (not confirmable from the sources):
the polling-interval column, the 2-4 week baseline, the 80%/15 min, 0.1% and 80% CPU thresholds, the
exam-objective reference, CDP/LLDP discovery detail and Zabbix feature claims.
Method: documentation only; no commands were run.
