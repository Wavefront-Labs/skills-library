---
id: computing-software.devops-ci-cd.semaphore-ui.install-docker-compose
name: install-docker-compose
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [docker, docker-compose, installation, container, semaphore-ui]
level: intro
status: docs-checked
description: "Run Semaphore UI with Docker Compose using MySQL, Postgres or SQLite, including the required secret variables."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Semaphore with Docker Compose

Goal: start Semaphore UI in containers with a database and an admin user.

Create `docker-compose.yml` with a database service (`mysql:8.0` or `postgres:14`) and the `semaphoreui/semaphore:latest` service publishing `3000:3000`. Key environment variables on the semaphore service:

- `SEMAPHORE_DB_USER`, `SEMAPHORE_DB_PASS`, `SEMAPHORE_DB_HOST`, `SEMAPHORE_DB_PORT` (3306 for MySQL, 5432 for Postgres), `SEMAPHORE_DB_DIALECT` (`mysql`, `postgres`, `sqlite`), `SEMAPHORE_DB`.
- SQLite (v2.16+): `SEMAPHORE_DB_DIALECT: sqlite` and `SEMAPHORE_DB: "/etc/semaphore/semaphore.sqlite"`.
- `SEMAPHORE_PLAYBOOK_PATH: /tmp/semaphore/`.
- Admin account: `SEMAPHORE_ADMIN`, `SEMAPHORE_ADMIN_NAME`, `SEMAPHORE_ADMIN_EMAIL`, `SEMAPHORE_ADMIN_PASSWORD`.
- `SEMAPHORE_ACCESS_KEY_ENCRYPTION`, generated with `head -c32 /dev/urandom | base64`.
- Optional `TZ: UTC` and LDAP variables. The docs compose example uses older names (`SEMAPHORE_LDAP_ACTIVATED`, `_HOST`, `_PORT`, `_DN_BIND`, `_DN_SEARCH`, `_PASSWORD`), but the LDAP page and configuration reference use `SEMAPHORE_LDAP_ENABLE`, `_SERVER`, `_BIND_DN`, `_SEARCH_DN`, `_BIND_PASSWORD`; use the latter.

Add `depends_on` for the database service and a named volume for its data. Start with:

```bash
docker-compose up
```

The UI is then at http://localhost:3000.

Gotchas:
- Set real values for `MYSQL_PASSWORD`/`SEMAPHORE_DB_PASS`, the admin password and the encryption key before first start.
- In Docker Swarm avoid plain credentials; use Docker Secrets with `_FILE` variables such as `SEMAPHORE_ADMIN_PASSWORD_FILE: /run/secrets/semaphore_admin_pw`.
- When switching to Postgres change host, port, dialect, `depends_on` and the volume name together.

Verify: `docker-compose ps` shows the semaphore service up and the login page loads on port 3000.

## Checked

2026-11-04: checked against the Docker installation page, LDAP page and configuration reference. The docs Compose example uses older LDAP variable names than the LDAP page; the skill says so and points to the current names.

Method: documentation only; no commands were run.
