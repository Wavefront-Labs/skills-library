---
id: computing-software.systems-network-administration.syncthing.case-sensitivity-conflicts
name: case-sensitivity-conflicts
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, case-sensitivity, case-conflict, casesensitivefs]
level: advanced
status: docs-checked
description: "Resolve Syncthing case conflicts between case-sensitive and case-insensitive systems, and know when caseSensitiveFS is safe."
sources: ["https://docs.syncthing.net/users/syncing.html", "https://docs.syncthing.net/users/tuning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case sensitivity in file names

## Rule
Syncthing treats paths as case-sensitive, so `file.txt` and `FILE.txt` are independent. Windows, macOS and (partly) Android treat them as one name and cannot hold both.

## What you see
If a remote device shares a name that clashes with an existing local file, it is not synchronized and appears as a case conflict. If two remote devices offer differing case variants, only one is pulled and the other gets an error. Which one wins is not predictable.

## Fixing it
Decide on one consistent name and rename the files manually on every case-insensitive device involved. The cautious behaviour is meant to prevent data loss from different files overwriting each other's contents. Before version 1.9.0 the same file could be wrongly accessed under two names.

The folder root path itself is unaffected. Only relative paths inside a shared folder matter.

## The caseSensitiveFS option
Per-folder `caseSensitiveFS` disables the safety checks needed for case-insensitive filesystems and can improve performance. Only enable it when the folder really sits on a case-sensitive filesystem. On a case-insensitive one it can cause data loss.

## Checked
2026-11-04. Read Understanding Synchronization (case sensitivity section) and Configuration Tuning (caseSensitiveFS entries): case-sensitive paths, Windows/Mac/Android to an extent, case conflict report, only one of two remote variants pulled and not predictable, manual rename on case-insensitive devices, behaviour before 1.9.0, folder root unaffected, caseSensitiveFS performance and data-loss warning. Removed the generic closing tip and the claim that Syncthing deliberately declines to choose.
Method: documentation only; no commands were run.
