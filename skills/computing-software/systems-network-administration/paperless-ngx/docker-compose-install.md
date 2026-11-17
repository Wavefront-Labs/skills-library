---
id: computing-software.systems-network-administration.paperless-ngx.docker-compose-install
name: docker-compose-install
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, docker-compose, compose-file, bind-mount, docker-secrets]
level: practitioner
status: docs-checked
description: "Install Paperless-ngx by hand from the compose templates: pick a database variant, bind-mount folders, set env values and start it."
sources:
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual Docker Compose installation

1. From the project's `docker/compose` directory download one `docker-compose.*.yml` for your database and save it as `docker-compose.yml`. Download `docker-compose.env` and `.env` into the same folder. A file with `-tika` in its name adds Office document support. PostgreSQL is recommended for new installs.
2. Edit `docker-compose.yml`. Point the consume, media and other volumes at host folders by replacing the part before the colon:
```yaml
- /path/to/paperless-inbox:/usr/src/paperless/consume
```
To publish on another host port, change the mapping, for example `8010:8000`.
3. Put settings in `docker-compose.env` (all options are in the configuration reference). Set `USERMAP_UID` and `USERMAP_GID` from `id -u` and `id -g` if your user is not 1000.
4. Run `docker compose pull`. The default image comes from the GitHub container registry; use `image: paperlessngx/paperless-ngx:latest` to pull from Docker Hub instead.
5. Run `docker compose up -d`.

## Secrets
Append `_FILE` to a setting to read it from a file, for example `PAPERLESS_DBUSER_FILE=/run/secrets/<SECRET_NAME>`.

## First login
Browse to `http://127.0.0.1:8000`; the first visit prompts you to create the superuser.

Remember that `PAPERLESS_SECRET_KEY` must be set before the container will start.

## Checked
2026-11-04. Compared with the Setup Docker Compose install steps, the _FILE secrets example and the PAPERLESS_SECRET_KEY requirement in the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: steps, secrets example, image registries, secret key requirement. Nothing removed.

Method: documentation only; no commands were run.
