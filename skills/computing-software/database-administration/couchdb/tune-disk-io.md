---
id: computing-software.database-administration.couchdb.tune-disk-io
name: tune-disk-io
category: computing-software
field: database-administration
product: couchdb
tags: [performance, disk-io, file-size, erl-flags, erlang-threads]
level: advanced
status: docs-checked
description: "Reduce CouchDB disk I/O pressure: keep files small, and use the Erlang +A async thread flag via ERL_FLAGS when disk is the bottleneck."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/performance.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tens of thousands of documents perform well however you write code; at millions you must be more careful.

**File size.** Smaller files mean fewer I/O operations, more of the file cached by CouchDB and the OS, and quicker replication and backup. Avoid keys hundreds of characters long, but do not use single-character keys either, since that hurts maintainability. Consider data that is duplicated by putting it in views.

**Faster storage.** Faster disks, striped RAID and modern file systems all help.

**Erlang async threads.** When disk is a bottleneck, the Erlang `+A` flag lets file operations run in their own threads so other Erlang processes keep executing. Set it through `ERL_FLAGS` in `(prefix)/etc/defaults/couchdb` (or equivalent):

```
export ERL_FLAGS="+A 4"
```

A value above zero keeps CouchDB responsive during heavy disk use; the page's example gives Erlang four I/O threads.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/performance page (Disk I/O): file size advice, faster disks, the Erlang +A flag via ERL_FLAGS and its four-thread example. Nothing removed.

Method: documentation only; no commands were run.
