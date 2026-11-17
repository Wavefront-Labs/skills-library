---
id: computing-software.systems-network-administration.immich.custom-storage-locations
name: custom-storage-locations
category: computing-software
field: systems-network-administration
product: immich
tags: [thumb-location, profile-location, encoded-video-location, backup-location, bind-mounts]
level: practitioner
status: docs-checked
description: "Store Immich thumbnails, encoded video, profiles and backups on separate disks using .env variables and extra volume mounts under /data."
sources:
  - https://docs.immich.app/guides/custom-locations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: place generated files on different storage from the originals, for example thumbnails on SSD and originals on a NAS.

In `.env`, `UPLOAD_LOCATION` is the base folder; define only the overrides you need:

```
UPLOAD_LOCATION=/custom/path/immich/immich_files
THUMB_LOCATION=/custom/path/immich/thumbs
ENCODED_VIDEO_LOCATION=/custom/path/immich/encoded-video
PROFILE_LOCATION=/custom/path/immich/profile
BACKUP_LOCATION=/custom/path/immich/backups
```

In `docker-compose.yml`, under `immich-server`, add mounts beneath `/data`:

```yaml
volumes:
  - ${UPLOAD_LOCATION}:/data
  - ${THUMB_LOCATION}:/data/thumbs
  - ${ENCODED_VIDEO_LOCATION}:/data/encoded-video
  - ${PROFILE_LOCATION}:/data/profile
  - ${BACKUP_LOCATION}:/data/backups
  - /etc/localtime:/etc/localtime:ro
```

Move the existing files into the new folders so Immich can find everything, or reset Immich if nothing important is uploaded yet. Then run `docker compose up -d`.

Notes:

- Do not mount `upload/` and `library/` as separate bind mounts when they are on the same device, because of how Docker bind mounts work. Mount the HDD or NAS at `/data` and put other folders under it.
- `thumbs/` holds both small timeline thumbnails and larger previews; they cannot be separated.
- Update backup settings for the new paths, especially `profile/`.
- The server tracks free space only at `UPLOAD_LOCATION`, so monitor the other disks yourself.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading guides/custom-locations in full: .env variables, compose mounts, move-or-reset advice, bind-mount note, thumbs note, storage metrics note.
Removed: nothing.
Method: documentation only; no commands were run.
