---
id: computing-software.web-development.directus.docker-compose-sqlite
name: docker-compose-sqlite
category: computing-software
field: web-development
product: directus
tags: [docker-compose, sqlite-setup, secret, public-url]
level: intro
status: docs-checked
description: "Create a persistent local Directus project with docker compose, SQLite, mounted volumes, SECRET, PUBLIC_URL and optional websockets."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/2.create-a-project.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Make a `directus` directory with empty `database`, `uploads` and `extensions` subdirectories, then add `docker-compose.yml`:

```yaml
services:
  directus:
    image: directus/directus:12.0.2
    ports:
      - 8055:8055
    volumes:
      - ./database:/directus/database
      - ./uploads:/directus/uploads
      - ./extensions:/directus/extensions
    environment:
      SECRET: "replace-with-random-value"
      DB_CLIENT: "sqlite3"
      DB_FILENAME: "/directus/database/data.db"
      WEBSOCKETS_ENABLED: "true"
      PUBLIC_URL: "http://localhost:8055/"
      LICENSE_KEY: ""
```

Run `docker compose up`, then open `http://localhost:8055` and create the Admin account.

Notes:
- `SECRET` is required, must be a long random value, and signs access tokens.
- `PUBLIC_URL` builds links, asset URLs and redirects; a license binds to it on first use, so set it accurately.
- `WEBSOCKETS_ENABLED` is optional and turns on Realtime. Empty `LICENSE_KEY` means core tier.
- The docs say this setup is not production-ready but enough to use many features. The image tag shown is the one in the docs page at the time of checking; releases are published on Docker Hub.

## Checked

2026-11-04: directory layout, compose file, volumes, SECRET, SQLite variables, WEBSOCKETS_ENABLED, PUBLIC_URL, LICENSE_KEY and the not-production-ready remark confirmed against the Directus Create a Project page. Reworded the production note and removed nothing else.

Method: documentation only; no commands were run.
