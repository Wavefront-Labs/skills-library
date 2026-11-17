---
id: computing-software.collaboration-platform-administration.vikunja.docker-quickstart
name: docker-quickstart
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, docker-run, sqlite-default, port-3456, cors-public-url]
level: intro
status: docs-checked
description: "Start Vikunja with a single docker run command using SQLite, the right volumes and ownership, and set the public URL so CORS does not block the UI."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quick start with SQLite:

```
mkdir $PWD/files $PWD/db
chown 1000 $PWD/files $PWD/db
docker run -p 3456:3456 -v $PWD/files:/app/vikunja/files -v $PWD/db:/db vikunja/vikunja
```

This exposes Vikunja on host port `3456`.

The default configuration has CORS enabled, which requires a public URL. Either set `VIKUNJA_SERVICE_PUBLICURL` to the URL where Vikunja is reachable, or set `VIKUNJA_CORS_ENABLE` to `false`.

The container runs as user `1000` with no group; use Docker's `--user` flag to change that, and make sure that user can write to the `db` and `files` folders.

The command mounts `files` at `/app/vikunja/files` and `db` at `/db` (SQLite).

To use a config file, mount it read-only (`-v /path/to/config/on/host.yml:/app/vikunja/config.yml:ro`). The docs recommend environment variables or `.env` files for Docker instead.

There is no default user or password: register a new account.

## Checked

2026-11-04: command, port, CORS warning, user 1000 note, config mount and registration note checked against the install page (Docker section). Removed the claim that uploads are lost if not mounted, which the page does not state.

Method: documentation only; no commands were run.
