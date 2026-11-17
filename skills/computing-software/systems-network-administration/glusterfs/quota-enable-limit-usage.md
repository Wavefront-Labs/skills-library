---
id: computing-software.systems-network-administration.glusterfs.quota-enable-limit-usage
name: quota-enable-limit-usage
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, quota, limit-usage, hard-limit, quota-list]
level: practitioner
status: docs-checked
description: "Enable directory quota on a GlusterFS volume, set limit-usage on a directory, list and remove limits, and disable quota; only hard limits are enforced."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Directory-Quota.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable quota and set limits

```
gluster volume quota <VOLNAME> enable
gluster volume quota <VOLNAME> limit-usage <DIR> <HARD_LIMIT>
gluster volume quota <VOLNAME> list [<DIR>]
gluster volume quota <VOLNAME> remove <DIR>
gluster volume quota <VOLNAME> disable
```

Example: `gluster volume quota test-volume limit-usage /data 10GB` prints `Usage limit has been set on /data`.

- Quota must be enabled before limits can be set.
- `<DIR>` is relative to the volume root, so the mount point is `/`.
- A limit can be set on an empty directory and applies once files are added.
- Only hard limits are supported; writes beyond the limit are denied. In nested directories the strictest limit applies.
- `list` shows Path, Hard-limit, Soft-limit, Used and Available.
- The first limit creates an auxiliary mount under `/var/run/gluster/<VOLNAME>`, which stays until quota is disabled.

Cache timeouts are in quota-timeouts-alert.

## Checked

2026-11-04. Confirmed against the glusterdocs Directory Quota page: enable, disable, limit-usage, list and remove commands and messages, hard limits only, limits on empty directories, strictest limit in nested directories, paths relative to the volume root, the list columns and the auxiliary mount under /var/run/gluster/<VOLNAME>. Removed: the quota log file names, which the page does not mention.

Method: documentation only; no commands were run.
