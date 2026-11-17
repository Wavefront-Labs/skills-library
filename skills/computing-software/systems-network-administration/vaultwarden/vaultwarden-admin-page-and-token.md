---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-admin-page-and-token
name: vaultwarden-admin-page-and-token
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, admin-page, admin-token, argon2, argon2id, config-json, docker-compose, dollar-escaping]
level: practitioner
status: docs-checked
description: "Enable the Vaultwarden /admin page with ADMIN_TOKEN, hash it with argon2id using vaultwarden hash, escape dollar signs in compose, and understand config.json overrides."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Enabling-admin-page"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden admin page and ADMIN_TOKEN

Setting `ADMIN_TOKEN` enables `/admin`. Enable HTTPS first. Entering the token gives a JWT session lasting 20 minutes by default (`ADMIN_SESSION_LIFETIME`). To invalidate all sessions, delete `rsa_key.pem` from `DATA_FOLDER` and restart.

Store an argon2id PHC hash instead of the plain token:

```
./vaultwarden hash
docker exec -it vwcontainer /vaultwarden hash
./vaultwarden hash --preset owasp     # m=19 MiB, t=2, p=1 (default m=64 MiB, t=3, p=4)
```
Alternative with the argon2 CLI: `echo -n 'MyPassword' | argon2 "$(openssl rand -base64 32)" -e -id -k 65540 -t 3 -p 4`. Use the `$argon2id$...` string as `ADMIN_TOKEN`, but log in with the original password.

In docker-compose `environment:`, double every `$` (`$$argon2id$$v=19$$...`), or keep the hash single-quoted in a `.env` file and reference `ADMIN_TOKEN=${VAULTWARDEN_ADMIN_TOKEN}`; verify with `docker compose config`.

The first Save in the admin panel creates `config.json` in `DATA_FOLDER`. Its values override matching environment variables, so afterwards change settings in the panel. A plain-text-token warning usually means the env var is being ignored because `config.json` exists. Debug with `printenv ADMIN_TOKEN` inside the container and `grep admin_token data/config.json`; look for stray quotes or doubled `$`.

To disable the page: unset `ADMIN_TOKEN` and `DISABLE_ADMIN_TOKEN`, remove any `admin_token` key from `config.json`, recreate the container.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Enabling-admin-page (session lifetime, rsa_key.pem, hash command and presets, argon2 CLI, $$ escaping, config.json precedence, disabling).
Removed or reworded: the unconfirmed claim that DISABLE_ADMIN_TOKEN opens the panel with no authentication.
Method: documentation only; no commands were run.
