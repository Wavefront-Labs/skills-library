---
id: computing-software.systems-network-administration.glusterfs.posix-acls
name: posix-acls
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, acl, setfacl, getfacl, mount-option]
level: practitioner
status: docs-checked
description: "Use POSIX ACLs on GlusterFS: mount the brick filesystem and the client with the acl option, then manage entries with setfacl and getfacl."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Access-Control-Lists.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# POSIX ACLs

Enable ACL support on both sides.

Server export partition:

```
mount -o acl /dev/sda1 /export1
```

In `/etc/fstab` add `acl` to the options (for example `rw,acl`).

Client:

```
mount -t glusterfs -o acl 198.192.198.234:glustervolume /mnt/gluster
```

Manage ACLs on the mount:

```
setfacl -m u:antony:rw /mnt/gluster/data/testfile
setfacl -m --set o::r /mnt/gluster/data
getfacl /mnt/gluster/data/test/sample.jpg
setfacl -x u:antony /mnt/gluster/data/test-file
```

Notes:

- Access ACLs apply to files and directories; default ACLs apply only to directories.
- A file without its own ACL inherits the parent's default ACL as its access ACL; a subdirectory inherits it as both default and access ACL.
- Samba has POSIX ACLs enabled by default over a FUSE mount. `setfacl` and `getfacl` also work over NFS.

## Checked

2026-11-04. Confirmed against the glusterdocs Access Control Lists page: mount -o acl on the export partition, the fstab option, the client mount with -o acl, setfacl -m, --set, -x and getfacl examples, access versus default ACLs, inheritance rules, Samba default and NFS support. Removed: the claim about no space after the comma, which the page does not state (its fstab example is spaced).

Method: documentation only; no commands were run.
