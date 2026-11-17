---
id: computing-software.cloud-infrastructure-engineering.observability.filelog-receiver-operators-and-multiline
name: filelog-receiver-operators-and-multiline
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [filelog-receiver-config, filelog-operators, multiline-filelog, otel-logs, otel-collector]
level: advanced
status: docs-checked
description: "Configure the OTel Collector filelog receiver: include/exclude, checkpoints with file_storage, operator chains (json, regex, time, severity, move), multiline and rotation."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/README.md", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# filelog receiver: operators and multiline

## Base config
```yaml
extensions:
  file_storage:
    directory: /var/lib/otelcol/storage     # persist offsets across restarts
receivers:
  filelog:
    include: [/var/log/app/*.log]
    exclude: [/var/log/app/*.gz]
    start_at: end                            # beginning only for first-time backfill
    include_file_path: true
    poll_interval: 200ms                     # default
    max_log_size: 1MiB                       # default; max_log_size_behavior: split (default) or truncate
    storage: file_storage
    multiline:
      line_start_pattern: '^\d{4}-\d{2}-\d{2}T'
    operators:
      - type: regex_parser
        regex: '^(?P<ts>\S+) (?P<level>\w+) \[(?P<thread>[^\]]+)\] (?P<msg>.*)$'
        timestamp: {parse_from: attributes.ts, layout_type: gotime, layout: '2006-01-02T15:04:05.000Z07:00'}
        severity: {parse_from: attributes.level}
      - type: move
        from: attributes.msg
        to: body
      - type: remove
        field: attributes.ts
service:
  extensions: [file_storage]
```

## Useful operators
Parsers: `json_parser`, `regex_parser`, `key_value_parser`, `csv_parser`, `syslog_parser`, `time_parser`, `severity_parser`,
`trace_parser`, `uri_parser`, and `container` (docker, cri-o and containerd formats; `add_metadata_from_filepath` defaults to
true and adds k8s metadata from a `/var/log/pods/...` path, which needs `log.file.path`, so set `include_file_path: true`).
General purpose: `add`, `copy`, `move`, `remove`, `flatten`, `recombine`, `router`, `filter`, `retain`, `regex_replace`,
`noop`. The receiver README says to use only parsers and general purpose operators here. `on_error` takes `drop`,
`drop_quiet`, `send` (default for parsers) or `send_quiet`; `if` takes an expression that decides whether the operator runs.

## Router example (mixed formats)
```yaml
operators:
  - type: router
    routes:
      - {output: json, expr: 'body matches "^\\{"'}
    default: plain
  - {id: json, type: json_parser, output: plain}
  - {id: plain, type: noop}
```

## Rotation and checkpoints
The README says move/create and copy/truncate rotation are both handled: files are tracked by inode and content fingerprint
(first `fingerprint_size` bytes, default 1000, minimum 16; lowering it re-ingests larger files). `on_truncate` (default
`ignore`) controls a copytruncate rotation. Without a `storage` extension offsets are kept in memory only, so after a restart
`start_at: end` skips lines written while down and `start_at: beginning` re-reads files. `delete_after_read` deletes
files after reading, needs the `filelog.allowFileDeletion` feature gate and must be false when `start_at` is `end`.

## Gotchas
- `multiline` configures the `file_input` operator, so it splits raw lines before any operator runs; it takes exactly one of
  `line_start_pattern` or `line_end_pattern`, and `omit_pattern` drops the matched text. Use the `recombine` operator to join
  entries after parsing.
- `timestamp.layout_type` is `strptime` (default), `gotime` or `epoch`; the example uses `gotime`, so the layout is Go style.
- A router entry that matches no route is dropped unless `default` is set.
- `start_at` defaults to `end`, so a file that is not being written to is not read unless you set `beginning`.

## Verify
`debug` exporter with `verbosity: detailed` shows parsed attributes, severity and timestamp per record.

## Checked

2026-10-24. OpenTelemetry Collector contrib filelog receiver README, stanza operator docs (operators list, regex_parser, router, container, on_error, timestamp) and filestorage extension README (main branch). Confirmed: defaults for `start_at`, `poll_interval`, `fingerprint_size` (1000), `max_log_size`, `max_log_size_behavior`, `on_truncate`; multiline rules; `delete_after_read` feature gate; `on_error` values; router default and expression form; container operator metadata from file path; `storage` and `directory` settings.

Method: documentation only; no commands were run.
