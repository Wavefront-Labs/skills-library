---
id: computing-software.systems-network-administration.audiobookshelf.env-paths-and-binaries
name: env-paths-and-binaries
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [environment-variables, config-path, metadata-path, backup-path, ffmpeg, ffprobe]
level: practitioner
status: docs-checked
description: "Set Audiobookshelf CONFIG_PATH, METADATA_PATH, BACKUP_PATH, FFMPEG_PATH, FFPROBE_PATH and SKIP_BINARIES_CHECK, with defaults and caveats."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/backups.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/migration-os.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Audiobookshelf is configured by environment variables: pass them to Docker with `-e VARIABLE=VALUE`, or put them in `/etc/default/audiobookshelf` for package installs. Unset variables use their defaults.

Filesystem:

| Variable | Default | Meaning |
| --- | --- | --- |
| `CONFIG_PATH` | `./config` | Database (users, books, libraries, settings). Must not be on a network mount. |
| `METADATA_PATH` | `./metadata` | Cache, streams, covers, downloads, backups, logs. |
| `BACKUP_PATH` | `./metadata/backups` | Where backups (database plus images/metadata) are stored. |

External tools:

| Variable | Default | Meaning |
| --- | --- | --- |
| `FFMPEG_PATH` | `ffmpeg` | Binary path; if unset it must be on the system path. |
| `FFPROBE_PATH` | `ffprobe` | Same for ffprobe. |
| `SKIP_BINARIES_CHECK` | unset | Set to `1` to allow newer or custom ffmpeg builds; if set, also set `FFMPEG_PATH` and `FFPROBE_PATH`. |

Setting `BACKUP_PATH` as an environment variable makes the backup path read-only in the web interface. The metadata path in metadata files is absolute, so set `METADATA_PATH` at initial setup rather than changing it later.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Environment Configuration page (Filesystem and External Tools tables), backups page, migration page.

Method: documentation only; no commands were run.
