---
id: computing-software.collaboration-platform-administration.matrix-synapse.purge-history-api
name: purge-history-api
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, purge-history, purge-up-to-ts, delete-local-events, vacuum-full, disk-space, database]
level: advanced
status: docs-checked
description: "Purge old room history with the purge_history admin API: choose the cut-off by event or timestamp, include local events deliberately, poll purge_history_status, then VACUUM FULL."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/purge_history_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The purge history API deletes historic events from the database to reclaim disk space. It needs an admin `access_token`. A call may take minutes or longer, and during that time users cannot paginate further back in the room from the point being purged. Synapse always keeps at least one message in each room, so the last message is never deleted.

```
POST /_synapse/admin/v1/purge_history/<room_id>[/<event_id>]
```

You must say where to purge up to, in one of three ways: an `event_id` in the URI, `purge_up_to_event_id` in the body, or `purge_up_to_ts` in the body (a timestamp in milliseconds since the Unix epoch). With an event ID, that event and others at the same graph depth are retained.

Defaults protect local content: events sent by local users are not deleted, because they may be the only copy, while events from remote users are. Room state such as joins, leaves and topic is always kept. To remove local message events too, send:

```json
{
   "delete_local_events": true
}
```

The call returns immediately with `{"purge_id": "<opaque id>"}` while the purge runs in the background. Poll it with:

```
GET /_synapse/admin/v1/purge_history_status/<purge_id>
```

The `status` is `active`, `complete` or `failed`; a failure also includes an `error` string.

Disk space is not returned to the operating system by the purge itself. On PostgreSQL run `VACUUM FULL;` against the database to do that.

When Synapse runs with workers, the docs warn that pagination requests for a room must be on one instance and that this API must not be used while pagination requests for the room are in flight.

## Checked

2026-11-04. Confirmed against the Synapse Purge History API page and the Workers page (pagination warning): endpoint, targets, delete_local_events, purge_id and status values, VACUUM FULL. Removed a lock-time remark and a closing pointer not on the page.
Method: documentation only; no commands were run.
