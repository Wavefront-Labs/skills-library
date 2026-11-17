---
id: computing-software.data-engineering.apache-hadoop.hdfs-centralized-cache-management
name: hdfs-centralized-cache-management
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, caching, cacheadmin, locked-memory, zero-copy]
level: advanced
status: docs-checked
description: "HDFS centralized cache management: cache pools and directives, cacheadmin options, dfs.datanode.max.locked.memory with ulimit -l, and refresh settings."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/CentralizedCacheManagement.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centralized cache management

A cache directive names a path to pin in DataNode memory, with a replication factor and expiry. Directories are cached non-recursively (first-level files only). A cache pool groups directives, with UNIX-like permissions (write adds/removes, read lists), an optional byte `-limit` and `-maxTtl`.

```
hdfs cacheadmin -addPool pool1 [-owner o] [-group g] [-mode 0755] [-limit n] [-maxTtl t]
hdfs cacheadmin -addDirective -path /path/to/dir -pool pool1 [-force] [-replication 1] [-ttl 4h]
hdfs cacheadmin -listDirectives [-stats] [-path p] [-pool pool1]
hdfs cacheadmin -removeDirective <id>
hdfs cacheadmin -removePool pool1
```

Replication defaults to 1; `-ttl` takes s, m, h or d and omitted means never expires; `-force` skips pool limit checks. Removing a pool uncaches its paths.

Required config (one of; DRAM cache and persistent-memory cache cannot coexist on one DataNode):
- `dfs.datanode.max.locked.memory` (bytes): cache memory per DataNode, shared with Lazy Persist writes. On Unix-like systems the DataNode user's `ulimit -l` (shown in KB, usually set in `/etc/security/limits.conf`) must be raised to match, otherwise the DataNode refuses to start with an RLIMIT_MEMLOCK error. Leave room for JVM heaps and the OS page cache.
- `dfs.datanode.pmem.cache.dirs`: persistent-memory cache volumes (comma-separated); then `dfs.datanode.max.locked.memory` is not needed. `dfs.datanode.pmem.cache.recovery` controls recovering that cache at DataNode start.

The DataNode needs native code (`libhadoop.so`, or `hadoop.dll` on Windows) to lock block files in memory.

Optional: `dfs.namenode.path.based.cache.refresh.interval.ms` (30000), `dfs.datanode.fsdatasetcache.max.threads.per.volume` (4), `dfs.cachereport.intervalMsec` (10000), `dfs.namenode.caching.enabled` (true; the page recommends disabling it when unused because of added write-lock overhead during rescans).

Clients get a zero-copy read API for cached blocks; the DataNode verifies checksums once. Blocks under construction, corrupt or incomplete are not cached, and symlink targets are not cached.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (CentralizedCacheManagement.md in the apache/hadoop repo). Core claims accurate; added persistent-memory option and caveats, removed an unsupported "Verify" step.
