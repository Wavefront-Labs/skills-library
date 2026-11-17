---
id: computing-software.systems-network-administration.syncthing.seed-initial-sync-by-copy
name: seed-initial-sync-by-copy
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, initial-sync, seeding, large-folders]
level: practitioner
status: docs-checked
description: "Pre-seed a large Syncthing folder by copying files manually before sharing so only differences travel the network."
sources: ["https://docs.syncthing.net/users/faq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seeding an initial sync

Use this when a large folder must reach a remote device over a slow network and you can move the data physically.

## Steps
1. Create the folder on the local device, but do not share it with the remote device yet.
2. Copy the files to the remote machine with normal file copy tools. If this takes long, make sure the files on the local device are not updated meanwhile.
3. On the remote device, create the folder with the same Folder ID as the local one. Copy the ID from the local folder dialog, because matching IDs make them the same folder. Point it at the copied files and wait until scanning is done.
4. Share the folder on both sides. Syncthing exchanges file information and updates its database. Existing files are not transferred again. This can still take a while at first, so wait until it settles.

## Tips
- Match the Folder ID exactly, or the two sides are treated as different folders.
- The same method helps when moving a synced folder: remove it in the GUI, move it on disk, re-add it at the new path, only when everything is already in sync. Otherwise it is unpredictable which changes win.

## Checked

2026-11-09. Confirmed against the Syncthing FAQ usage part (users/faq-parts/usage, raw rst from syncthing/docs): the four-step manual-copy procedure and the rename/move-a-synced-folder answer. Removed: the "Why it works" section on block-list comparison and the "ideally" hedge around moving (block lists are described on users/syncing but not tied to this FAQ procedure); added the wait-for-scan step and the do-not-modify note from the page.

Method: documentation only; no commands were run.
