---
id: computing-software.web-development.phoenix.phx-new-project
name: phx-new-project
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, phxnew, phxserver, mixsetup, elixir, ecto, project-setup]
level: intro
status: docs-checked
description: "Create a Phoenix app with mix phx.new, choose flags to skip Ecto, HTML, assets or LiveView, create the database and start the server."
sources:
  - https://hexdocs.pm/phoenix/up_and_running.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: generate a new Phoenix application and get it serving on port 4000.

## Steps
1. Erlang, Elixir and Phoenix must be installed first (see the Installation Guide). Anyone you share the app with needs the same.
2. From any directory run `mix phx.new hello` (absolute or relative path both work; `hello` is the app name).
3. By default it includes Ecto (data store such as PostgreSQL or MySQL), Phoenix.HTML, TailwindCSS and Esbuild, and Phoenix.LiveView. Skip them with:
   - `--no-ecto`
   - `--no-html` and `--no-assets`
   - `--no-live`
   `mix help phx.new` lists all options.
4. Answer `Y` to "Fetch and install dependencies? [Yn]". It runs `mix deps.get`, `mix assets.setup`, `mix deps.compile`. If you answer `n`, it tells you to `cd hello` and run `mix deps.get` yourself.
5. `cd hello`, configure the database in `config/dev.exs`, then `mix ecto.create`. Phoenix assumes a PostgreSQL `postgres` user with password "postgres". If creation fails, see the Ecto guide's Mix tasks section or `mix help ecto.create`.
6. Start with `mix phx.server`, or inside IEx with `iex -S mix phx.server`.
7. Open http://localhost:4000 (port 4000 by default) for the welcome page. If it does not load, try http://127.0.0.1:4000 and check your OS maps "localhost" to 127.0.0.1.
8. Stop the server with `ctrl-c` twice.

## Notes
- A `.gitignore` is generated, so you can `git init` and commit everything not ignored straight away.
- Phoenix Express (a one-line installer) is an alternative on some OSes; `mix phx.new` is the fallback if it fails.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
