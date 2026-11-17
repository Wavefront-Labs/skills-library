---
id: computing-software.systems-network-administration.immich.change-media-location
name: change-media-location
category: computing-software
field: systems-network-administration
product: immich
tags: [change-media-location, immich-media-location, schema-check, file-paths, database]
level: advanced
status: docs-checked
description: "Rewrite Immich database file paths after the media location moves, using immich-admin change-media-location, then confirm with schema-check."
sources:
  - https://docs.immich.app/administration/server-commands
  - https://docs.immich.app/install/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep the database in step when the media directory inside the container changes, for example from `/data` to `/my-data`.

Immich stores file paths in the database, so they must be rewritten to match a new media location. The `IMMICH_MEDIA_LOCATION` variable sets the media location inside the container; the docs warn that you probably should not set it, so treat this as a rare migration.

1. Back up the database first (see backup-and-restore).
2. Open a shell in the server container:

```bash
docker exec -it immich_server bash
```

3. Run the path rewrite:

```bash
immich-admin change-media-location
? Enter the previous value of IMMICH_MEDIA_LOCATION: /data
? Enter the new value of IMMICH_MEDIA_LOCATION: /my-data
```

The tool shows the previous and current values, states "Changing database paths from "/data/*" to "/my-data/*"" and asks "Do you want to proceed? [Y/n]". On success it prints "Database file paths updated successfully!".

4. The command changes database file paths only; the files and the container's `IMMICH_MEDIA_LOCATION` must agree with the new location.

5. Run a schema check:

```bash
immich-admin schema-check
```

Expect "Migrations are up to date" and "No schema drift detected".

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading administration/server-commands in full (command list, change-media-location and schema-check examples) and the `IMMICH_MEDIA_LOCATION` row and footnote in install/environment-variables.
Removed: the closing integrity-report step and the restart instruction, which these pages do not state.
Method: documentation only; no commands were run.
