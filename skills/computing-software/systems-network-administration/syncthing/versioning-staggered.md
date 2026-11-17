---
id: computing-software.systems-network-administration.syncthing.versioning-staggered
name: versioning-staggered
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, versioning, staggered, maxage]
level: practitioner
status: docs-checked
description: "Set up staggered versioning in Syncthing so old versions thin out over time and expire at a maximum age."
sources: ["https://docs.syncthing.net/users/versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Staggered file versioning

## How the intervals work
Staggered versioning moves replaced or deleted files into `.stversions` like simple versioning, but prunes them by age. Each interval keeps at most one version, always the oldest one in that interval, which preserves a file that was overwritten recently:
- first hour: one version per 30 seconds
- first day: one per hour
- first 30 days: one per day
- until maximum age: one per week

Versions older than the maximum age are deleted.

## Configuration
```xml
<versioning type="staggered">
  <cleanupIntervalS>3600</cleanupIntervalS>
  <param key="maxAge" val="31536000"></param>
</versioning>
```
- `params.maxAge` is stored in seconds in the configuration. The GUI field is in days (365 keeps a year, 10 keeps ten days).
- `maxAge` of `0` keeps versions forever, so the folder can grow without bound.
- `fsPath` and `fsType` work as for the other strategies. Keep the versions folder on the same filesystem.
- `cleanupIntervalS` controls how often pruning runs. It is limited to one year, and `0` disables it.

## Gotcha
Because only remote changes are archived, a device that only edits locally builds no history of its own. Configure staggered versioning on the devices that receive changes.

## Checked

2026-11-09. Confirmed against the Syncthing File Versioning page (users/versioning, raw rst from syncthing/docs): the four intervals and oldest-version rule, maxAge in seconds in config and days in the GUI, 0 meaning forever, cleanupIntervalS limit of one year and 0 disabling it, same-filesystem advice, remote-changes-only note. Removed: nothing.

Method: documentation only; no commands were run.
