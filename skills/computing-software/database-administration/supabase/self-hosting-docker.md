---
id: computing-software.database-administration.supabase.self-hosting-docker
name: self-hosting-docker
category: computing-software
field: database-administration
product: supabase
tags: [self-hosting, docker-compose, secrets, run-sh, env]
level: advanced
status: docs-checked
description: "Self-host Supabase with Docker Compose: pinned clone, required secrets and key formats, run.sh operations, ports, resources and gotchas."
sources:
  - https://supabase.com/docs/guides/self-hosting/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run the Supabase stack yourself with safe secrets.

Setup (pinned tag):

```bash
git clone --depth 1 --branch self-hosted/v0.8.4 https://github.com/supabase/supabase
mkdir supabase-project
cp -rf supabase/docker/. supabase-project
cd supabase-project && cp .env.example .env
docker compose pull
```

A quick-start script also exists (`curl -fsSL https://supabase.link/setup.sh | sh`, then `sh run.sh start`). Generate secrets with `sh utils/generate-keys.sh`, `sh utils/db-passwd.sh` and `sh utils/rotate-new-api-keys.sh --update-env`. Never start with the placeholder defaults.

Key variables: `SUPABASE_PUBLIC_URL`, `API_EXTERNAL_URL`, `SITE_URL`, `DASHBOARD_USERNAME`/`DASHBOARD_PASSWORD`, `POSTGRES_PASSWORD`, `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SECRET_KEY`, SMTP settings. Formats: `SECRET_KEY_BASE` 64+ characters (`openssl rand -base64 48`); `REALTIME_DB_ENC_KEY` exactly 16 (`openssl rand -hex 8`); `VAULT_ENC_KEY` exactly 32 (`openssl rand -hex 16`); `PG_META_CRYPTO_KEY` and the two `LOGFLARE_*_ACCESS_TOKEN` values 32+.

Operations: `sh run.sh start | stop | restart [service] | recreate [service] | logs [service] | printenv <service> | pull`; `sh reset.sh` destroys all data. Use `recreate`, not `restart`, after env or secret changes.

Ports: `8000` API gateway and Studio; `443` behind a reverse proxy.

Gotchas:
- Studio password needs at least one letter and no special characters; `POSTGRES_PASSWORD` letters and numbers only, set before first start.
- CRLF line endings can break the gateway; normalise `docker/` to LF.
- Rotating API keys does not invalidate sessions; regenerating the asymmetric key pair does.
- Never expose `SUPABASE_SECRET_KEY` in client code.
- Minimum 4 GB RAM, 2 cores, 40 GB SSD; recommended 8 GB, 4 cores, 80 GB. Logs and analytics add load.

## Checked

Confirmed against the page: clone commands, quick-start script, utils scripts, URL variables, dashboard credentials, secret length rules and generator commands, run.sh commands, reset.sh, recreate vs restart, ports, Studio password rule, CRLF gotcha, key rotation behaviour, resource table. Changed the pinned tag from self-hosted/v0.8.3 to the page's self-hosted/v0.8.4 and dropped JWT_SECRET from the key variable list (it appears only in a generic .env snippet).

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/self-hosting/docker (apps/docs/content on GitHub master), read in full.
