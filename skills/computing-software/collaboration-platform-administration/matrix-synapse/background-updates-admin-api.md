---
id: computing-software.collaboration-platform-administration.matrix-synapse.background-updates-admin-api
name: background-updates-admin-api
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, background-updates, event-resign, regenerate-directory, populate-stats, signing-key, pause]
level: advanced
status: docs-checked
description: "Check, pause and start Synapse database background updates via the admin API, including regenerate_directory, populate_stats_process_rooms and event_resign."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_api/background_updates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The background updates API manages the database updates Synapse runs after schema changes. It needs an admin `access_token`.

**Status.** `GET /_synapse/admin/v1/background_updates/status` returns `enabled` plus `current_updates`, keyed by database name (usually `master`). Each entry has the update `name`, `total_item_count` (what an "item" is depends on the update), `total_duration_ms` (running time excluding sleeps) and `average_items_per_ms` (an exponential average).

**Pause.** `POST /_synapse/admin/v1/background_updates/enabled` with `{"enabled": false}` pauses updates; `GET` on the same path reads the state. Do not leave them paused for long, because that harms Synapse performance. The setting does not survive a restart, and it does not cancel a query that is already running, which matters for `CREATE INDEX` updates since those cannot be interrupted once started.

**Run a job.** `POST /_synapse/admin/v1/background_updates/start_job` with a `job_name` starts it immediately. Valid names:

- `populate_stats_process_rooms`: recalculate the stats for all rooms.
- `regenerate_directory`: recalculate the user directory when it is stale or out of sync.
- `event_resign`: re-sign all locally-sent events with the current signing key, useful after rotating the server signing key so historical events carry the new signature.

```json
{
    "job_name": "populate_stats_process_rooms"
}
```

`event_resign` accepts optional narrowing parameters: `old_key`, to only re-sign events whose signature verifies against that key (format `"ed25519:key_id base64_public_key"`), and `before_ts`, to only re-sign events with a `received_ts` earlier than the value in milliseconds. Related: signing key backup and `old_signing_keys` are covered in the backup skill.

## Checked

2026-11-04. Confirmed against the Synapse Background Updates API page: status fields, pause behaviour and caveats, start_job names, event_resign parameters. Removed a closing usage tip.
Method: documentation only; no commands were run.
