---
id: computing-software.cybersecurity-defensive.suricata.other-log-outputs
name: other-log-outputs
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [fast-log, pcap-log, stats-log, alert-debug, file-store-output]
level: practitioner
status: docs-checked
description: "Configure the non-EVE outputs: fast.log, pcap-log modes and limits, stats.log, alert-debug, file-store and deprecated loggers."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Other outputs

- Global stats: `enabled`, `interval: 8` seconds; decoder events counted by default, `stream-events` off.
- `fast` (fast.log): one-line alerts; `append`, `ipv6-compress` (default no).
- `pcap-log`: `filename: log.pcap`, `limit: 32` (MB), `mode: normal|multi`, `conditional` (`all`, `alerts`, `tag`), optional `bpf-filter`, `lz4` compression.
- `alert-debug`: verbose alert detail, disabled by default and slow.
- `stats` (stats.log): enabled by default.
- `file-store`: version 2, disabled by default, `dir: filestore`, `max-open-files` default 0.
- `syslog` output: disabled, deprecated in 8.0, removal planned for 9.0. `tls-log` is deprecated in 8.0 and planned for removal in 9.0; `tls-store` stores TLS certificate chains to disk.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page: Stats, fast, TLS, Packet log (pcap-log), alert-debug, Stats, Syslog, File-store sections.

Removed: a closing "prefer EVE" tip and a claim that `tls-store` "remains".

Method: documentation only; no commands were run.
