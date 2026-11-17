---
id: computing-software.systems-network-administration.ceph.health-mute-and-detail
name: health-mute-and-detail
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, health, mute, sticky, health-detail]
level: practitioner
status: docs-checked
description: "Mute and unmute Ceph health alerts with a TTL or sticky flag, and read ceph health detail."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List current checks:

```
ceph health
ceph health detail
```

Mute a code you have accepted:

```
ceph health mute OSD_DOWN
ceph health mute OSD_DOWN 4h
ceph health mute MON_DOWN 15m
ceph health mute OSD_DOWN 1h --sticky
ceph health unmute OSD_DOWN
```

Behaviour:

- A plain mute is lifted automatically if the problem gets worse, for example more OSDs go down.
- The TTL (`4h`, `15m`) expires the mute after that time.
- `--sticky` ignores any change to that code for the period, such as further down OSDs.
- A muted check still appears in `ceph health detail` but no longer turns overall status to warning.

A muted check changes the summary rather than hiding the fault: `ceph health` then prints `HEALTH_OK (muted: OSD_DOWN)`, and `ceph health detail` lists the entry with a `(MUTED)` marker, for example `(MUTED) [WRN] OSD_DOWN: 1 osds down`. If the underlying condition resolves, the mute goes away on its own, and if the check later returns it is reported normally. The exception is a sticky mute, which survives the check clearing. Mutes on checks with a threshold, such as down OSD counts, disappear when the condition gets worse unless you use `--sticky`.

## Checked

2026-11-03. Confirmed against: the Ceph Monitoring page (docs.ceph.com/en/latest/rados/operations/monitoring/): Muting Health Checks (mute, unmute, TTL, --sticky, HEALTH_OK (muted: ...) output).

Removed: the maintenance/TTL advice.

Method: documentation only; no commands were run.
