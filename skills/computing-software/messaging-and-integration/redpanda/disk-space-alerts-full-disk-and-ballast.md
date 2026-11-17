---
id: computing-software.messaging-and-integration.redpanda.disk-space-alerts-full-disk-and-ballast
name: disk-space-alerts-full-disk-and-ballast
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [disk-full, storage-min-free-bytes, space-alert, ballast-file, metrics, producers-blocked]
level: practitioner
status: docs-checked
description: "Monitor Redpanda free disk with redpanda_storage_disk_free_space_alert, set alert and hard thresholds, know the 5 GiB default, prepare a ballast file."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/disk-utilization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If a node reaches critically low disk, Redpanda blocks clients from writing; if it runs out, the process terminates.

**Metrics:** `redpanda_storage_disk_total_bytes`, `redpanda_storage_disk_free_bytes` and `redpanda_storage_disk_free_space_alert` with values 0 (no alert), 1 (low free space) or 2 (out of space, degraded, external writes rejected).

**Thresholds**

| Property | Meaning |
|---|---|
| `storage_space_alert_free_threshold_bytes` | Free bytes below which the low-space alert fires |
| `storage_space_alert_free_threshold_percent` | Same, as a percentage of the drive |
| `storage_min_free_bytes` | Hard limit; below it Redpanda enters the degraded state |

Set one of bytes or percent to zero to disable it. These do not control Continuous Data Balancing. On alert Redpanda logs an error-level `storage space alert` line such as free space at 25.574% on `/var/lib/redpanda/data`.

**Full disk.** Below the hard limit Redpanda rejects external writes but still allows internal traffic like replication and rebalancing. `storage_min_free_bytes` defaults to 5 GiB; when any broker's free space falls below it, writes are rejected to all brokers.

**Ballast file.** An empty file you delete as a last resort to regain space and time to remove topics or records and fix retention. In `redpanda.yaml`:

```yaml
rpk:
  tune_ballast_file: true
  ballast_file_path: "/var/lib/redpanda/data/ballast"
  ballast_file_size: "1GiB"
```
Create it with `rpk redpanda tune ballast_file`. The path must be on the same mount as the data directory. Size it to give you time to react but small enough not to waste space.

Other levers: shorter retention, Tiered Storage with space management, and Continuous Data Balancing.

## Checked

2026-11-08. Partial read of the Manage Disk Space page: the introduction and the sections Monitor disk space, Set free disk space thresholds, Handle full disks and Create a ballast file (other sections were not read). Confirmed the opening statements, the three metrics and alert values 0, 1 and 2, the three threshold properties and zero-to-disable, the Continuous Data Balancing note, the error-level log line, the 5 GiB default and write rejection on all brokers, internal traffic still allowed, and the ballast YAML, command and same-mount-point rule. The closing list of other levers is from the page introduction.

Method: documentation only; no commands were run.
