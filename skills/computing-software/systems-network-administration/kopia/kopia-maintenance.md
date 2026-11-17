---
id: computing-software.systems-network-administration.kopia.kopia-maintenance
name: kopia-maintenance
category: computing-software
field: systems-network-administration
product: kopia
tags: [maintenance, quick-maintenance, full-maintenance, gc, maintenance-owner, safety]
level: advanced
status: docs-checked
description: "Understand Kopia quick and full maintenance, the maintenance owner, scheduling and the safety flag."
sources: ["https://kopia.io/docs/advanced/maintenance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since v0.6.0 maintenance is automatic and runs occasionally when the CLI is used.

- **Quick maintenance** keeps the number of frequently accessed blobs (`q` and `n`) low and never deletes metadata without ensuring another copy exists. Enabled by default, about hourly. Disabling it hurts performance.
- **Full maintenance** keeps the repository compact and removes deleted data. Its key task is snapshot GC, which marks contents unreachable from any active snapshot, and it compacts `p` data blobs.

## Owner

Only one `user@hostname` is the maintenance owner and only it runs maintenance automatically.

```console
kopia maintenance info
kopia maintenance set --owner=me
kopia maintenance set --owner=another@somehost
```

## Scheduling

```console
kopia maintenance set --enable-quick true
kopia maintenance set --enable-full true
kopia maintenance set --quick-interval=2h
kopia maintenance set --full-interval=8h
kopia maintenance set --pause-quick=48h
kopia maintenance set --pause-full=268h
```

Run manually as the owner with `kopia maintenance run` (quick) or `kopia maintenance run --full`. `kopia maintenance info` also shows the history of the last five runs.

## Safety

Maintenance depends on elapsed time so other clients' caches and in-flight operations can settle, which means full maintenance may take several hours or several cycles to actually remove unused blobs. Kopia 0.8 added `kopia maintenance run --full --safety=none`, which skips those protections; use it only if you can guarantee no snapshots are being created and storage is in sync, because otherwise it can corrupt the repository.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Maintenance page (v0.6.0 automatic maintenance, quick and full tasks, owner commands, scheduling flags, manual run, v0.8 --safety=none and its warning, history of the last 5 runs).
Method: documentation only; no commands were run.
