---
id: computing-software.collaboration-platform-administration.matrix-synapse.federation-destinations-admin-api
name: federation-destinations-admin-api
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, federation, destinations, retry-interval, reset-connection, backoff, remote-server]
level: advanced
status: docs-checked
description: "Inspect which remote servers Synapse cannot reach with the federation destinations admin API, sort and paginate, list shared rooms, and reset the retry backoff for a destination."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_api/federation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The federation API is described as new, experimental and subject to change. It exposes the retry state Synapse keeps for every remote server it federates with. It needs an admin `access_token`.

`GET /_synapse/admin/v1/federation/destinations` lists all destinations whether or not they have errored. After a failure it can take up to 20 minutes for the error to appear because a complete retry must have failed. Query parameters: `from` (offset, default 0), `limit` (default 100), `order_by` and `dir` (`f` forwards, `b` reverse). Valid `order_by` values are `destination` (default), `retry_last_ts`, `retry_interval`, `failure_ts` and `last_successful_stream_ordering`. The database only indexes `destination`, so other sort orders can put a large load on a big database. To paginate, repeat with `from` set to `next_token` until none is returned.

Each destination object holds:

- `retry_last_ts`: last failed attempt in ms, `0` if the last attempt succeeded.
- `retry_interval`: delay before the next try in ms, `0` if no retrying.
- `failure_ts`: first failure in ms, null if it never failed.
- `last_successful_stream_ordering`: most recent successfully sent PDU, or null if not yet tracked.

`GET /_synapse/admin/v1/federation/destinations/<destination>` returns one entry, and `.../<destination>/rooms` lists rooms shared with it (`room_id`, `stream_ordering`; `from`, `limit`, `dir` apply).

**Reset the backoff.** After a failed request Synapse marks the destination offline for a cooldown that grows by exponential backoff. To cancel it and retry immediately:

```
POST /_synapse/admin/v1/federation/destinations/<destination>/reset_connection
```

It only works if the destination previously failed, meaning `retry_last_ts` is not `0`. The connection attempt happens in the background and may take a while even though the call returns 200 straight away.

## Checked

2026-11-04. Confirmed against the Synapse Federation API page: endpoints, parameters and defaults, sort values, index caution, field meanings, reset_connection behaviour. Removed a closing usage tip.
Method: documentation only; no commands were run.
