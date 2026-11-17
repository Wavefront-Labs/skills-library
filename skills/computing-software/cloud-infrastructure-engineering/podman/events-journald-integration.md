---
id: computing-software.cloud-infrastructure-engineering.podman.events-journald-integration
name: events-journald-integration
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [podman-events, journalctl, journald-identifiers, podman-event, inspect-data, events-container-create-inspect-data, containers-conf]
level: advanced
status: docs-checked
description: "Filter Podman events directly in journalctl using PODMAN_* identifiers, and enable verbose container-create events carrying inspect JSON."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-events.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query events with systemd tools instead of podman events.

With the journald backend Podman writes fields you can match with `journalctl`. `SYSLOG_IDENTIFIER` is always `podman`. Others: `PODMAN_EVENT` (event status), `PODMAN_TYPE` (event type), `PODMAN_TIME` (time written), `PODMAN_NAME` and `PODMAN_ID` (name and ID of the event object such as container, image or artifact), `PODMAN_EXIT_CODE`, `PODMAN_POD_ID`, `PODMAN_LABELS`, `PODMAN_HEALTH_STATUS`, `PODMAN_NETWORK_NAME`, and `PODMAN_CONTAINER_INSPECT_DATA`.

The last field appears only when `events_container_create_inspect_data=true` is set in containers.conf(5). That setting makes container-create events carry a JSON payload identical to `podman container inspect` output. The same payload is available to `podman events --format` as `.ContainerInspectData`.

Combine this with the `--filter` semantics of `podman events` where you can, but remember that with `events_logger` set to `file` or `none` these journald identifiers will not be present. Choose the backend first, then the query method.


The event types that appear with these fields mirror `podman events`: container, pod, image, artifact, system, volume, secret and network. Filtering by `PODMAN_TYPE` and `PODMAN_EVENT` in `journalctl` therefore corresponds to the `type=` and `event=` filters of the command. `PODMAN_CONTAINER_INSPECT_DATA` is the journald name of the inspect payload field.

## Checked

2026-11-09. Read against the official page text (podman-events.1); identifiers, event types, the verbose-create setting and the events_logger values were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
