---
id: computing-software.systems-network-administration.syncthing.versioning-restore-and-paths
name: versioning-restore-and-paths
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, versioning, fspath, restore]
level: practitioner
status: docs-checked
description: "Place Syncthing version archives with fsPath and fsType, and know which settings each versioning strategy honours."
sources: ["https://docs.syncthing.net/users/versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Versions folder location and options

## Where versions live
The default is `.stversions` inside the shared folder. Override it with `folder.versioning.fsPath`:
- An absolute path is used as is.
- A relative path is resolved against the folder path when `fsType` is `basic`.
- It should be on the same partition or filesystem as the folder, since moving files across filesystems may fail.

`folder.versioning.fsType` selects the filesystem implementation for the versions folder. It only applies when `fsPath` is non-empty. Otherwise the folder's `filesystemType` is used.

## Option summary
| Option | Meaning |
|---|---|
| `type` | `trashcan`, `simple`, `staggered`, `external`, or empty for none |
| `cleanupIntervalS` | cleanup period in seconds, `0` disables, max 31536000 |
| `params.cleanoutDays` | days to keep, `0` forever |
| `params.keep` | versions per file (simple) |
| `params.maxAge` | seconds to keep (staggered), `0` forever |
| `params.command` | external command |

`fsPath`, `fsType` and `cleanupIntervalS` are ignored by the external strategy.

## Older configs
`fsPath`, `fsType` and `cleanInterval` used to be stored inside `params`. Current configuration keeps them as direct children of `versioning`.

## Reminder
Versions are created only for changes received from other devices, never for local edits.

## Checked

2026-11-09. Confirmed against the Syncthing File Versioning page (users/versioning, raw rst from syncthing/docs), Configuration Parameter Reference section: type values, fsPath default and absolute/relative rules, fsType scope, cleanupIntervalS meaning and one-year limit, cleanoutDays, keep, maxAge, command, the list of options ignored for external, the old params locations, remote-changes-only note. Removed: nothing (the page has no restore procedure, and the skill does not claim one).

Method: documentation only; no commands were run.
