---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-memory-and-file-single-plugins
name: buffer-memory-and-file-single-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buf-memory, buf-file-single, buffer, chunk-format, calc-num-records]
level: practitioner
status: docs-checked
description: "Compare Fluentd memory and file_single buffers: memory loses unflushed data on shutdown, file_single has no meta file and limited chunk keys."
sources:
  - https://docs.fluentd.org/buffer/memory
  - https://docs.fluentd.org/buffer/file_single
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd buf_memory and buf_file_single
**memory**: fast; chunks live in RAM. When Fluentd shuts down, buffered logs that cannot be written quickly are deleted. It has no plugin-specific parameters.

**file_single**: persistent, like `file` but without the metadata file.
- `path` (required, since 1.7.0): must be unique across output plugins and Fluentd instances. Name format: `path/fsb.<tag or field value>.b<chunk_id>.buf`; with multiple workers `worker<N>/<plugin id>/` is added.
- `calc_num_records` (default true): recomputes chunk size by reading files at startup, because there is no meta file. Set false to speed startup if the output does not need chunk size (mainly `out_forward`).
- `chunk_format`: `msgpack`, `text` or `auto` (default; decided by `formatted_to_msgpack_binary?`).
- `file_permission` (falls back to the system `file_permission`, else `0644`) and `dir_permission` (system `dir_permission`, else `0755`).

Limitation: chunk keys can only be tag or one field key.
```
<buffer>           # ok, same as <buffer tag>
<buffer tag>       # ok
<buffer key>       # ok
<buffer time>      # not supported
<buffer key1,key2> # not supported
```
Like `file`, do not place it on NFS, GlusterFS or HDFS; major data loss was observed.

```
<buffer>
  @type file_single
  path /var/log/fluent/out_fwd
</buffer>
```

## Checked

2026-11-04. Confirmed against the Fluentd memory and file_single buffer pages (docs.fluentd.org/buffer/memory, docs.fluentd.org/buffer/file_single): shutdown behaviour, path rules and file name format, calc_num_records, chunk_format, permissions, chunk key limitation, remote file system caution. Removed: the claim that memory cannot evacuate chunks (not on those pages).

Method: documentation only; no commands were run.
