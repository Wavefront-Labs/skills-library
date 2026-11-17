---
id: computing-software.systems-network-administration.immich.external-library-setup
name: external-library-setup
category: computing-software
field: systems-network-administration
product: immich
tags: [external-library, import-paths, read-only, docker-volumes, trash]
level: practitioner
status: docs-checked
description: "Add existing photo folders to Immich as an external library: read-only mounts, admin creation, import paths and access troubleshooting."
sources:
  - https://docs.immich.app/features/libraries
  - https://docs.immich.app/guides/external-library
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have Immich index photos that live outside its own storage.

Behaviour to know: an external library belongs to a single user, chosen at creation and not changeable. If an external file is deleted from disk, the asset goes to trash on rescan and is purged after 30 days. Metadata you add inside Immich (albums, descriptions) is stored only in Immich, not in the file. Moving a file within the library makes it a new asset, so metadata stored only in Immich is lost on rescan.

1. Mount the folder into `immich-server` (and any microservices worker) in `docker-compose.yml`:

```yaml
immich-server:
  volumes:
    - ${UPLOAD_LOCATION}:/data
    - /mnt/nas/christmas-trip:/mnt/media/christmas-trip:ro
```

The `:ro` flag blocks deleting from the web UI and writing XMP sidecars. Without it Immich can delete those files. Run `docker compose up -d`.

2. As admin: Administration, External Libraries, Create Library, pick the owner, then Add under Folders. Use the path the container sees (`/mnt/media/christmas-trip`), not the host path.

3. Optionally add exclusion patterns, then click Scan.

Import paths are scanned recursively. A file removed from all import paths is treated like a deleted file.

If a scan finds nothing, check: mounts in compose, mounts on worker containers, import paths matching the container path, no symlinks or links across mounts, permissions, and forward slashes. Test with `docker exec -it immich_server bash` then `ls /mnt/media/christmas-trip`.

Browser caching can delay refreshed assets showing correctly.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/libraries in full and guides/external-library in full.
Reworded: the file-move behaviour, to match the caution on the page.
Method: documentation only; no commands were run.
