---
id: computing-software.data-engineering.apache-hadoop.hdfs-viewfs-mount-tables
name: hdfs-viewfs-mount-tables
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, viewfs, federation, mount-table, namespaces]
level: advanced
status: docs-checked
description: "ViewFs client-side mount tables: fs.defaultFS viewfs, fs.viewfs.mounttable link keys, linkFallback, linkMergeSlash, rename limits, nfly and regex links."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ViewFs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ViewFs

ViewFs manages several Hadoop file system namespaces, like client-side mount tables on Unix. It implements the Hadoop file system interface, so shell commands work with it, but it is a trivial file system that only links to other file systems.

Set `fs.defaultFS` to `viewfs://clusterX`; the authority is the mount table name, and the page recommends naming the table after the cluster. Gateways and service machines should contain the mount tables of all clusters (needed for e.g. distcp). Mount keys all start with `fs.viewfs.mounttable.`:

```
fs.viewfs.mounttable.clusterX.link./data  =  hdfs://nn1-clusterx.example.com:8020/data
fs.viewfs.mounttable.clusterX.linkFallback  =  hdfs://nn5-clusterx.example.com:8020/home
```

Link types:
- `link`: mount a path onto a target filesystem (keep mount point names the same as the target locations).
- `linkFallback`: namespaces not in the table fall back to a default filesystem.
- `linkMergeSlash`: merges the table's root with another filesystem's root (e.g. `fs.viewfs.mounttable.clusterY.linkMergeSlash`).
- `linkNfly`: one logical file synchronously replicated across several filesystems, meant for small files (up to about a gigabyte), with logic in a single client JVM. Key form `fs.viewfs.mounttable.global.linkNfly.<params>./ads` with a comma-separated URI list (two dots appear when params are empty). Params: `minReplication` (default 2; must not exceed the number of URIs), `readMostRecent`, `repairOnRead`. Creation writes an invisible `_nfly_tmp_<name>` on each target then renames; temp files can be left behind if the client crashes, so the page suggests a cron job to purge them. Reads go to the "closest" URI using rack-awareness-style topology mapping.
- `linkRegx`: rule-based mounts, key `fs.viewfs.mounttable.<table>.linkRegx.<regex>` with a Java named group substituted into the target, e.g. `^(?<username>\\w+)` mapping to `gs://${username}.hadoop.apache.org/`. Optional interceptors (`replaceresolveddstpath:_:-#.` prefix) replace strings in the resolved target. The page sets `fs.viewfs.rename.strategy` to `SAME_FILESYSTEM_ACROSS_MOUNTPOINT` in this section.

Mounting below the top level (for example `/user/joe` and `/user/jane`) makes `/user` an internal read-only directory.

Rename: files and directories cannot be renamed across namenodes or clusters; a rename between mount points on different namenodes (e.g. `/user` to `/data`) fails.

Keep the table in a separate file (e.g. `mountTable.xml`) pulled into `core-site.xml` by XInclude; the page prefers fetching it over HTTP from a central place. The mount table is read at job submission, so after changing it jobs must be resubmitted. ResourceManager and NodeManager need not use ViewFs. For shared mount-table distribution without changing scheme, the page points to the ViewFsOverloadScheme guide.

## Checked

Method: 2026-11-08 compared against the ViewFs guide (apache/hadoop trunk markdown, read in full). Link types, nfly parameters, regex links, rename and reload behaviour match the page; the draft's inconsistent table-name casing was normalised and the invented "Verify" step removed.
