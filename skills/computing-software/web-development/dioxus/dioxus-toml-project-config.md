---
id: computing-software.web-development.dioxus.dioxus-toml-project-config
name: dioxus-toml-project-config
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dioxus-toml, web-app, web-watcher, web-proxy, index-on-404, pre-compress, wasm-opt, base-path]
level: practitioner
status: docs-checked
description: "Configure the Dioxus CLI in Dioxus.toml: application, web.app, web.watcher, web.resource, web.proxy, web.https, pre_compress and wasm_opt keys."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tools/configure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus.toml project configuration

Goal: set CLI behaviour per project. Headers marked mandatory on the page ([application], [web.app], [web.watcher], [web.resource], [web.resource.dev]) can be given with no keys.

## Keys

- `[application]`: `asset_dir` (static assets copied into out_dir after build/serve), `sub_package` (workspace member built by default), plus `name` and `out_dir` in the full example.
- `[web.app]`: `title` (HTML title) and `base_path` (serving subdirectory, e.g. GitHub Pages).
- `[web.watcher]` (dev server): `reload_html` (rebuild index.html each rebuild), `watch_path` (list of dirs), `index_on_404` (serve the root page for unknown routes; needed when the app uses the router).
- `[web.resource]`: `style` and `script` lists, local paths or CDN URLs. `[web.resource.dev]` is the same but only for development servers (e.g. `dx serve` but not `dx serve --release`).
- `[[web.proxy]]`: `backend`, a URL such as `http://localhost:8000/api/`. Requests with that prefix are forwarded to it with path and query unchanged; path rewriting is not supported.
- `[[web.https]]`: `enabled`, `mkcert` (generate certs with the mkcert CLI), `key_path`, `cert_path`.
- `[web]` `pre_compress = true`: brotli-compress built assets in release mode; enabled by default.
- Web wasm_opt: `level` for release builds (z and s optimize for size; 1, 2, 3, 4 optimize for speed, 4 being the default) and `debug = true` to keep debug symbols in release.

## Example

```toml
[application]
name = "project_name"
out_dir = "dist"
asset_dir = "public"

[web.app]
title = "project_name"

[web.watcher]
reload_html = true
watch_path = ["src", "public"]

[web.resource]
style = []
script = []

[[web.proxy]]
backend = "http://localhost:8000/api/"
```

## Gotcha

With a non-Dioxus static host, `index_on_404` does not apply: on GitHub Pages copy `index.html` to `404.html` in the same directory.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 project configuration page (read in full): mandatory headers, application, web.app, web.watcher, web.resource and its dev variant, web.proxy, web.https, pre_compress default, wasm_opt level and debug, and the GitHub Pages 404.html note.

Method: documentation only; no commands were run.
