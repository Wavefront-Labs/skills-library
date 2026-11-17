---
id: computing-software.systems-network-administration.glusterfs.geo-rep-faulty-eoferror
name: geo-rep-faulty-eoferror
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, geo-replication, faulty, eoferror, rsync]
level: advanced
status: docs-checked
description: "Troubleshoot GlusterFS geo-replication: Faulty status with EOFError tracebacks, files not syncing (rsync 3.0.0+), log file lookup and log rotation."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-georep.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo-replication troubleshooting

Find the Primary log file for a session:

```
gluster volume geo-replication <session> config log-file
```

Rotate logs (current log is backed up with a timestamp):

```
gluster volume geo-replication Volume1 example.com:/data/remote_dir log rotate
gluster volume geo-replication Volume1 log rotate
gluster volume geo-replication log rotate
```

Success prints `log rotate successful`.

Status often Faulty with an `EOFError` raised from `repce.py` `recv`: the RPC link between the Primary and Secondary gsyncd is broken. Check:

- Passwordless SSH works between hosts.
- FUSE is installed.
- A Secondary volume is started; a Secondary directory exists with correct permissions.
- If Gluster is installed in a custom location, set `gluster-command` (Primary) or `remote-gsyncd-command` (Secondary) to the exact path.

Status OK but only directories and symlinks sync, with `GMaster: failed to sync` in the log: install rsync 3.0.0 or higher on both Primary and remote host.

To force a complete resync, erase the index and restart geo-replication; every file is compared by checksum, which is slow on large data sets. The page does not give the exact commands.

## Checked

2026-11-04. Confirmed against the glusterdocs Troubleshooting geo-replication page: config log-file, the three log rotate forms and the success message, the Faulty EOFError cause and its checklist (SSH, FUSE, Secondary volume or directory, gluster-command, remote-gsyncd-command), rsync 3.0.0 or higher, and the erase-the-index full resync note. Nothing removed.

Method: documentation only; no commands were run.
