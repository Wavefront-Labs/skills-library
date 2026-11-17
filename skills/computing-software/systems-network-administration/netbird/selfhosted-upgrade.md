---
id: computing-software.systems-network-administration.netbird.selfhosted-upgrade
name: selfhosted-upgrade
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, self-hosted, upgrade, traefik-upgrade, rollback]
level: advanced
status: docs-checked
description: "Upgrade a self-hosted NetBird deployment safely: check versions, pin image tags, pull and recreate, upgrade Traefik and CrowdSec, verify, roll back and migration notes."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/selfhosted/maintenance/upgrade.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Check: the dashboard shows an update indicator; `GET /api/instance/version` (needs a token) reports Dashboard and Management versions. Traefik, CrowdSec and its bouncer are not reported; check those releases yourself.

Before: read release notes (Management, Signal and Relay share version numbers), back up, and set explicit image tags in `docker-compose.yml` since `docker compose pull` fetches whatever the tag points to.

Upgrade:
```
docker compose pull netbird-server dashboard
docker compose up -d --force-recreate netbird-server dashboard
```
Add `proxy` if you use the Reverse Proxy. Keep Management and proxy on matching versions, Management first or together; check with `docker compose exec proxy /go/bin/netbird-proxy --version`.

Traefik and CrowdSec: rerunning the installer is not an upgrade; edit image tags, use full versions or digests, record current ones, change one component at a time, validate with `docker compose config --quiet`, recreate with `--no-deps`. Do not use `docker compose down -v` during an upgrade; preserve the CrowdSec database, bouncer keys and certificate volumes.

Verify: dashboard login, peers, proxied services, certificate issuance for a new hostname, client IPs in proxy logs, CrowdSec blocking; restart and repeat.

Roll back by restoring the recorded digest or tag; restore the backup first if stored data changed. Traefik v3.0.0 through v3.7.11 has a header-alias spoofing vulnerability; use v3.7.12+.

Migration notes: set `aliasHeadersStrategy=delete` on `web` and `websecure` for Traefik v3.7.12+; check the real Docker network name with `docker inspect netbird-traefik`; add `reverseProxy.trustedPeers` in `config.yaml` for pre-September-2026 deployments, then `docker compose restart netbird-server`.

## Checked

2026-11-04: read the upgrade page in full. Confirmed the version check endpoint, image tag advice, pull and recreate commands, proxy and Management version note, the Traefik and CrowdSec procedure, verification table, rollback notes, the Traefik v3.7.12 header advisory, the network name check and the trustedPeers migration. Softened the claim that `down -v` deletes data, which the page states only as something not to do during an upgrade.

Method: documentation only; no commands were run.
