---
id: computing-software.web-development.phoenix.releases
name: releases
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, deployment, releases, mixrelease, phxgenrelease, migrations, elixir, production]
level: advanced
status: docs-checked
description: "Package a Phoenix app as an Elixir release: set secrets, compile assets, run phx.gen.release, mix release, migrations via eval, and custom release commands."
sources:
  - https://hexdocs.pm/phoenix/releases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a self-contained release (Erlang VM, Elixir, your code and deps) to drop onto a production machine.

## Steps
```console
$ mix phx.gen.secret
$ export SECRET_KEY_BASE=REALLY_LONG_SECRET
$ export DATABASE_URL=ecto://USER:PASS@HOST/database

$ mix deps.get --only prod
$ MIX_ENV=prod mix compile
$ MIX_ENV=prod mix assets.deploy

$ mix phx.gen.release
$ MIX_ENV=prod mix release
```
`mix phx.gen.release` creates `rel/overlays/bin/server` (+ `.bat`), `rel/overlays/bin/migrate` (+ `.bat`) and `lib/my_app/release.ex`. Files in `rel/overlays` are copied into every release. `mix release` reads `config/runtime.exs` at runtime.

Run the built release (replace `my_app`):
- `_build/prod/rel/my_app/bin/my_app start`
- `_build/prod/rel/my_app/bin/server` (starts with the Phoenix server running)
- once running: `.../bin/my_app remote` to connect, `.../bin/my_app stop` to stop (SIGINT/SIGTERM also work)

Copy `_build/prod/rel/my_app` to any machine with the same OS and architecture as the one that built it. For Elixir release details, see the `mix release` docs.

## Migrations
Releases have no Mix, so migrations run through the generated `MyApp.Release` module (replace the app names):
```elixir
defmodule MyApp.Release do
  @app :my_app

  def migrate do
    load_app()

    for repo <- repos() do
      {:ok, _, _} = Ecto.Migrator.with_repo(repo, &Ecto.Migrator.run(&1, :up, all: true))
    end
  end

  def rollback(repo, version) do
    load_app()
    {:ok, _, _} = Ecto.Migrator.with_repo(repo, &Ecto.Migrator.run(&1, :down, to: version))
  end

  defp repos do
    Application.fetch_env!(@app, :ecto_repos)
  end

  defp load_app do
    Application.ensure_all_started(:ssl)
    Application.ensure_loaded(@app)
  end
end
```
Rebuild with `MIX_ENV=prod mix release`, then:
```console
$ _build/prod/rel/my_app/bin/my_app eval "MyApp.Release.migrate"
```
Some platforms (e.g. Fly.io) have migration hooks; otherwise migrate at start by editing the end of the generated `server` script:
```bash
./my_app eval MyApp.Release.migrate
PHX_SERVER=true exec ./my_app start
```

## Custom commands
Write any production command the same way: each calls `load_app`, which only loads the app (`Application.ensure_loaded/1`) without starting it. If a command needs the app running use `Application.ensure_all_started/1`, which starts the whole supervision tree including the endpoint. To avoid that, set a flag and have the application start fewer children:
```elixir
defp start_app do
  load_app()
  Application.put_env(@app, :minimal, true)
  Application.ensure_all_started(@app)
end
```
and check `Application.get_env(@app, :minimal)` in your application module.

## Clustering
Configure clustering, especially with long-polling (enabled by default but can be disabled); details depend on the platform (see the Phoenix clustering guide).

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
