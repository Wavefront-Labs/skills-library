---
id: computing-software.collaboration-platform-administration.matrix-synapse.media-admin-quarantine-and-query
name: media-admin-quarantine-and-query
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, media, quarantine, protect-media, room-media, quarantine-changes, sha256]
level: advanced
status: docs-checked
description: "Query media in a room or by ID and quarantine, unquarantine or protect media through the Synapse admin API, including hash-based quarantine and the admin bypass parameter."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/media_admin_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All media admin APIs need an admin `access_token`.

**Query.** `GET /_synapse/admin/v1/room/<room_id>/media` returns `local` and `remote` lists of MXC URIs, but only for unencrypted events or rooms. For a user's uploads use the user admin API's media listing. `GET /_synapse/admin/v1/media/<origin>/<media_id>` returns a `media_info` object (`media_type`, `media_length`, `upload_name`, `created_ts`, `filesystem_id`, `last_access_ts`, `quarantined_by`, `safe_from_quarantine`, `sha256` and more); uncached remote media returns 404.

**What quarantine does.** It marks local media, and locally cached copies of remote media, inaccessible; downloads return 404. Files and thumbnails are not deleted. Since Synapse 1.128.0 upload hashes are tracked, so quarantining one item also quarantines already-uploaded media with the same hash, any future uploads, and existing and future cached remote copies. Admins can fetch quarantined content only by adding `?admin_unsafely_bypass_quarantine=true` to the normal download URL, which the docs advise against because it can serve harmful content; non-admins cannot bypass it.

**Endpoints (all `POST` with an empty `{}` body):**

- `/_synapse/admin/v1/media/quarantine/<server_name>/<media_id>` and `/media/unquarantine/<server_name>/<media_id>` for one item.
- `/_synapse/admin/v1/room/<room_id>/media/quarantine` for everything in a room, returning `num_quarantined`. The legacy `quarantine_media/<room_id>` form is deprecated.
- `/_synapse/admin/v1/user/<user_id>/media/quarantine` for all local media uploaded by a local user (not remote users).
- `/_synapse/admin/v1/media/protect/<media_id>` and `/media/unprotect/<media_id>` to exempt local media such as sticker packs from the bulk quarantine calls.

`GET /_synapse/admin/v1/media/quarantine_changes?from=<next_batch>` lists change records, 100 per page oldest first. It is best-effort and may have missing or duplicate records, and only captures explicit quarantine API use.

Deleting and purging media is a separate skill.

## Checked

2026-11-04. Confirmed against the Synapse Media Admin API page: room media listing, media info fields, quarantine behaviour and hash tracking, bypass parameter, all quarantine, protect and changes endpoints. Nothing removed.
Method: documentation only; no commands were run.
