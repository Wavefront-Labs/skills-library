---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-tail-position-file-and-read-tuning
name: in-tail-position-file-and-read-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-tail, pos-file, read-from-head, read-lines-limit, encoding, num-threads, max-line-size]
level: practitioner
status: docs-checked
description: "Control where in_tail reads from and how fast: pos_file and compaction, read_from_head, line and byte limits, encoding pitfalls, num_threads and max_line_size."
sources:
  - https://docs.fluentd.org/input/tail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_tail position and read tuning
- `pos_file` (highly recommended): records last-read positions across restarts; one file can hold many positions. Never share it between `in_tail` sources (corrupts content). It grows with dynamic paths until restart; `pos_file_compaction_interval` (1.9.2), e.g. `72h`, compacts it.
- `read_from_head` (default false): start from the head or the recorded position. With a huge file it blocks other plugins from starting; `skip_refresh_on_startup` helps. From v1.14.3 newly added files are read from the head automatically.
- `read_lines_limit` (default 1000): lines per I/O; lower it on `chunk bytes limit exceeds for an emitted event stream`.
- `read_bytes_limit_per_second` (1.13.0, default -1): throttle; must be at least 8192.
- `max_line_size` (1.14.4): longer lines are skipped; set below `chunk_limit_size` to avoid frequent `BufferChunkOverflowError`.
- `multiline_flush_interval`: flush a multiline buffer after e.g. `5s`.
- `encoding` / `from_encoding`: strings are ASCII-8BIT by default. Give both together; from v0.14.12 to v1.18.x specifying only `encoding` ran `String#encode` and could break data. Same value for both only relabels the encoding.
- `num_threads` (1.20.0, default 1): 2 or more parses on worker threads for supported parsers (`none`, `regexp`, `json`, `csv`, `tsv`, `ltsv`, `msgpack`, `apache`, `apache2`, `apache_error`, `nginx`, `syslog`; not multiline; `open_on_every_update` false). Otherwise it logs `in_tail worker parsing is unavailable` and falls back. Up to `num_threads * 2` batches are in flight.
- `open_on_every_update`, `ignore_repeated_permission_error`.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/input/tail and confirmed: pos_file, compaction, read limits, encoding bug note, num_threads conditions. Removed or reworded: nothing.

Method: documentation only; no commands were run.
