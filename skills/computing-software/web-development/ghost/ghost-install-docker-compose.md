---
id: computing-software.web-development.ghost.ghost-install-docker-compose
name: ghost-install-docker-compose
category: computing-software
field: web-development
product: ghost
tags: [ghost, docker, docker-compose, caddy, mysql, tinybird, self-hosting]
level: advanced
status: docs-checked
description: "Self-host Ghost 6 with the Docker Compose tooling: clone ghost-docker, edit .env and the Caddyfile, and enable Tinybird analytics."
sources:
  - https://github.com/TryGhost/docs/blob/main/install/docker.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Ghost with Caddy and MySQL in Docker.

The docs present this as a preview tooling with full support for the Social Web (ActivityPub) and Web Analytics (Tinybird). It runs Ghost, Caddy as the web server and MySQL.

Prerequisites: a Linux server, Docker 20.10.13 or higher, a domain with a DNS A record, an SMTP service for transactional mail, and optionally a Tinybird account.

Steps:
1. `git clone https://github.com/TryGhost/ghost-docker.git /opt/ghost && cd /opt/ghost`
2. `cp .env.example .env` and `cp caddy/Caddyfile.example caddy/Caddyfile`
3. Edit `.env`: `DOMAIN`, optional `ADMIN_DOMAIN`, `DATABASE_ROOT_PASSWORD` and `DATABASE_PASSWORD` (generate with `openssl rand -hex 32`) and the SMTP section.
4. In the Caddyfile uncomment only the blocks you need (separate admin domain, redirect www to root or root to www) and change `CHANGE_ME` where required.
5. `docker compose pull` then `docker compose up -d`.
6. Finish setup at `/ghost`.

Web analytics: with a Tinybird account and workspace, from the install directory run `docker compose run --rm tinybird-login`, then `docker compose run --rm tinybird-sync`, `docker compose run --rm tinybird-deploy` (expect "Deployment #1 is live!") and `docker compose run --rm tinybird-login get-tokens`. Paste the values into the "Tinybird configuration" section of `.env`, set `COMPOSE_PROFILES=analytics` (or `analytics,activitypub`) at the top, then `docker compose pull` and `docker compose up -d`.

ActivityPub: new installs use the Ghost(Pro) hosted ActivityPub service by default (free to self-hosters up to 2000 followers, 2000 following and 100 interactions per day). To self-host it, add `activitypub` to `COMPOSE_PROFILES`, uncomment `ACTIVITYPUB_TARGET=activitypub:8080` and run `docker compose up -d --force-recreate ghost caddy`. With a `www` DOMAIN, redirect the root domain to www in the Caddyfile for ActivityPub to work.

Updating: in the install directory run `git pull`, `docker compose pull`, `docker compose up -d`. After changing `.env`, recreate with `docker compose up -d --force-recreate ghost` (add `caddy` when `DOMAIN`, `ADMIN_DOMAIN` or `ACTIVITYPUB_TARGET` changed). Do not change the `DATABASE_xxx` variables after the database is initialised.

An existing Ghost-CLI site can be migrated in place on the same server: do the clone, config and Caddy steps, then run `bash scripts/migrate.sh` as root (it asks to stop Nginx, which takes the site offline; `bash recovery_instructions.sh` restores the original site). For problems, `docker compose logs caddy` then `docker compose logs ghost`.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 391 lines, no imported snippets): install/docker.mdx, and the stripped ghost-docker repo page (only its README intro, IPv6 note and licence; it does not list compose files). Prerequisites, clone path, `.env` keys, Caddyfile blocks, Tinybird commands and update commands match docker.mdx. The Tinybird section covering automation analytics (TINYBIRD_SYNC_AUTH, beta) was read but is not summarised here. Removed: the Verify step with `docker compose ps` (not on the page); added profiles, ActivityPub, update and migration details.
Method: documentation only; no commands were run.
