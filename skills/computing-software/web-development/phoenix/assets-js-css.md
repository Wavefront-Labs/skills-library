---
id: computing-software.web-development.phoenix.assets-js-css
name: assets-js-css
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, assets, esbuild, tailwind, javascript, npm, phx-digest, heroicons]
level: practitioner
status: docs-checked
description: "Manage Phoenix assets: esbuild and tailwind defaults, adding JS packages three ways, external images and fonts, custom Node build scripts, and removing esbuild or tailwind."
sources:
  - https://hexdocs.pm/phoenix/asset_management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: configure how a Phoenix 1.7+ app builds JS, CSS and static files.

## Defaults
New apps use `esbuild` and `tailwind` via Elixir wrappers, with no Node.js or Webpack dependency. JS lives at `assets/js/app.js` and is built to `priv/static/assets/js/app.js`: automatically by the `esbuild` watcher in development, by `mix assets.deploy` in production. Tailwind builds all CSS by default. Other assets that need no preprocessing go straight into `priv/static`.

## Third-party JS packages
1. Vendor the file and import by relative path: `import topbar from "../vendor/topbar"`.
2. `npm install topbar --prefix assets`, then `import topbar from "topbar"`. Make sure npm runs on checkout and release builds by adding `"cmd --cd assets npm ci"` to the aliases in `mix.exs`:
```elixir
"assets.build": ["cmd --cd assets npm ci", "tailwind your_app", "esbuild your_app"],
"assets.deploy": [
  "cmd --cd assets npm ci",
  "tailwind your_app --minify",
  "esbuild your_app --minify",
  "phx.digest"
]
```
3. Track a git dependency in `mix.exs`, run `mix deps.get`, then `import topbar from "topbar"`:
```elixir
{:topbar, github: "buunguyen/topbar", app: false, compile: false}
```
New apps use option 3 for Heroicons. Git dependencies cannot be used by Hex packages. With npm-style managers you may need to adjust deployment; with `mix phx.gen.release --docker`, see `Mix.Tasks.Phx.Gen.Release` docs.

## Images and fonts
esbuild tries to resolve files referenced from CSS/JS, so `url(/images/bg.png)` can fail with `Could not resolve "/images/bg.png" (mark it as external to exclude it from the bundle)`. Since v1.6.1, `config/config.exs` marks them external:
```elixir
args: ~w(
  js/app.js
  --bundle
  --format=esm
  --target=es2022
  --outdir=../priv/static/assets/js
  --external:/fonts/*
  --external:/images/*
  --alias:@=.
),
```
Add more `--external:` args for other directories. `mix phx.digest` still cache-busts everything in `priv/static`. To copy fonts that an imported Node package references, add `--loader:.woff=copy`, `--loader:.ttf=copy`, `--loader:.eot=copy`, `--loader:.woff2=copy`.

## esbuild plugins / custom build
The default wrapper config cannot use esbuild plugins. Replace it with a Node script: in `assets/`, `npm install esbuild --save-dev` and `npm install ../deps/phoenix ../deps/phoenix_html ../deps/phoenix_live_view --save` (Yarn equivalents exist). Write `assets/build.js` using `esbuild.build(opts)`, with `--watch` (`esbuild.context(opts)` then `ctx.watch()`, inline sourcemaps) and `--deploy` (minify) flags, `entryPoints: ["js/app.js"]`, `outdir: "../priv/static/assets"`, `external: ["*.css", "fonts/*", "images/*"]`, `nodePaths: ["../deps"]`. Then:
- `config/dev.exs`: `watchers: [node: ["build.js", "--watch", cd: Path.expand("../assets", __DIR__)]]`
- `mix.exs`: `setup: ["deps.get", "ecto.setup", "cmd --cd assets npm install"]` and `"assets.deploy": ["cmd --cd assets node build.js --deploy", "phx.digest"]`
- remove the `esbuild` config from `config/config.exs` and the dependency from `mix.exs`.

## Removing esbuild or tailwind
For another JS tool or an API-only app: remove the `esbuild` config in `config/config.exs` and `config/dev.exs`, remove the `assets.deploy` task, remove the dependency from `mix.exs`, then `mix deps.unlock esbuild`. Do the same for `tailwind` (and optionally `heroicons`) to use another CSS framework.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
