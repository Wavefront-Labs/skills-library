---
id: computing-software.systems-network-administration.glusterfs.mount-fuse-client
name: mount-fuse-client
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, fuse, native-client, backupvolfile-server, mount]
level: practitioner
status: docs-checked
description: "Mount a GlusterFS volume with the native FUSE client, with the mount command, mount options such as backupvolfile-server and log-level, and test checks."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Clients.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount with the native FUSE client

The native client is recommended for high concurrency and high write performance.

Load FUSE first: `modprobe fuse`, then `dmesg | grep -i fuse` should show a FUSE init line.

```
mount -t glusterfs HOSTNAME-OR-IPADDRESS:/VOLNAME MOUNTDIR
mount -t glusterfs server1:/test-volume /mnt/glusterfs
```

Create the mount point first if you see a "Usage: mount.glusterfs" message.

Options go after `-o`, comma separated:

- `backupvolfile-server`: fallback server to fetch the volfile from.
- `volfile-max-fetch-attempts`: number of fetch attempts (useful with round-robin DNS).
- `log-level`, `log-file`, `transport`.
- `direct-io-mode`: `enable` or `disable`.
- `use-readdirp`: `yes` or `no`.

Notes:

- Server names used at volume creation must resolve on the client.
- The server in the mount command only supplies the volfile; the client then talks directly to the servers it lists.

Test: `mount` lists type `fuse.glusterfs`, and `df -h /mnt/glusterfs` shows the aggregated space.

## Checked

2026-11-04: the FUSE module check, mount command, usage-message note, option list, backupvolfile-server and volfile-max-fetch-attempts behaviour, name resolution note, volfile-only note and mount/df tests were read against the glusterdocs page Setting-Up-Clients. Nothing removed.

Method: documentation only; no commands were run.
