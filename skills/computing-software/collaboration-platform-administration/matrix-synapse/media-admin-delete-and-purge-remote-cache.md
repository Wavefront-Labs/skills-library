---
id: computing-software.collaboration-platform-administration.matrix-synapse.media-admin-delete-and-purge-remote-cache
name: media-admin-delete-and-purge-remote-cache
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, media, delete-media, purge-media-cache, before-ts, size-gt, keep-profiles, disk-space]
level: advanced
status: docs-checked
description: "Reclaim Synapse media disk space: delete one local media item, delete by last-access date or size with keep_profiles, and purge cached remote media with purge_media_cache."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/media_admin_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
These calls need an admin `access_token`.

**Delete one local item.** `DELETE /_synapse/admin/v1/media/<server_name>/<media_id>` with a `{}` body, where `server_name` is your own server. It removes the local file, its thumbnails and copies downloaded from remote homeservers. The response lists `deleted_media` and `total`. It does not touch media in external repositories such as matrix-media-repo.

**Delete by age or size.**

```
POST /_synapse/admin/v1/media/delete?before_ts=<before_ts>
{}
```

- `before_ts` (required): Unix timestamp in milliseconds. It is compared with the time of last access, not creation, so files used recently survive.
- `size_gt` (optional): only files larger than this many bytes; default `0`.
- `keep_profiles` (optional): default `true`, which keeps files still used as a profile or room avatar. Set `false` to delete those too.

The older `POST /_synapse/admin/v1/media/<server_name>/delete` form has been deprecated since Synapse v1.78.0. The response again returns `deleted_media` and `total`.

**Purge cached remote media.**

```
POST /_synapse/admin/v1/purge_media_cache?before_ts=<unix_timestamp_in_ms>
{}
```

All cached remote media last accessed before the timestamp is removed, and the response is `{"deleted": 10}`. If a user requests purged remote media again, Synapse fetches it from the originating server. Deleting media uploaded by one user is in the user admin API.

## Checked

2026-11-04. Confirmed against the Synapse Media Admin API page: delete one item, delete by date or size and parameters, deprecated endpoint, purge_media_cache, response fields. Removed a closing paragraph with unsourced advice.
Method: documentation only; no commands were run.
