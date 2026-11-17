---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-docker-tags-slim-and-rootless
name: uptime-kuma-docker-tags-slim-and-rootless
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [docker-tags, slim-image, rootless, embedded-mariadb, embedded-chromium, louislam-uptime-kuma]
level: practitioner
status: docs-checked
description: "Choose the right Uptime Kuma image tag: 2 vs slim vs rootless vs beta, and what each gives up."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Docker-Tags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Uptime Kuma Docker tags

Recommended: `2` (latest v2) and `2-slim`. Pinned: `2.x.x` and `2.x.x-slim`. `next` / `next-slim` are the latest version of Uptime Kuma. The `latest` tag is deprecated and always points to v1, so avoid it.

Full versus slim (slim is roughly 300-400 MB smaller):
- Full includes embedded MariaDB (a low-maintenance storage backend) and embedded Chromium (needed for the Browser Engine monitor type, plus fonts).
- Slim has neither. You can still use an external MariaDB/MySQL, and an external Chromium for browser monitors.

Rootless tags (`2-rootless`, `2-slim-rootless`, `2.x.x-rootless`, `next-slim-rootless`) run without root, but:
- not recommended for upgrading from v1 to v2 (likely startup issues);
- make sure the `data` directory is owned by `node:node` (1000:1000), or you will hit startup issues;
- the Docker monitor does not work without extra configuration because it needs root by default;
- embedded MariaDB does not seem to work on Docker Desktop for Windows when `data` is a mounted Windows folder.

Unstable: `beta`, `beta-slim`, `2.x.x-beta.x` and rootless variants; `nightly2` and `nightly2-rootless` are daily development builds for testing only.

The page says to use the slim version if you do not need the embedded MariaDB or Chromium.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Docker Tags page (tag lists, slim versus full, rootless known issues, nightly) and Migration From v1 To v2 page. Removed: The production pinning rule of thumb, the claim that startup fails on wrong ownership (page says startup issues), and the verify line.

Method: documentation only; no commands were run.
