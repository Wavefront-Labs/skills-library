---
id: computing-software.systems-network-administration.glusterfs.mount-nfsv3
name: mount-nfsv3
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, nfsv3, mountproto, nfs-client, gnfs]
level: practitioner
status: docs-checked
description: "Mount a GlusterFS volume over NFSv3 with mount -t nfs -o vers=3, force TCP with mountproto=tcp, the Solaris URL form, and the no-UDP and no-NFSv4 limits."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Clients.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-gnfs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount over NFSv3

```
mount -t nfs -o vers=3 HOSTNAME-OR-IPADDRESS:/VOLNAME MOUNTDIR
mount -t nfs -o vers=3 server1:/test-volume /mnt/glusterfs
```

- Gluster NFS does not support UDP. If the client defaults to UDP you get "requested NFS version or transport protocol is not supported". Add `mountproto=tcp`: `mount -o mountproto=tcp -t nfs server1:/test-volume /mnt/glusterfs`.
- Solaris: `mount -o proto=tcp,vers=3 nfs://HOSTNAME-OR-IPADDRESS:38467/VOLNAME MOUNTDIR`.
- Debian-based systems need `nfs-common` on servers and clients.
- Gluster NFS includes NLM v4 for record locking.
- NFSv4 is not supported. A mount that times out can mean the client is using v4; force `-o vers=3`.
- "rpc.statd is not running" at mount: run `rpc.statd` on the client, or mount with `nolock`.

Test: `mount` shows an entry like `server1:/test-volume on /mnt/glusterfs type nfs (rw,vers=3,addr=server1)`.

For fstab, see fstab-automount. For ports, see firewall-ports.

## Checked

2026-11-04: the mount commands, no-UDP error and mountproto=tcp, the Solaris form, nfs-common, NLM v4, the version 3 only limit with the timeout fix, and the rpc.statd or nolock error were read against the glusterdocs pages Setting-Up-Clients and troubleshooting-gnfs. Nothing removed.

Method: documentation only; no commands were run.
