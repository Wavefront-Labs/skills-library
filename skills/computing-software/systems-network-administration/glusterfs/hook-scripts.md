---
id: computing-software.systems-network-administration.glusterfs.hook-scripts
name: hook-scripts
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, hook-scripts, glusterd-hooks, samba-hooks, lifecycle]
level: advanced
status: docs-checked
description: "Attach pre and post hook scripts to GlusterFS volume events under /var/lib/glusterd/hooks/1: directory layout, S-prefix naming, arguments and the Samba hooks."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Hook-scripts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume lifecycle hook scripts

Each supported event can have a pre script (before) and a post script (after). Events: create, start, add-brick, remove-brick, set, stop, delete.

Directories (one per event) are created with the pool:

```
/var/lib/glusterd/hooks/1/create/
/var/lib/glusterd/hooks/1/delete/
/var/lib/glusterd/hooks/1/start/
/var/lib/glusterd/hooks/1/stop/
/var/lib/glusterd/hooks/1/set/
/var/lib/glusterd/hooks/1/add-brick/
/var/lib/glusterd/hooks/1/remove-brick/
```

The examples imply `pre` and `post` subdirectories, such as `/var/lib/glusterd/hooks/1/start/post` and `/var/lib/glusterd/hooks/1/stop/pre`.

Rules:

- The script name must begin with `S` to be enabled; scripts run in lexicographic order.
- Install the script on every node of the trusted pool.
- Arguments: all get `--volname=VOLNAME`; start adds `--first=yes|no`; stop adds `--last=yes|no`; set adds `-o key=value` for each option.

Prepackaged Samba hooks (enabled by default): `S30samba-start.sh` (start/post) adds the volume's share to `smb.conf`, FUSE-mounts it with an fstab entry and restarts Samba; `S30samba-stop.sh` (stop/pre) reverses this.

## Checked

2026-11-04: the event list, the seven hook directories, the S-prefix and lexicographic order rule, the install-on-all-nodes rule, the per-event arguments and the prepackaged Samba scripts were read against the glusterdocs page Hook-scripts. Reworded `uppercase S` to `S` as the page says, and removed the line about exit codes, which was a statement about the page rather than about Gluster.

Method: documentation only; no commands were run.
