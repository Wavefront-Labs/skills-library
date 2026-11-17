---
id: computing-software.collaboration-platform-administration.matrix-synapse.media-repository-storage-layout
name: media-repository-storage-layout
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, media-repository, mxc, local-content, remote-content, thumbnails, url-cache, filesystem-id]
level: advanced
status: docs-checked
description: "Map MXC URIs to files on disk: local_content and remote_content layout, 24 character media IDs, thumbnail paths, the url_cache scheme and the tables recording each media kind."
sources:
  - https://element-hq.github.io/synapse/latest/media_repository.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The media repository stores avatars, attachments and thumbnails uploaded by local users, caches the same for remote users' media, and caches resources and thumbnails for URL previews. Everything is addressed by an MXC URI, `mxc://<server-name>/<media-id>`.

**Local media.** Synapse generates 24-character, case-sensitive media IDs made of upper and lowercase letters (other homeservers may differ). Metadata such as MIME type, upload time and size is in the `local_media_repository` table, which is shared with the URL cache. The ID is split into path segments of 2, 2 and 20 characters. For ID `aabbcccccccccccccccccccc`:

```
local_content/aa/bb/cccccccccccccccccccc
local_thumbnails/aa/bb/cccccccccccccccccccc/128-96-image-jpeg-scale
```

The thumbnail file name encodes width, height, MIME type and the thumbnailing method.

**Remote media.** When media from another server is requested, Synapse assigns a local `filesystem_id` in the same format. The `remote_media_cache` table maps remote server name and media ID to that `filesystem_id`. Files live under a per-server directory:

```
remote_content/matrix.org/aa/bb/cccccccccccccccccccc
remote_thumbnail/matrix.org/aa/bb/cccccccccccccccccccc/128-96-image-jpeg-scale
```

Older thumbnails may omit the method (`128-96-image-jpeg`). Note the directory is `remote_thumbnail`, without an `s`, unlike `local_thumbnails`.

**URL previews.** Downloaded preview resources get temporary IDs of the form `yyyy-mm-dd_aaaaaaaaaaaaaaaa` (the date plus 16 random case-sensitive letters), stored in `local_media_repository` and `local_media_repository_url_cache`, and deleted after a few days:

```
url_cache/yyyy-mm-dd/aaaaaaaaaaaaaaaa
url_cache_thumbnails/yyyy-mm-dd/aaaaaaaaaaaaaaaa/128-96-image-jpeg-scale
```

Admin APIs for deleting or quarantining media are covered separately.

## Checked

2026-11-04. Confirmed against the Synapse Media Repository page: MXC URI form, 24-character IDs, tables, local, remote and URL cache paths, thumbnail names. Removed a generic closing paragraph.
Method: documentation only; no commands were run.
