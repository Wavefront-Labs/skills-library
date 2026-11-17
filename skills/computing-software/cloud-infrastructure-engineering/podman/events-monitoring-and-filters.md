---
id: computing-software.cloud-infrastructure-engineering.podman.events-monitoring-and-filters
name: events-monitoring-and-filters
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [podman-events, events-logger, journald, filter, since-until, format, monitoring]
level: practitioner
status: docs-checked
description: "Monitor Podman with podman events: event backends (journald, file, none), streaming versus since/until, supported filters, event types and Go template placeholders."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-events.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: watch or query what Podman did and when.

`podman events` (also `podman system events`) prints a timestamp, type, status, name and image for each event. The default logger is journald; set `events_logger` in containers.conf to `file` (only `file` and `journald` are accepted). The value `none` completely disables events, so nothing is reported.

By default it streams new events; `--since` and `--until` accept RFC3339Nano timestamps or Go durations such as `10m` or `5h` to list past events. With neither, only new events are shown. `--stream` (default true) keeps the command running after the last known event; `--no-trunc` defaults to true.

Event types: container, pod, image, artifact, system, volume, secret and network, each with its own statuses (container statuses include create, init, start, stop, died, exited, exec, remove and checkpoint/restore; pods have create, kill, pause, remove, start, stop, unpause).

Filters use `filter=value`: `artifact`, `container`, `event`, `image`, `label`, `network`, `pod`, `volume`, `type`. IDs may be short or full. The `die` status maps to `died` for Docker compatibility. Examples: `podman events -f event=create` and `podman events --filter event=create --filter type=pod`.

`--format` outputs JSON Lines or a Go template using placeholders such as `.Status`, `.Type`, `.Name`, `.ID`, `.Image`, `.ContainerExitCode`, `.HealthStatus`, `.OOMKilled`, `.PodID`, `.Time`, `.TimeNano`, `.Error`, `.Attributes`.

## Checked
2026-11-09: read the podman-events man page in full and confirmed the logger values, streaming, --since and --until formats, --stream and --no-trunc defaults, event types and statuses, the filter list, the die to died mapping and the format placeholders. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

