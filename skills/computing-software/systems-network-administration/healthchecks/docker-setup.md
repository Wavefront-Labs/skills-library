---
id: computing-software.systems-network-administration.healthchecks.docker-setup
name: docker-setup
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, docker-compose, env-file, prebuilt-images, docker-superuser]
level: practitioner
status: docs-checked
description: "Run Healthchecks with Docker Compose: required .env variables, starting containers, creating a superuser, bundled background commands and pre-built image tags."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_docker.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/docker/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Copy `docker/.env.example` to `docker/.env` and set:
   `ALLOWED_HOSTS`, `DEFAULT_FROM_EMAIL`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `SECRET_KEY` (a random value), `SITE_ROOT` (public base URL).
2. Start: `cd docker && docker compose up`. The sample runs one database node and one web node on the same host, without TLS.
3. Superuser:

```
docker compose run web /opt/healthchecks/manage.py createsuperuser
```

Add `--email` and `--password` for non-interactive use. Then open http://localhost:8000.

On container start the image runs `migrate` and, in the background, `sendalerts`, `sendreports` and `smtpd` (the SMTP listener starts only when `SMTPD_PORT` is set). `collectstatic` and `compress` run at build time. Run `createsuperuser`, `pruneobjects`, `prunetokenbucket`, `pruneusers` and `settelegramwebhook` manually with `docker compose run web /opt/healthchecks/manage.py <command>`.

Pre-built images: Docker Hub `healthchecks/healthchecks`, for amd64, arm/v7 and arm64, with PostgreSQL and MySQL drivers, whitenoise and apprise. To pin a version, replace the `build` section in `docker-compose.yml` with `image: healthchecks/healthchecks:vX.Y`; to upgrade change the version and run `docker compose up`.

## Checked

2026-11-04. Confirmed against the Healthchecks Docker documentation and docker README: the minimum .env fields, compose up, createsuperuser command and its --email and --password form, which manage.py commands run automatically versus manually, and the pre-built image facts and version pinning. Added the SMTPD_PORT condition for smtpd.

Method: documentation only; no commands were run.
