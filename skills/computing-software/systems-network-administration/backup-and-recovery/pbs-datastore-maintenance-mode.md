---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-datastore-maintenance-mode
name: pbs-datastore-maintenance-mode
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-maintenance-mode, proxmox-backup-server, datastore-maintenance, pbs, removable-datastore, storage-maintenance]
level: practitioner
status: docs-checked
description: "Put a Proxmox Backup Server datastore into read-only or offline maintenance mode for storage work or removable datastores, and clear it afterwards."
sources:
  - https://pbs.proxmox.com/docs/maintenance.html
  - https://pbs.proxmox.com/docs/storage.html#datastore-maintenance-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS datastore maintenance mode

**Goal:** block new reads and/or writes to a datastore cleanly before storage work, letting operations already in progress finish.

## Modes
| Mode | Effect |
|---|---|
| `read-only` | only read operations are allowed on the datastore |
| `offline` | neither read nor write operations are allowed |
PBS tracks whether each datastore access is a read or a write, so it enters a mode gracefully: conflicting operations that started before the mode was enabled are allowed to finish. The documentation's stated purpose is to let an administrator safely run maintenance, for example on the underlying storage.

## Setting and clearing
- Web UI: maintenance mode is one of the per-datastore options (Options in the datastore's settings).
- CLI (the form shown in the Removable Datastores section of the storage page, which omits the datastore name; add it as for other `datastore update` calls):
```sh
proxmox-backup-manager datastore update <datastore> --maintenance-mode offline   # block all IO
proxmox-backup-manager datastore update <datastore> --delete maintenance-mode    # clear it
```
The documentation shows the CLI only for `offline` and for clearing; set `read-only` in the web UI.

## Removable datastores
Removable datastores have a backing device and can be mounted and unmounted; otherwise they behave like normal datastores. Unmount through the UI ("Unmount" on the summary page) or the CLI:
```sh
proxmox-backup-manager datastore unmount store1
```
This waits for running tasks to finish and unmounts the device. If unmounting fails, the reason is logged in the unmount task log and the datastore stays in maintenance mode `unmounting`, which prevents any IO; reset it manually with the two `--maintenance-mode offline` / `--delete maintenance-mode` commands above. Removable datastores are mounted under `/mnt/datastore/<name>`. Creating a datastore on FAT file systems is not supported.

## Related
Clearing a datastore's GC schedule (`--delete gc-schedule`) disables automatic garbage collection, which the documentation suggests for example during maintenance.

## Checked
2026-11-07. Read in full: the Maintenance Mode section of the PBS Maintenance Tasks page (also read the Scheduled GC and Verification sections) and, from the Storage page, the Removable Datastores section and the datastore Options list; the rest of the Storage page was not read. The command-syntax page contains no `--maintenance-mode` entry in the fetched text. Removed as unconfirmed: the claim that read-only still allows verify and sync-from and refuses prune/GC, "GUI shows a maintenance icon", `task list`, the zfs send/datastore.cfg migration recipe, "PBS 3.3+", disabling the vzdump job advice, behaviour of PVE jobs and GC/verify jobs during read-only, the `--maintenance-mode read-only` CLI form and the invented Verify step.
Method: documentation only; no commands were run.
