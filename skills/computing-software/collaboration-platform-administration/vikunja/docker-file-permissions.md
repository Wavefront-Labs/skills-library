---
id: computing-software.collaboration-platform-administration.vikunja.docker-file-permissions
name: docker-file-permissions
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, uid-1000, permission-denied, files-volume, rootless-docker]
level: practitioner
status: docs-checked
description: "Fix Vikunja container permission-denied errors on the files volume, data export and uploads, including rootless Docker and macOS notes."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/docker-start-to-finish.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vikunja runs as user `1000` with no group and will not take ownership of the files folder (that would need root). Before starting:

```
mkdir $PWD/files
chown 1000 $PWD/files
```

Use `chown -R 1000` when the directory already holds files.

Typical errors: `open /app/vikunja/files/1: permission denied` (uploads, project backgrounds) and `mkdir /app/vikunja/files/user-export-tmp/: permission denied` (data export). Export also needs a writable `/tmp`; if you see `open /tmp/vikunja-export-*.zip: no such file or directory`, mount `/tmp:/tmp`.

`PUID` and `PGID` have no effect. Change the user with Docker's `user:` directive.

Rootless Docker remaps UIDs, so ownership can look right yet fail. Set `user: "0:0"`; container root maps to your unprivileged host user. `vikunja doctor` detects user-namespace problems and suggests this.

On macOS, Docker Desktop handles bind-mount permissions, so skip the `chown` (default UID is 501).

## Checked

2026-11-04. Confirmed against the Vikunja Docker Walkthrough (setup/docker-start-to-finish) and Full docker example (setup/full-docker-example): UID 1000 and no group, no ownership takeover, mkdir and chown commands, -R advice, the permission-denied messages, writable /tmp, PUID and PGID having no effect, rootless Docker user 0:0, vikunja doctor, and the macOS note. Nothing removed.

Method: documentation only; no commands were run.
