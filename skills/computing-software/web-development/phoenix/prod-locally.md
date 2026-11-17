---
id: computing-software.web-development.phoenix.prod-locally
name: prod-locally
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, mixenv, secret, production, assets-deploy, runtime-exs, deployment]
level: practitioner
status: docs-checked
description: "Run a Phoenix app in the prod environment on your own machine: secrets, deps, assets.deploy, phx.server and migrations."
sources:
  - https://github.com/phoenixframework/phoenix/blob/main/guides/deployment/prod_locally.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get the production environment running locally to learn how to prepare a Phoenix app for production. For real deployments the guide recommends the releases or containers guides.

## 1. Secrets
Keep secrets (database credentials, the secret Phoenix uses to sign and encrypt) in environment variables, loaded in `config/runtime.exs` (formerly `config/prod.secret.exs` or `config/releases.exs`) at boot time.

```console
$ mix phx.gen.secret
REALLY_LONG_SECRET
$ export SECRET_KEY_BASE=REALLY_LONG_SECRET
$ export DATABASE_URL=ecto://USER:PASS@HOST/database
```

Set `SECRET_KEY_BASE` from the `mix phx.gen.secret` output and `DATABASE_URL` to your database address; do not copy the placeholders. If you hard code secrets in `config/runtime.exs` instead, never check that file into version control.

## 2. Dependencies and compile
```console
$ mix deps.get --only prod
$ MIX_ENV=prod mix compile
```

## 3. Assets
Only needed if you have compilable assets (JavaScript, stylesheets). Phoenix uses `esbuild` by default, wrapped in the `mix assets.deploy` task defined in `mix.exs`. It builds the assets, then generates digests plus a cache manifest so Phoenix can serve them quickly.

```console
$ MIX_ENV=prod mix assets.deploy
```

Locally this creates many digested files in `priv/static`; prune them with `mix phx.digest.clean --all`.

If you skip this step, the server logs an error that it "Could not find static manifest" at `.../priv/static/cache_manifest.json` and tells you to run `mix phx.digest`. Fix by running the steps above, or, if you do not serve assets, remove the `cache_static_manifest` configuration.

## 4. Start the server
Set `PORT` and `MIX_ENV`:
```console
$ PORT=4001 MIX_ENV=prod mix phx.server
```
Detached (keeps running after the terminal closes):
```console
$ PORT=4001 MIX_ENV=prod elixir --erl "-detached" -S mix phx.server
```
Interactive shell:
```console
$ PORT=4001 MIX_ENV=prod iex -S mix phx.server
```

## All together
```console
$ mix deps.get --only prod
$ MIX_ENV=prod mix compile
$ MIX_ENV=prod mix assets.deploy
$ MIX_ENV=prod mix ecto.migrate   # custom tasks such as DB migrations
$ PORT=4001 MIX_ENV=prod mix phx.server
```
Add steps of your own as needed; with a database, run `mix ecto.migrate` before starting.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Source switched to the guide in the Phoenix repository because the guide is not published on hexdocs.

Method: documentation only; no commands were run.
