---
id: computing-software.systems-network-administration.linux.mdadm-monitor-alerting
name: mdadm-monitor-alerting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mdadm, mdadm-monitor, raid-alerts, mailaddr, mdmonitor, degraded-array, software-raid]
level: practitioner
status: docs-checked
description: "Get alerted when an md array degrades: MAILADDR/PROGRAM in mdadm.conf, the mdmonitor service, --test alerts, and wiring events into monitoring instead of email."
sources:
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.8.in
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.conf.5.in
  - https://github.com/prometheus/node_exporter/blob/master/collector/mdadm_linux.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mdadm --monitor alerting

A degraded RAID1 runs silently until the second disk dies — monitoring is not optional.

## Configure
`/etc/mdadm.conf` or `/etc/mdadm/mdadm.conf` (both are searched):
```
MAILADDR ops@example.com
MAILFROM mdadm@host01.example.com
PROGRAM /usr/local/sbin/md-alert       # one program only; called with: <event> <md-device> [component]
```
Mail alerts need a working local MTA/relay.
```bash
systemctl status mdmonitor.service     # where systemd manages monitoring; also configurable: MONITORDELAY (default 60 s)
mdadm --monitor --scan --test --oneshot   # generates a TestMessage for every array
```
## Events
`DeviceDisappeared`, `RebuildStarted`, `RebuildNN` (default increment 20, so 20/40/60/80), `RebuildFinished`, `Fail`, `FailSpare`, `SpareActive`, `NewArray`, `DegradedArray`, `MoveSpare`, `SparesMissing`, `TestMessage`.

## PROGRAM example (push to monitoring)
```bash
#!/bin/sh
logger -t md-alert "$1 $2 $3"
curl -fsS -X POST https://alerts.example/api -d "host=$(hostname) event=$1 array=$2 dev=$3" || true
```
Alternatively scrape `/proc/mdstat` with node_exporter (`node_md_disks{state="failed"}`) and alert in Prometheus.

## Gotchas
- With `--scan`, mdadm monitors the arrays listed in mdadm.conf; keep ARRAY lines current (`mdadm --detail --scan`).
- Disk-level SMART warnings come earlier than md failure — monitor both.

## Verify
- [ ] The `--test` alert arrives in the right channel; the monitor service is active.

## Checked

Checked against the mdadm main branch (mdadm.8.in MONITOR MODE, mdadm.conf.5.in, Makefile) and prometheus/node_exporter collector/mdadm_linux.go (last commit 2026-10-24), repository last pushed 2026-10-08.
Confirmed: the event names and the default RebuildNN increment of 20; PROGRAM runs with two or three arguments and only one PROGRAM line is used; `--test` with `--oneshot`; `MONITORDELAY` default 60 seconds; both config file locations; `node_md_disks` with a `failed` state label.
Removed unconfirmed claims: the RHEL/Debian enablement details and the `mail -s` test.

Method: documentation only; no commands were run.
