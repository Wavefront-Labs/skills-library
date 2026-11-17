---
id: computing-software.devops-ci-cd.gitea.docker-compose
name: docker-compose
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-docker-compose, gitea, docker-compose, user-uid, user-gid, postgres-18, depends-on-db]
level: practitioner
status: docs-checked
description: "Run Gitea with docker compose: image tags, ports, UID/GID ownership of the data volume, MySQL or PostgreSQL sidecar, named volumes, upgrade by pull."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/with-docker.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea with docker compose (rootful image)

Minimal `docker-compose.yml`:
```yaml
networks:
  gitea:
    external: false
services:
  server:
    image: docker.gitea.com/gitea:<version>
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    networks: [gitea]
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "222:22"
```
Tags: `latest`, `1`, a pinned release, `main-nightly`, or `1.x-nightly` for a release branch. With no DB configured Gitea uses SQLite3.

- **Permissions**: with host volumes the volume must be owned by `USER_UID`/`USER_GID` or the container may not start. Named volumes (`gitea:/data` plus a top-level `volumes: gitea: {driver: local}`) avoid this.
- **Ports**: change only the host side (`8080:3000`, `2221:22`). If HTTP is not on 3000 inside, set `LOCAL_ROOT_URL = http://localhost:3000/` to match in `app.ini`.
- **Database sidecar**: add `depends_on: [db]` and `GITEA__database__DB_TYPE=mysql|postgres`, `HOST=db:3306|db:5432`, `NAME`, `USER`, `PASSWD`. The docs use `mysql:8` and `postgres:18` images; the PostgreSQL example pins a major version because PostgreSQL does not upgrade its data directory itself (needs `pg_upgrade` or dump/restore). In the install wizard the DB host is `db`.
- **Run**: `docker compose up -d`, `docker compose ps`, `docker compose logs`, `docker compose down` (volumes survive).
- **Upgrade**: edit the tag if pinned, `docker compose pull`, `docker compose up -d`. Keep data outside the container.
- Customisation files go under `/data/gitea` (e.g. `/data/gitea/public/robots.txt`); config lives at `/data/gitea/conf/app.ini`.

Rootful and rootless images are not interchangeable: never switch by editing `image:` alone (see `gitea-docker-rootless`).

## Checked
2026-11-03. Every claim confirmed against the Gitea docs pages with-docker.md and database-preparation.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
