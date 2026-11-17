---
id: computing-software.collaboration-platform-administration.matrix-synapse.rooms-admin-api-delete-and-block
name: rooms-admin-api-delete-and-block
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, delete-room, block-room, purge, new-room-user-id, delete-status, shutdown]
level: advanced
status: docs-checked
description: "Shut down, block and purge a room with the Synapse delete room API v2: new_room_user_id, block, purge, force_purge, polling delete_status, and how v1 differs."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/rooms.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The delete room API removes a room from your server and can block it. It shuts the room down, and either moves local users and aliases to a new room (when `new_room_user_id` is set) or simply makes local users leave. Users on other servers are unaffected. Admin `access_token` required.

**Version 2 (asynchronous, marked experimental and subject to change)**

```
DELETE /_synapse/admin/v2/rooms/<room_id>
```

The body must not be empty; send at least `{}`. Parameters, all optional:
- `new_room_user_id`: local user ID (need not be registered) who creates and administers a new room into which everyone is moved. Invited users get power level -10, so they cannot speak.
- `room_name`: defaults to "Content Violation Notification".
- `message`: first message in the new room; the default text talks about illegal content, so set your own.
- `block`: defaults to false; true prevents future joins to the old room.
- `purge`: defaults to true; removes all traces of the room from the database after local users are removed.
- `force_purge`: only with `purge`; purges even if local users remain. Use only when a regular purge fails, because it can leave clients confused.

The call returns at once with `{"delete_id": "<opaque id>"}`.

**Status.** `GET /_synapse/admin/v2/rooms/<room_id>/delete_status` lists active tasks and those finished in the last 24 hours; each result has a `status` (such as active or failed), an `error` on failure, and a `shutdown_room` object with `kicked_users`, `failed_to_kick_users`, `local_aliases` and `new_room_id`. Status is kept for up to 24 hours or until Synapse restarts, whichever comes first. You can also query by `delete_id`.

**Version 1** is `DELETE /_synapse/admin/v1/rooms/<room_id>` with the same body. It is synchronous, so the response only arrives when the work ends (minutes or longer), a second identical request blocks, and it will be deprecated. Only v1 can pre-emptively block a room unknown to the server, using `block: true`.

Depending on the amount of history purged, a call may take several minutes or longer.

## Checked

Method: docs-checked 2026-11-09 against docs/admin_api/rooms.md (Synapse develop branch, raw markdown; Delete Room API and delete status sections read in full).
