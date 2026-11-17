---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tail-file-selection-and-refresh
name: tail-file-selection-and-refresh
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tail-input, exclude-path, ignore-older, refresh-interval, rotate-wait, path-key]
level: practitioner
status: docs-checked
description: "Select, exclude and age-limit files for tail, and tune how often the watched list refreshes after rotation."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/tail"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tail file selection

Keys on the `tail` input that decide what is read:

| Key | Default | Meaning |
| --- | --- | --- |
| `path` | none | file or wildcard pattern; several patterns separated by commas |
| `exclude_path` | none | shell patterns, comma separated, such as `*.gz,*.zip` |
| `ignore_older` | read all | skip files older than this; accepts `m`, `h`, `d` |
| `ignore_active_older_files` | `false` | ignore files older than `ignore_older` even if the file is being ingested |
| `refresh_interval` | `60` | seconds between refreshes of the watched file list |
| `rotate_wait` | `5` | extra seconds to monitor a file once it is rotated, in case pending data is flushed |
| `path_key` | none | append the monitored file name to each record under this key |
| `offset_key` | none | append the current offset to each record under this key |
| `skip_empty_lines` | `false` | skip empty lines from further processing |

```yaml
pipeline:
  inputs:
    - name: tail
      path: /var/log/containers/*.log
      exclude_path: '*.gz,*.zip'
      ignore_older: 2d
      path_key: filename
      refresh_interval: 10
```

Unstructured lines (no parser applied) are appended as a string under the key `log`; change that with `key`. Apply a parser with `parser` to produce a structured record.

File rotation is handled, including logrotate `copytruncate`, but that mode can lose a small amount of data in the window between copy and truncate. The `path` patterns must not match rotated files, or they would be read again and produce duplicates.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs tail input page (raw markdown, read in full).
