---
id: computing-software.cloud-infrastructure-engineering.docker.otel-collector-filelog-receiver-for-docker-logs
name: otel-collector-filelog-receiver-for-docker-logs
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, filelog-receiver, opentelemetry-collector, json-file-logs, docker-logs, otel-logs, log-parsing]
level: practitioner
status: docs-checked
description: "Collect Docker json-file container logs with the OpenTelemetry Collector filelog receiver: paths, json parsing operators, container metadata, multiline, checkpoints and exporters."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/container.md
  - https://docs.docker.com/engine/logging/drivers/json-file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenTelemetry Collector filelog receiver for json-file logs

With Docker's default `json-file` driver, each container's stdout and stderr are written as JSON
lines, one container per file, shaped like
`{"log":"Log line is here\n","stream":"stdout","time":"2019-01-01T11:11:11.111111111Z"}`.

**Caveat from the Docker docs:** these files are designed to be accessed exclusively by the Docker
daemon, and reading them with external tools may interfere with Docker's logging and cause
unexpected behaviour. Weigh this against shipping logs with a Docker logging driver instead.

## Collector config (contrib distribution)
```yaml
receivers:
  filelog:
    include: [<path to the json-file logs on the host>]
    start_at: end                    # default; 'beginning' only for a first backfill
    include_file_path: true          # adds attribute log.file.path
    storage: file_storage            # ID of a storage extension; keeps offsets across restarts
    operators:
      - type: container
        format: docker
        add_metadata_from_filepath: false   # the k8s metadata parser expects Kubernetes paths
extensions:
  file_storage: { directory: <writable directory> }
service:
  extensions: [file_storage]
  pipelines:
    logs: { receivers: [filelog], exporters: [<your exporter>] }
```
- `container` parses docker, crio and containerd formats; `format` is optional because it is
  auto-detected. For Docker input it sets the body to the `log` text, the timestamp from `time`,
  and the stream in attribute `log.iostream`.
- `start_at` defaults to `end`, so a file not actively being written is not read.
- Without a `storage` extension, offsets are kept in memory only, so a collector restart loses
  its position.
- `fingerprint_size` (default 1000 bytes) identifies files; the receiver tracks files by inode and
  content fingerprint, so move/create and copy/truncate rotation are both handled.

## Container names and labels
The log file path carries only the container ID. For names or labels, use the json-file driver
options `labels`, `labels-regex`, `env` and `env-regex` (comma-separated labels or environment
variables the daemon accepts; for advanced log tag options), then map those attributes.

## Multiline
For the Docker format, add a `recombine` operator after the container operator (the operator docs
example):
```yaml
- id: recombine
  type: recombine
  combine_field: body
  is_first_entry: body matches "^\\d{4}-\\d{2}-\\d{2}T\\d{2}"
```
CRI formats recombine partial lines using their `P`/`F` tag. The container operator's
`max_log_size` (default 1MiB) limits the recombined size of partial logs.

## Log rotation (Docker side)
`max-size` (default unlimited) and `max-file` (default 1; only effective with `max-size`) are
json-file options, settable in `daemon.json` as strings or per container with `--log-opt`.

## Verify
- [ ] Records arrive with the expected body, stream and timestamps.
- [ ] Restarting the collector neither duplicates nor drops lines (compare counts).

## Checked
Checked 2026-10-28 against the filelog receiver README, the stanza `container` operator doc and
Docker's json-file driver page: config fields and defaults, container operator behaviour and
fields, recombine example, rotation support, json-file options and the exclusive-access warning.
Removed as unconfirmed: the `regex_parser`, `move` and `json_parser` steps, `resourcedetection`
and `otlphttp` settings, the `docker_observer` suggestion, the "16 KB partial-message limit", the
collector container run command and its mount paths, and the claim that the container operator
alone recombines Docker-format partial lines.
Method: documentation only; no commands were run.
