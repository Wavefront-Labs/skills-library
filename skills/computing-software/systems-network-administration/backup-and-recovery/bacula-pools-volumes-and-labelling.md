---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-pools-volumes-and-labelling
name: bacula-pools-volumes-and-labelling
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula, bacula-pool, bacula-volume, bareos, volume-retention, recycling, label, autochanger]
level: advanced
status: docs-checked
description: "Configure Bacula pools and volumes: per-level pools, retention and recycling, labelling disk and tape volumes, and volume status management in bconsole."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Automated_Disk_Backup.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Brief_Tutorial.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula pools, volumes and labelling

**Goal:** volumes that recycle predictably, so retention holds and storage never fills by surprise.

## Pools per level
```text
Pool {
  Name = Full-Pool
  Pool Type = Backup
  Recycle = yes
  AutoPrune = yes
  Volume Retention = 6 months
  Maximum Volume Bytes = 50G
  Maximum Volumes = 100
  Label Format = "Full-"
}
Pool { Name = Inc-Pool;  Pool Type = Backup; Recycle = yes; AutoPrune = yes; Volume Retention = 20 days; Maximum Volume Bytes = 10G; Label Format = "Inc-" }
Pool { Name = Scratch;   Pool Type = Backup }
```
Route levels to pools in the Job/JobDefs:
```text
Full Backup Pool = Full-Pool
Differential Backup Pool = Diff-Pool
Incremental Backup Pool = Inc-Pool
```
The Pool named `Scratch` is special: when Bacula needs a new volume and finds none, it takes an available one from Scratch into the pool the job is using.

## Retention
- `Volume Retention` is how long catalog records are kept after the end time of each job written to the volume; the default is 365 days, and `0` disables it. It is stored on each volume when created: changing the Pool resource later does not change existing volumes (use `update` in the Console).
- The Job, File and Volume retention periods are all applied; the shortest effectively wins.
- Pruned does not mean recycled: Bacula keeps the data as long as possible and recycles only when it needs a volume.
- Too short a volume retention can prune the last valid Full, so the next Incremental or Differential is promoted to Full. The manual's minimum is twice the Full interval (monthly Fulls: at least two months).

## Labelling
- Disk: `Label Format` lets Bacula create volumes automatically, with `LabelMedia = yes` in the SD Device.
- Tape with barcodes, in bconsole: `*label barcodes`, then `*update slots`.
- To reuse the oldest volume manually: `list volumes`, check it shows `Purged` (if not, `purge jobs volume`), then `relabel`.

## Volume status
A volume goes from `Append` to `Full` when it fills. Other states you will see: `Used` (set by hand to stop appending), `Purged` (all jobs pruned), `Recycle`, and `Cleaning` (barcodes matching the Pool's cleaning prefix).
```text
*list volumes pool=Full-Pool
*purge jobs volume
```

## Gotchas
- A volume appended over many days retains longer than expected, because retention counts from each job's end time; limit with `Volume Use Duration` or `Maximum Volume Jobs`.
- `Recycle = no` means Bacula never reuses the pool's volumes, so storage keeps growing.
- `Purge Oldest Volume` overrides retention periods; prefer `Recycle Oldest Volume` or normal AutoPrune.

## Verify
`list volumes` shows volumes cycling through Append, Full, Purged and Recycle states, and repository free space is stable over a retention cycle.

## Checked
2026-10-28. Confirmed against the Bacula 15.0.x manual pages Configuring the Director (Pool directives, Volume Retention defaults and the twice-Full-interval minimum, Scratch pool, Cleaning prefix, Purge Oldest Volume), Automated Disk Backup (`LabelMedia`) and Brief Tutorial (Append to Full, Purged, `purge jobs volume`, relabel). Removed: the `label ... slots=` form, `update volume ... volstatus`, `prune volume`, and the status values Error, Archive and Read-Only, none of which the pages show.
Method: documentation only; no commands were run.
