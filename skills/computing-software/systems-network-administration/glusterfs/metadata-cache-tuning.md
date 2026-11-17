---
id: computing-software.systems-network-administration.glusterfs.metadata-cache-tuning
name: metadata-cache-tuning
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, metadata-cache, inode-lru-limit, md-cache, performance]
level: advanced
status: docs-checked
description: "Tune GlusterFS metadata and directory performance: the metadata-cache and nl-cache option groups, inode LRU limit, readdir-ahead, and small-file cache invalidation."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Performance-Tuning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata cache tuning

Enable metadata caching with invalidation (caches stat and xattr data, refreshed every 10 minutes):

```
gluster volume set <volname> group metadata-cache
gluster volume set <volname> network.inode-lru-limit 50000
```

- Helps most workloads, but not those where many clients access the same files at once.
- A higher `network.inode-lru-limit` raises brick process memory use; raise it for volumes with very many active files.
- Samba: `cache-samba-metadata on`. Extra xattrs: `xattr-cache-list` with a comma-separated list such as `user.org.netatalk.*,user.swift.metadata`. Capability xattrs, IMA xattrs and ACLs are cached by default.

Directory listing: use together with metadata caching:

```
performance.readdir-ahead on
performance.parallel-readdir on
```

File and directory creation: enable `group nl-cache`, then `nl-cache-positive-entry on` (the group also enables cache invalidation and a 10 minute timeout).

Small-file reads: `performance.cache-invalidation on`, `features.cache-invalidation on`, `performance.qr-cache-timeout 600`, `cache-invalidation-timeout 600`. Files of 64KB or smaller are cached by default; change with `performance.cache-max-file-size`. Sizes use SI suffixes such as `64KB`.

## Checked

2026-11-04. Confirmed against the glusterdocs Performance Tuning page: group metadata-cache and its 10 minute refresh, inode-lru-limit 50000 and memory note, cache-samba-metadata, xattr-cache-list and its example, readdir-ahead and parallel-readdir, group nl-cache with nl-cache-positive-entry, the small-file read options, the 64KB default and cache-max-file-size. Nothing removed.

Method: documentation only; no commands were run.
