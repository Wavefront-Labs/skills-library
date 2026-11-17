---
id: computing-software.digital-privacy-hygiene.password-managers.bitwarden-cli-serve-api
name: bitwarden-cli-serve-api
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, bw-serve, bitwarden-cli, password-manager-cli]
level: practitioner
status: docs-checked
description: "Run bw serve to expose the Bitwarden vault as a local REST API for scripts, bind it to localhost, unlock and lock it, and avoid exposing secrets."
sources:
  - "https://bitwarden.com/help/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bitwarden CLI serve API

**Goal:** let local automation (home-lab scripts, a launcher) read vault items via HTTP instead of repeatedly
spawning `bw` and handling `BW_SESSION`.

## Start it
```
bw login            # once
bw serve --hostname localhost --port 8087
```
The default port is 8087 and the default bind is localhost. `--hostname all` removes hostname binding and lets any
machine on the network call the API; do not use it.

## Use it
```
# endpoint paths are not kept here; use the Vault Management API spec
```
The CLI help page says `bw serve` exposes every CLI action as RESTful HTTP calls and points to the API spec for the
endpoints; take paths and payloads from that spec rather than from memory.

## Security model
- Once unlocked, **any local process** that can reach the port can read the vault. Run it only on a single-user
  machine, lock it after use, or run it inside a container/namespace that only your script can reach.
- Origin protection blocks browser requests; don't pass `--disable-origin-protection` unless you understand that
  any web page could then query it.
- Don't put the master password in a script; prompt, or use an API key for login plus interactive unlock.

## Gotchas
- Sync the vault (`bw sync` or the spec's equivalent) before reading recently changed items.
- For machine/CI secrets, consider Bitwarden Secrets Manager rather than a personal vault over HTTP.

## Checked
2026-11-01: `bw serve` with `--port`/`--hostname`, default port 8087, default localhost bind, `--hostname all`
warning, and origin blocking with `--disable-origin-protection` confirmed against the Bitwarden CLI help page. Removed:
curl endpoint examples and the vault-caching claim (the API spec page could not be read).
Method: documentation only; no commands were run.
