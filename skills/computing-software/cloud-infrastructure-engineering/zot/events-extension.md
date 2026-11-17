---
id: computing-software.cloud-infrastructure-engineering.zot.events-extension
name: events-extension
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, events, cloudevents, http-sink, nats-sink, image-scanned]
level: advanced
status: docs-checked
description: "Send Zot registry events to HTTP or NATS sinks as CloudEvents: sink settings, source and typePrefix, hot reload, payload metadata and image-scanned events."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configure `extensions.events` with `enable`, `source`, `typePrefix` and `sinks`.

Sink attributes:
- `type`: `http` or `nats`.
- `address`: endpoint.
- `timeout`: HTTP sinks default to 30 seconds if omitted or not positive.
- `credentials`: optional auth block for HTTP sinks (`username`/`password`, optional bearer `token`).
- `headers`: optional custom HTTP headers.
- `channel`: NATS subject to publish to.

CloudEvents identity: `source` defaults to `zotregistry.dev`; `typePrefix` defaults to `zotregistry` and cannot start or end with a dot or contain two consecutive dots.

Hot reload: enable/disable, identity and sink settings change without restarting Zot.

Payloads include `actor` (such as `actor.name`) and `request` (`request.addr`, `request.method`, `request.useragent`) when request context exists; internally triggered operations omit them.

Image scanned event: with CVE scanning and events both enabled, each successful non-cached scan (scheduled or on-demand) emits `zotregistry.image.scanned` (or `<typePrefix>.image.scanned`). Data has repo, reference, resolved digest, media type and a `summary` with `count`, `fixableCount`, `unknownCount`, `lowCount`, `mediumCount`, `highCount`, `criticalCount`, `maxSeverity`. HTTP sinks also get the type in the `ce-type` header. The page documents only this event type.

## Checked

2026-11-04. Read against the zot events article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
