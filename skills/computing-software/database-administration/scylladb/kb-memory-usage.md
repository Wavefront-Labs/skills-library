---
id: computing-software.database-administration.scylladb.kb-memory-usage
name: kb-memory-usage
category: computing-software
field: database-administration
product: scylladb
tags: [memory, seastar, reserve-memory, scylla-args, cache]
level: practitioner
status: docs-checked
description: "Why ScyllaDB uses most available RAM (cache) and how to limit it with --memory and --reserve-memory in /etc/default/scylla-server or /etc/sysconfig/scylla-server."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/memory-usage.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ScyllaDB memory usage

ScyllaDB can use far more memory than the data set. For example 19 GB of data and 220 GB of memory used is normal: free memory is used as cache and managed dynamically. If many clients connect, ScyllaDB evicts cached data to make room for connection buffers, so a large resident size is not a leak.

To limit it, pass one of these to the scylla process:
- `--memory <size>`: total memory for ScyllaDB.
- `--reserve-memory <size>`: memory left for the operating system and external scylla modules (it must be enough for those).

Where to set:
- Ubuntu/Debian: `/etc/default/scylla-server`
- Red Hat / CentOS: `/etc/sysconfig/scylla-server`

Example:

```
SCYLLA_ARGS="--log-to-syslog 1 --log-to-stdout 0 --default-log-level info --network-stack posix --memory 2G --reserve-memory 2G"
```

## Checked

2026-11-04: memory behaviour, the --memory and --reserve-memory options, the file locations and the example confirmed against the ScyllaDB memory usage knowledge-base page. Removed the unsupported restart, co-location and container advice.

Method: documentation only; no commands were run.
