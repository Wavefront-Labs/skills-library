---
id: computing-software.systems-network-administration.glusterfs.geo-rep-config-options
name: geo-rep-config-options
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, sync-jobs, rsync-command, use-tarssh]
level: advanced
status: docs-checked
description: "View and change GlusterFS geo-replication session options such as sync-jobs, rsync-command, ssh-command, use-tarssh, ignore-deletes and use-meta-volume."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Geo-Replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo-replication config options

```
gluster volume geo-replication <primary_volume> \
    <secondary_user>@<secondary_host>::<secondary_volume> config [option]
```

With no option it lists all options; with one it shows that option. Changes apply after the session restarts itself automatically; a restart mid-sync may resync some entries already synced.

Examples: `config sync-jobs 3`, `config use-meta-volume true`, `config log-file`.

Options:

- `log-level`, `gluster-log-level`, `changelog-log-level`: log levels.
- `ssh-command`: SSH command (default `ssh`), for a custom path.
- `rsync-command`: rsync command (default `rsync`).
- `use-tarssh true`: tar over SSH, suited to files that are not edited after creation.
- `timeout SECONDS`.
- `sync-jobs N`: number of files and directories synced simultaneously.
- `ignore-deletes`: set to 1 so deletes on the Primary are not applied to the Secondary, which keeps a superset useful for recovery.
- `use-meta-volume true`: workers lock files in the meta volume to choose the Active worker.
- `ssh_port`: custom SSH port (see geo-rep-create-session).

## Checked

2026-11-04. Confirmed against the glusterdocs Geo-Replication page: the config command form, listing and single-option views, automatic restart and resync note, the options table (log levels, ssh-command, rsync-command, use-tarssh, timeout, sync-jobs, ignore-deletes), use-meta-volume and the ssh_port example. Nothing removed.

Method: documentation only; no commands were run.
