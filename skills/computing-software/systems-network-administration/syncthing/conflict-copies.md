---
id: computing-software.systems-network-administration.syncthing.conflict-copies
name: conflict-copies
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, conflicts, sync-conflict, maxconflicts]
level: practitioner
status: docs-checked
description: "Handle Syncthing sync-conflict files, understand which version loses, and limit copies with maxConflicts."
sources: ["https://docs.syncthing.net/users/syncing.html", "https://docs.syncthing.net/users/config.html", "https://docs.syncthing.net/users/foldertypes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sync conflicts

## What happens
When a file is modified on two devices at once and the contents differ, one version is renamed to:

`<filename>.sync-conflict-<date>-<time>-<modifiedBy>.<ext>`

## Which one loses
- The file with the older modification time becomes the conflict copy.
- If the times are equal, the file from the device with the larger first 63 bits of its device ID loses.
- If a modification conflicts with a deletion and the deletion wins, the file is renamed to a conflict copy too.

## Propagation
Conflict copies are ordinary files once created, so they sync to every device. The conflict was detected on one device, but it is equally a conflict everywhere, and Syncthing cannot tell which version a person prefers.

## Limiting copies
`maxConflicts` is the maximum number of conflict copies kept around for any given file. The config page text says the default is `10`, `-1` means unlimited and `0` disables conflict copies altogether. Its example XML blocks are inconsistent (some show `-1`, the folder example shows `10`), so check the value your version actually uses.

## Receive only folders
A locally modified file that is subsequently modified by the cluster causes a sync conflict, resolved with the cluster version as the winner. In a receive-only folder the sync conflict copy is not sent to the cluster, and it is deleted if Revert Local Changes is used.

## Checked
2026-11-04. Read Understanding Synchronization (conflicts section), the config page (`maxConflicts`) and Folder Types (receive-only conflicts). Name pattern, older-mtime rule, 63-bit device ID tiebreak, deletion-wins case, propagation as normal files, and the `maxConflicts` values are confirmed; noted that the config page's own XML examples disagree on the default. Removed the closing "Practice" advice, which no page states.
Method: documentation only; no commands were run.
