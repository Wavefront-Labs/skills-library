---
id: computing-software.collaboration-platform-administration.matrix-synapse.rooms-admin-api-list-and-search
name: rooms-admin-api-list-and-search
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, rooms, list-rooms, search-term, order-by, pagination, state-events, empty-rooms]
level: practitioner
status: docs-checked
description: "Find rooms on a Synapse server with GET /_synapse/admin/v1/rooms: order_by, search_term, public and empty filters, next_batch pagination, room size fields."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/rooms.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The List Room API returns the rooms on your server with filtering, sorting and pagination. Authenticate with an admin `access_token`.

```
GET /_synapse/admin/v1/rooms
```

**Query parameters**
- `from` (offset, default 0) and `limit` (default 100).
- `order_by`: `name` (default), `canonical_alias`, `joined_members` (largest first), `joined_local_members`, `version`, `creator`, `encryption`, `federatable`, `public`, `join_rules`, `guest_access`, `history_visibility`, `state_events` (largest first). `alphabetical` and `size` are deprecated aliases of `name` and `joined_members`.
- `dir`: `f` or `b`; `b` reverses the sort.
- `search_term`: matches if contained in the room name, the local part of the canonical alias, or the complete room ID (case sensitive).
- `public_rooms` and `empty_rooms`: booleans; when absent both kinds are returned. A room is empty when `joined_members` is zero.

**Response.** `rooms` holds objects with `room_id`, `name`, `canonical_alias`, `joined_members`, `joined_local_members`, `version`, `creator`, `encryption` (null when not encrypted), `federatable`, `public`, `join_rules`, `guest_access`, `history_visibility`, `state_events` (the room's "complexity") and `room_type` (such as `m.space`). Also `offset`, `total_rooms`, and `next_batch` / `prev_batch` when more pages exist; repeat the request with `from` set to `next_batch`. Prefer `offset` over `next_token`, which is not meant to be parsed.

**Examples.** Find a room by name: `GET /_synapse/admin/v1/rooms?search_term=TWIM`. Order by number of state events, largest first: `?order_by=state_events` (the docs' own example uses the deprecated `order_by=size`, plus `from` for the next page). List only empty rooms: `?empty_rooms=true`.

The same page also documents room details, members, state, messages, block status, forward extremities and make-room-admin endpoints.

## Checked

Method: docs-checked 2026-11-09 against docs/admin_api/rooms.md (Synapse develop branch, raw markdown; List Room API section read in full, other sections skimmed by heading).
