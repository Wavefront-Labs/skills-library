---
id: computing-software.web-development.phoenix.directory-structure
name: directory-structure
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, libhello, libhelloweb, assets, directory-structure, config, elixir]
level: intro
status: docs-checked
description: "Map of a generated Phoenix project: what _build, assets, config, deps, lib, priv and test hold, and what lives in lib/hello versus lib/hello_web."
sources:
  - https://hexdocs.pm/phoenix/directory_structure.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: know where things live in a project created by `mix phx.new hello`.

## Top level
- `_build` - compilation artifacts from `mix`. Do not commit; safe to delete (forces a full rebuild).
- `assets` - front-end sources (JavaScript, CSS), bundled by `esbuild`. Static files such as images and fonts go in `priv/static`.
- `config` - `config/config.exs` is the entry point and at its end imports `dev.exs`, `test.exs`, `prod.exs`. `config/runtime.exs` runs afterwards and is the best place to read secrets and other dynamic configuration.
- `deps` - Mix dependencies, listed in `defp deps do` in `mix.exs`. Do not commit; safe to delete (re-downloaded).
- `lib` - application source, split into `lib/hello` and `lib/hello_web`.
- `priv` - production resources that are not source: database scripts, translation files, images. Generated assets go to `priv/static/assets`.
- `test` - tests, often mirroring `lib`.

## lib/hello (business domain, the "Model")
- `application.ex` - `Hello.Application`; its children start in order and stop in reverse order: `HelloWeb.Telemetry`, `Hello.Repo`, `{Phoenix.PubSub, name: Hello.PubSub}`, `HelloWeb.Endpoint`.
- `mailer.ex` - `use Swoosh.Mailer, otp_app: :hello`.
- `repo.ex` - `use Ecto.Repo, otp_app: :hello, adapter: Ecto.Adapters.Postgres` (Postgres is the default).

## lib/hello_web (web layer, View and Controller)
- `controllers/` - `page_controller.ex`, `page_html.ex`, `error_html.ex`, `error_json.ex`, `page_html/home.html.heex`.
- `components/` - `core_components.ex`, `layouts.ex`, `layouts/root.html.heex`.
- `endpoint.ex` - entry point for HTTP requests, leads to the router.
- `router.ex` - dispatches requests to controllers.
- `telemetry.ex` - supervisor for telemetry/metrics processes.
- `gettext.ex` - internationalization; skippable if unneeded.

## Assets
- Since Phoenix v1.6 `esbuild` (via the `esbuild` Elixir package) compiles assets; config is in `config/config.exs`.
- Everything in `priv/static` is served by `Plug.Static` configured in `lib/hello_web/endpoint.ex`.
- In dev (`MIX_ENV=dev`) changes under `assets` are watched and the browser is updated.
- `mix phx.new` options can change or remove the `assets` directory (for example API-only apps). Tailwind CSS ships by default but any CSS framework can replace it.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
