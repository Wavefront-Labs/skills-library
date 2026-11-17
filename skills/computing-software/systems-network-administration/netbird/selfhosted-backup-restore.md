---
id: computing-software.systems-network-administration.netbird.selfhosted-backup-restore
name: selfhosted-backup-restore
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, self-hosted, backup, restore, docker-compose-volumes]
level: advanced
status: docs-checked
description: "Back up and restore a self-hosted NetBird server: what to save, stop-copy-start procedure, restoring on a new host with the same domain and ports."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/selfhosted/maintenance/backup.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Losing the data directory loses accounts, peers, policies and setup keys, and every client must re-enrol. Back up the volumes, not just config.

Back up:
- Config files in the install directory: `docker-compose.yml`, `config.yaml`, `dashboard.env`; plus `proxy.env`, `traefik-dynamic.yaml` for the reverse proxy and the `crowdsec/` directory if used.
- Management data: the `netbird_data` volume (`/var/lib/netbird` in `netbird-server`). Required.
- CrowdSec database (`crowdsec_db`), or the restored proxy cannot authenticate to CrowdSec.
- Certificates (optional; reissuable, but restoring avoids a Let's Encrypt burst).
- PostgreSQL or MySQL, if Management uses one, separately.

Procedure: `docker compose stop`; copy config into `backup/`; `docker compose cp -a` the `/var/lib/netbird/` data out of `netbird-server`; `docker compose start`; archive off the server. It holds encryption keys and secrets, so treat it like a private key.

Restore on a new server (same domain; once DNS points to it, clients reconnect without re-enrolling):
1. Install Docker and Compose; open TCP 80 and 443, UDP 3478, and UDP 51820 if the reverse proxy is enabled.
2. Restore config files.
3. `docker compose create netbird-server` (and `crowdsec`) to make empty volumes.
4. `docker compose cp -a` the data in; optionally certificates.
5. `docker compose up -d`; confirm peers, policies and setup keys.

Older split deployments (`management`, `signal`, `relay`, `coturn`) also back up `Caddyfile`, `management.json`, `relay.env`.

## Checked

2026-11-04: read the backup and restore page in full. Confirmed the file and volume list, the stop-copy-start procedure, the secrecy warning, the same-domain restore requirement, the open ports and the older-setup file list. Nothing removed.

Method: documentation only; no commands were run.
