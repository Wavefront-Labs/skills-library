---
id: computing-software.systems-network-administration.glusterfs.netgroup-export-auth
name: netgroup-export-auth
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, netgroup, exports-auth, nfs-exports-auth-enable, gnfs]
level: advanced
status: docs-checked
description: "Restrict Gluster NFS mounts per host or netgroup with the export and netgroup files and nfs.exports-auth-enable; file formats, refresh options and validation."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Export-And-Netgroup-Authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NFS export and netgroup authentication

Files (create on every node of the pool before enabling):

- `/var/lib/glusterd/nfs/export`: which hosts or netgroups may mount which exports.
- `/var/lib/glusterd/nfs/netgroup`: expands netgroups referenced in the export file.

Export line:

```
/<export path> <host/netgroup> (options),..
```

A name prefixed with `@` is a netgroup; `*` allows any client. Options named include `sec`, `ro`/`rw` and `anonuid`.

Netgroup lines map a netgroup to nested netgroups, ending in IPs:

```
<netgroup name> ng1000
ng1000 ng999
ng2 (ip1,ip2,..)
```

Volume options:

```
gluster volume set <volname> nfs.exports-auth-enable on
gluster volume set <volname> nfs.auth-refresh-interval-sec <seconds>
gluster volume set <volname> nfs.auth-cache-ttl-sec <seconds>
```

Validate before applying:

```
glusterfsd --print-netgroups <file>
glusterfsd --print-exports <file>
```

Caveats: not every exports(5) option is supported; files are maintained by hand so nodes can disagree; do not combine with `nfs.rpc-auth-allow` or `nfs.export-dir`. If changes do not take effect, stop and start the volume to force a re-read.

## Checked

2026-11-04. Confirmed against the glusterdocs Export and Netgroup Authentication page: file paths, export line format, @ for netgroups, * for any client, the sec, ro/rw and anonuid options, netgroup chain format, the three volume options, the glusterfsd print flags, and the four caveats plus the stop-and-start troubleshooting. Nothing removed.

Method: documentation only; no commands were run.
