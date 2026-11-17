---
id: computing-software.web-development.rails.deploying-with-kamal
name: deploying-with-kamal
category: computing-software
field: web-development
product: rails
tags: [rails, kamal, kamal-proxy, docker, deployment, zero-downtime, accessories, ruby, web-development, rails-deployment]
level: practitioner
status: docs-checked
description: "Deploying Rails with Kamal 2: deploy.yml servers and roles, kamal-proxy with SSL and health checks, secrets, accessories, volumes, rollbacks and day-two commands."
sources:
  - https://kamal-deploy.org/docs/configuration/overview/
  - https://kamal-deploy.org/docs/commands/view-all-commands/
  - https://kamal-deploy.org/docs/configuration/proxy/
  - https://kamal-deploy.org/docs/configuration/builder-examples/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying with Kamal

**Goal:** zero-downtime Docker deploys of a Rails app to your own servers with one command.

## 1. Configure
```yaml
# config/deploy.yml
service: shop
image: acme/shop
servers:
  web: [203.0.113.10, 203.0.113.11]
  job:
    hosts: [203.0.113.12]
    cmd: bin/jobs                         # Solid Queue worker
proxy:
  ssl: true                               # TLS handled by kamal-proxy
  host: shop.example.com
  healthcheck: { path: /up, interval: 3 }
registry:
  server: ghcr.io
  username: acme
  password: [KAMAL_REGISTRY_PASSWORD]
builder:
  arch: amd64
env:
  clear: { SOLID_QUEUE_IN_PUMA: false, DB_HOST: shop-db }
  secret: [RAILS_MASTER_KEY, POSTGRES_PASSWORD]
volumes:
  - "shop_storage:/rails/storage"         # Active Storage Disk / SQLite
accessories:
  db:
    image: postgres:17
    host: 203.0.113.12
    env: { secret: [POSTGRES_PASSWORD] }
    directories: ["data:/var/lib/postgresql/data"]
```
```bash
# .kamal/secrets  (committed; values come from env/password managers, not literals)
KAMAL_REGISTRY_PASSWORD=$KAMAL_REGISTRY_PASSWORD
RAILS_MASTER_KEY=$(cat config/master.key)
POSTGRES_PASSWORD=$(op read op://prod/shop/db_password)
```

## 2. Deploy
```bash
kamal setup          # first time: installs Docker, boots accessories and proxy, deploys
kamal deploy         # build, push, pull, start new container, wait for health, switch traffic, stop old
kamal rollback <version>
kamal app details / kamal app logs -f
```
Health check: by default kamal-proxy requests `/up` once a second until the deploy timeout, with a 5-second timeout per request; once the app is up it stops checking.

## 3. Migrations
With multiple web hosts, migrations can race - keep them backward-compatible, or run them from a pre-deploy hook or a single role.

## 4. Gotchas
- Building amd64 images from an ARM64 machine (Apple Silicon) can be sped up with a remote builder: `builder: { arch: amd64, remote: ssh://... }` (Docker must run on the remote host).

## Checked
2026-10-31. Confirmed against kamal-deploy.org: configuration overview (secrets path default `.kamal/secrets`, hooks incl. pre-deploy, deploy timeout), proxy page (`ssl`, healthcheck `/up` default polling and `interval`), builder examples (`arch`, `remote`), and the command list (`setup`, `deploy`, `rollback [VERSION]`, accessories). Removed: `kamal lock release`, `app exec --reuse` and console aliases, Let's Encrypt wording, the Rails entrypoint `db:prepare` claim, `SECRET_KEY_BASE_DUMMY`, and the accessory and firewall remarks.
Method: documentation only; no commands were run.

## Verify
- [ ] `kamal deploy` during a load test produces no 5xx.
- [ ] `kamal rollback` to the previous version works.
- [ ] Secrets don't appear in `deploy.yml` or git history.
