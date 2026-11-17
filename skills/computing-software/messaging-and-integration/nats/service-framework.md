---
id: computing-software.messaging-and-integration.nats.service-framework
name: service-framework
category: computing-software
field: messaging-and-integration
product: nats
tags: [services, micro, service-discovery, endpoints, srv-ping, srv-stats, srv-info]
level: practitioner
status: docs-checked
description: "Build discoverable NATS services: semver-named services, endpoints, groups, and the $SRV.PING, STATS and INFO discovery subjects."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/developing-with-nats/services/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: structure request-reply handlers as a service that tooling can discover and monitor.

Concepts (per the ADR-32 services protocol; check that your client library supports it):
- Service: the top-level group of related functionality. It must have a name and a version that follows semver. Services are discoverable in a NATS system.
- Endpoint: one operation clients call; a service needs at least one.
- Group: optional collection of endpoints that gives a logical grouping and an optional common subject prefix.

Built-in operations answered by the client library (not by your code):
- `PING` on `$SRV.PING.>` gathers replies from running services so tooling can list them.
- `STATS` on `$SRV.STATS.>` returns statistics: total requests, errors and processing time.
- `INFO` on `$SRV.INFO.>` returns the service definition and metadata including groups and endpoints.

Your responsibility: responding to requests on the real endpoints. Multiple instances of one service load balance naturally when they share a queue group, a core feature of request-reply.

Gotcha: the services API is relatively new and not every client implements it; see NATS By Example for per-language samples.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
