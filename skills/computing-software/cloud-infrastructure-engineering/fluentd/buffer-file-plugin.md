---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-file-plugin
name: buffer-file-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buf-file, buffer, persistent-buffer, path, file-permission, nfs]
level: practitioner
status: docs-checked
description: "Configure the Fluentd file buffer: path and chunk file naming, per-worker directories, root_dir with @id, path_suffix, permissions, NFS limitation."
sources:
  - https://docs.fluentd.org/buffer/file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd buf_file
Persistent buffer on local disk. Chunks are `buffer.b{chunk_id}.log` plus a `.meta` file.

- `path`: directory for chunks; must be unique per buffer. With multiple workers, `worker{worker_id}` subdirectories are created automatically.
- With `root_dir` in `<system>` and an `@id` on the plugin, `path` may be omitted; files go to `{root_dir}/worker{worker_id}/{@id}/buffer`, and the worker directory exists even with one worker.
- `path_suffix` (default `.log`, since 1.6.3), e.g. `.buf`.
- `file_permission` (default from system `file_permission`, else `0644`) and `dir_permission` (else `0755`); the same file permission applies to `.meta`.
- Rename the prefix by ending `path` in `.*` (`/var/log/fluent/buf/custom.*` gives `custom.b<id>.log`) or the whole name with `.*.` (`custom_prefix.*.custom_suffix`, where `path_suffix` is ignored).

Cautions from the page:
- Ensure enough disk space; running out is frequently reported.
- Never use it on remote file systems (NFS, GlusterFS, HDFS); major data loss was observed.
- If `path` is implicitly taken from the output's `path`, the evaluated value must not contain `[` or `]`, or resuming after restart may ignore it; override `path` inside `<buffer>`.

```
<buffer>
  @type file
  path /var/log/fluent/buf
</buffer>
```

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/buffer/file and confirmed: path and file naming, worker directories, root_dir with @id, path_suffix, permissions, caution notes. Removed or reworded: nothing.

Method: documentation only; no commands were run.
