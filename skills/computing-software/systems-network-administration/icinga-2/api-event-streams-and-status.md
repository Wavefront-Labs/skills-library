---
id: computing-software.systems-network-administration.icinga-2.api-event-streams-and-status
name: api-event-streams-and-status
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, rest-api, event-streams, v1-events, v1-status, long-polling, statechange]
level: practitioner
status: docs-checked
description: Subscribe to Icinga 2 live events with POST /v1/events using types and event. filters, and read daemon statistics from GET /v1/status.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API event streams and status
**Subscribe:** `POST /v1/events` with `types` (required array) and optional `filter`, as URL parameters or JSON body. Each type needs its own `events/<type>` permission.

**Types:** CheckResult, StateChange, Notification, AcknowledgementSet, AcknowledgementCleared, CommentAdded, CommentRemoved, DowntimeAdded, DowntimeRemoved, DowntimeStarted, DowntimeTriggered, ObjectCreated, ObjectDeleted, ObjectModified.

**Filter** event attributes with the `event.` prefix:
```
-d '{ "types": [ "CheckResult" ], "filter": "event.check_result.exit_status==2" }'
-d '{ "types": [ "CheckResult" ], "filter": "match(\"random*\", event.service)" }'
```

**Response:** newline-separated JSON objects, one per event, for example `{"check_result":{...},"host":"...","service":"ping4","timestamp":...,"type":"CheckResult"}`. The client must support long-polling and HTTP/1.1; HTTP/1.0 is not supported.

Use cases named in the docs: forward events to your own backend, correlate metrics with notifications and state changes (for example in Elasticsearch via Icingabeat), and open or resolve tickets automatically.

**Status:** `GET /v1/status` returns status information and statistics; limit by type in the path, for example `/v1/status/IcingaApplication`. Permission: `status/query`. Add `?pretty=1` for readable JSON.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/. No commands were run.
