---
id: computing-software.systems-network-administration.ceph.cephfs-quotas
name: cephfs-quotas
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephfs, quota, max-bytes, max-files, setfattr]
level: practitioner
status: docs-checked
description: "Set CephFS directory quotas with ceph.quota extended attributes."
sources:
  - https://docs.ceph.com/en/latest/cephfs/quota/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CephFS quotas are virtual extended attributes on directories: `ceph.quota.max_bytes` (byte limit) and `ceph.quota.max_files` (file limit). The quota restricts the bytes or files stored beneath that directory.

```
setfattr -n ceph.quota.max_bytes -v 100000000 /some/dir
setfattr -n ceph.quota.max_files -v 10000 /some/dir
setfattr -n ceph.quota.max_bytes -v 5Gi /some/dir
```

`ceph.quota.max_bytes` also accepts human-friendly units such as `100K` and `5Gi`; values are strictly cast to IEC units even for SI input, so `1K` becomes 1024 bytes. If the attributes appear on a directory a quota is set there; if absent, a quota may still be set on a parent.

Read a value with `getfattr -n ceph.quota.max_bytes /some/dir`. Listing with `getfattr -d -m -` prints none of the CephFS attributes because the clients hide them from `listxattr(2)`; name the attribute explicitly.

Remove a quota with `setfattr -x ceph.quota.max_bytes /some/dir` or by setting the value to `0`.

A client needs the `p` flag in its authentication capabilities, in addition to `rw`, to set a quota (see the CephFS client capabilities page, layout and quota restriction).

Space reporting: when the mount root has a quota, `df` and similar tools report available space as quota limit minus used space. Disable with `client quota df = false` in the client section of `ceph.conf`.

Limitations from the page:

- Quotas are cooperative and non-adversarial: they rely on the mounting client to stop writers, so a modified or adversarial client cannot be prevented from writing.
- Quotas are imprecise: writers are stopped a short time after the limit is crossed, generally within tens of seconds, so some overshoot is inevitable.
- Supported by the userspace client (libcephfs, `ceph-fuse`) and by Linux kernel clients 4.17 and higher, the latter only on mimic or newer clusters.
- With path-based mount restrictions, the client needs access to the directory inode carrying the quota (a kernel client also needs access to its parent), otherwise it will not enforce it. Configure the quota on the directory the client is restricted to or something nested beneath it.
- Deleted or changed snapshot file data does not count towards the quota, so snapshots can retain space beyond it; `ceph fs set <fs_name> allow_new_snaps false` disables creating new snapshots.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "CephFS Quotas" on docs.ceph.com. Removed the unsupported "plain rw may be refused" hedge in favour of the page's wording on the `p` flag.
