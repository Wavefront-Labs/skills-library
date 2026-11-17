---
id: computing-software.systems-network-administration.syncthing.versioning-trashcan
name: versioning-trashcan
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, versioning, trashcan, stversions]
level: intro
status: docs-checked
description: "Enable trash can file versioning in Syncthing and set cleanoutDays so replaced or deleted files are kept in .stversions for a limited time."
sources: ["https://docs.syncthing.net/users/versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trash can versioning

## What it does
When a file is deleted or replaced because of a change that arrived from another device, Syncthing moves the old copy into the folder's `.stversions` directory instead of discarding it. If a file with the same name is already in the trash can, it is replaced, so only the latest old version of each file is kept.

## Settings
- `folder.versioning.type` is `trashcan`.
- `folder.versioning.params.cleanoutDays` removes trash items older than that many days. `0` means never clean automatically.
- `folder.versioning.fsPath` overrides the default `.stversions` location. Keep it on the same filesystem as the folder, because moving files across partitions may fail.
- `folder.versioning.cleanupIntervalS` sets how often the cleanup runs, in seconds. `0` turns periodic cleaning off.

```xml
<versioning type="trashcan">
  <cleanupIntervalS>3600</cleanupIntervalS>
  <param key="cleanoutDays" val="30"></param>
</versioning>
```

## Limits worth knowing
Versioning only applies to changes received from other devices. If you edit or delete a file on your own device, that device cannot archive the old copy. Versioning is configured per folder on each device, and the default is no versioning at all, so a device that should keep history must be configured explicitly.

## Checked

Method: docs-checked 2026-11-09 against docs.syncthing.net/users/versioning (read as raw reStructuredText from the syncthing/docs repository, including its configuration parameter reference); documentation only, no commands were run.

Confirmed: the trash can move into `.stversions` with same-name replacement, `cleanoutDays` (zero never cleans), the `fsPath` default and same-filesystem advice, `cleanupIntervalS` with zero disabling periodic cleaning, the XML layout, that versioning applies only to changes received from other devices, and that the default is no versioning.

Removed: the closing sentence about restoring files through the GUI versions dialog or REST versions endpoints, which those pages do not cover.
