---
id: computing-software.web-development.vapor.vapor-deploy-fly
name: vapor-deploy-fly
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-fly, fly-io, flyctl, postgres, deployment, secrets, migrations]
level: practitioner
status: docs-checked
description: "Deploy a Vapor app on Fly with flyctl: fly launch, fly deploy, Postgres attach, release_command migrations, secrets, env vars, ssh and logs."
sources:
  - https://docs.vapor.codes/deploy/fly/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run a Dockerized Vapor app on Fly (commands are subject to Fly's pricing).

## Setup
- Install `flyctl`: `brew install flyctl` (macOS) or `curl -L https://fly.io/install.sh | sh` (Linux); then `fly auth login`.
- The project needs a Dockerfile at its root (the Vapor templates include one). Start with `vapor new app-name` or a template: template-bare, template-fluent-postgres, template-fluent-postgres-leaf. Fluent with Postgres is recommended if you need a database.

## Launch and deploy
From the app root:

```bash
fly launch
```

It prompts for name (blank for generated), region, and whether to create a database, and writes `fly.toml` (ports, health checks and more). For a fresh `vapor new` project the default `fly.toml` needs no changes. It then offers to deploy now; otherwise use `fly deploy` whenever you want to ship changes.

`fly deploy` builds from `Dockerfile` and `fly.toml`, starts an instance, and runs health checks; it exits with an error if they fail, and Fly rolls back to the latest working version by default. In the app root the CLI finds `fly.toml`; elsewhere append `-a name-of-your-app`.

Background worker (Vapor Queues): leave CMD and ENTRYPOINT alone and add to `fly.toml`:

```
[processes]
  app = ""
  worker = "queues"
```

## Postgres
```bash
fly pg create                         # makes a Fly app that can host databases
fly pg attach name-of-your-postgres-app   # creates a database and user for your app; sets DATABASE_URL
fly pg list                           # find the Postgres app name
```

`fly launch` with a database does both create and attach. `DATABASE_URL` holds credentials, so treat it as sensitive. In `configure.swift`:

```swift
if let databaseURL = Environment.get("DATABASE_URL") {
    try app.databases.use(.postgres(url: databaseURL), as: .psql)
} else {
    // Handle missing DATABASE_URL here...
}
```

## Migrations
```toml
[deploy]
 release_command = "migrate -y"
```

With the default Dockerfile (`ENTRYPOINT` is `./App`) this runs `./App migrate -y`; adapt it if your ENTRYPOINT differs. It runs in a temporary instance with access to the internal network, secrets and env vars, and if it fails the deployment does not continue.

## Secrets, env, access
```bash
fly secrets set MYSECRET=A_SUPER_SECRET_VALUE
```
Shell history records this command; some shells skip commands prefixed with a space; see also `fly secrets import`. Non-sensitive variables go in `fly.toml`:

```toml
[env]
  MAX_API_RETRY_COUNT = "3"
```

Shell into an instance: `fly ssh console -s`. Live logs: `fly logs`.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) deploy/fly, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
