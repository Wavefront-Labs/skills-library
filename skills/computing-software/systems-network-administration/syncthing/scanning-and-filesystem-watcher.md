---
id: computing-software.systems-network-administration.syncthing.scanning-and-filesystem-watcher
name: scanning-and-filesystem-watcher
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, scanning, fswatcher, rescan]
level: practitioner
status: docs-checked
description: "Tune Syncthing scanning with rescanIntervalS, fsWatcherEnabled and fsWatcherDelayS, and know why watcher changes lag."
sources: ["https://docs.syncthing.net/users/syncing.html", "https://docs.syncthing.net/users/config.html", "https://docs.syncthing.net/rest/db-scan-post.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scanning and the filesystem watcher

## Two detection methods
Syncthing finds local changes by periodic full scans and by filesystem notifications (the watcher). By default the watcher is on and a full scan runs hourly. Both are per-folder settings.

| Option | Meaning |
|---|---|
| `folder.rescanIntervalS` | rescan interval in seconds; 0 disables it when external plugins trigger rescans (default 3600 in the config examples) |
| `folder.fsWatcherEnabled` | detects changes to files in the folder and scans them |
| `folder.fsWatcherDelayS` | duration during which detected changes are accumulated before a scan is scheduled (10s by default; only takes effect if the watcher is enabled) |
| `folder.fsWatcherTimeoutS` | maximum delay before a scan when a file is continuously changing; if unset or zero a default is calculated from fsWatcherDelayS |

## Details
- The actual scan interval is a random time between 3/4 and 5/4 of the given interval, so that not all folders are rescanned at the same time.
- Even with the watcher enabled it is advised to keep regular full scans enabled, as some changes may not be picked up by the watcher.
- During a rescan (full or from the watcher) existing files are checked for changes to modification time, size or permission bits. If a change is detected the file is rehashed, that is a new block list is calculated.
- The watcher accumulates changes for 10s (adjustable by fsWatcherDelayS) and deleted files are further delayed for 1min, so a slight delay before the change appears on another device is expected.
- Increasing the full scan interval uses fewer resources and is useful, for example, on large folders that change infrequently.

## Trigger a scan manually
```sh
curl -X POST -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/db/scan?folder=default&sub=docs"
```
`folder` omitted or empty scans all folders. `sub` is a path relative to the folder root; only that path (and its children, for a directory) is scanned. Requesting a scan of a path that no longer exists, but previously did, makes Syncthing notice the deletion. `next` (seconds) delays the automated rescan interval. Success returns 200 with no content, or 500 with a plain text error.

## Checked
2026-11-04. Read Understanding Synchronization (Scanning), the config page folder element and POST /rest/db/scan: the two detection methods, defaults, random interval range, rehash attributes, watcher delays, option meanings and scan parameters match. Added fsWatcherTimeoutS and the `next` parameter from the pages.
Method: documentation only; no commands were run.
