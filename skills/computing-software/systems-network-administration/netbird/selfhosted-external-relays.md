---
id: computing-software.systems-network-administration.netbird.selfhosted-external-relays
name: selfhosted-external-relays
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, self-hosted, external-relay, stun, relay-secret]
level: advanced
status: docs-checked
description: "Add external relay servers to self-hosted NetBird: requirements, shared secret, relay.env and Compose, config.yaml stuns and relays, verification and failover tests."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/selfhosted/maintenance/scaling/set-up-external-relays.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enterprise with a commercial licence uses a separate guide: this procedure generates a new shared secret and would stop traffic event logging.

Per relay: Linux VM (1 CPU, 1 GB RAM), public IP, domain, Docker. Open 443/tcp, 443/udp and 3478/udp (STUN); port 80 not needed. Keep both 443 rules because clients race WebSocket (TCP) and QUIC (UDP) and a closed UDP port fails silently.

Steps:
1. `openssl rand -base64 32`; use the same value as `NB_AUTH_SECRET` on every relay and as `relays.secret` on the main server (copy, do not retype).
2. Create `relay.env` (log level, listen address, exposed `rels://` address, secret, Let's Encrypt and STUN settings), `chmod 600`.
3. Compose file for `netbirdio/relay`, publishing 443 TCP and UDP and 3478/udp.
4. `docker compose up -d`; logs should show WebSocket and QUIC listeners and STUN; `curl -v` the domain.

Alternatives: own certificates (drop `NB_LETSENCRYPT_*`, set `NB_TLS_CERT_FILE` and `NB_TLS_KEY_FILE`, restart on renewal) or behind a proxy (forwards WebSockets to port 8080, narrow `NB_TRUSTED_PROXIES`, no QUIC).

Main server: ADD `stuns` and `relays` under the existing `server:` block of `config.yaml`; do not overwrite other keys. Listing `relays.addresses` disables the embedded relay and STUN. Bring relays online first (the switch drops connections). Apply a `config.yaml`-only change with `docker compose restart netbird-server`; if you also removed the STUN port mapping from `docker-compose.yml`, use `docker compose up -d netbird-server` instead (a restart cannot remove a published port). Avoid `docker compose down`. `relays` and `stuns` need v0.65.0+.

Verify: `netbird status -d` shows your STUN and `rels://` relays Available; stop the relay a peer uses to test failover; test `NB_FORCE_RELAY=true` via `netbird service reconfigure`, then back to false.

## Checked

2026-11-04: read the external relays page in full. Confirmed requirements and ports, the TLS-ALPN-01 note (no port 80), the shared secret rule, relay.env and Compose layout, proxy and own-certificate alternatives, the config.yaml additions, the embedded relay switch-off, the restart commands and the verification and failover tests. Added the restart nuance and the version gate from the page.

Method: documentation only; no commands were run.
