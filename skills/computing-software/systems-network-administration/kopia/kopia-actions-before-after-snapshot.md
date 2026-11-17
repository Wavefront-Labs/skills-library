---
id: computing-software.systems-network-administration.kopia.kopia-actions-before-after-snapshot
name: kopia-actions-before-after-snapshot
category: computing-software
field: systems-network-administration
product: kopia
tags: [actions, before-snapshot, after-snapshot, folder-action, zfs, database-dump]
level: advanced
status: docs-checked
description: "Run scripts before and after snapshots or folders in Kopia, enable actions safely, and redirect the snapshot to a point-in-time mount."
sources: ["https://kopia.io/docs/advanced/actions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Actions run commands before or after a snapshot root or an individual folder (v0.8 and later). Uses: ZFS snapshots, database or VM dumps, notifications. They are opt-in because they can run arbitrary code.

## Enable

CLI: pass `--enable-actions` to `repository connect` (global for the client) or override per run with `--force-enable-actions` or `--force-disable-actions` on `snapshot create`. KopiaUI: set `"enableActions": true` in `repository.config` and restart.

## Configure

```console
kopia policy set /some/dir --before-folder-action /path/to/command
kopia policy set /some/dir --after-folder-action /path/to/command
kopia policy set /some/dir --before-snapshot-root-action /path/to/command
kopia policy set /some/dir --after-snapshot-root-action /path/to/command
```

Folder actions are not inherited and must be set on the target folders. Snapshot-root actions inherit from parent policies. `--action-command-mode` is `essential` (must succeed, default), `optional` or `async`. `--action-command-timeout` defaults to 5 minutes. `--persist-action-script` stores a script up to 32000 characters in the repository; it is extracted to a temporary file and run with `sh -e` (or `cmd.exe /c` on Windows), or directly if it starts with `#!`.

## Environment

Before actions receive `KOPIA_ACTION`, `KOPIA_SNAPSHOT_ID`, `KOPIA_SOURCE_PATH`, `KOPIA_SNAPSHOT_PATH` and `KOPIA_VERSION`. After actions get the same, with `KOPIA_SNAPSHOT_PATH` being the path actually snapshotted. A before action can redirect the upload by printing `KOPIA_SNAPSHOT_PATH=<new-directory>` on standard output, which is how a mounted ZFS snapshot is backed up: create the snapshot, mount it, print the path, then unmount and destroy in the after action.

A database example runs `mysqldump SomeDatabase --result-file=$KOPIA_SOURCE_PATH/dump.sql` in a before action with `set -e`.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Actions (v0.8, enabling flags, policy flags, modes, 5 minute default timeout, 32000 character limit, sh -e / cmd.exe /c, environment variables, KOPIA_SNAPSHOT_PATH redirect, ZFS and mysqldump examples).
Method: documentation only; no commands were run.
