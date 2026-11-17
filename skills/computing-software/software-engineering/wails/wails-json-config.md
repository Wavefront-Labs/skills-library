---
id: computing-software.software-engineering.wails.wails-json-config
name: wails-json-config
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, configuration, wails-json]
level: practitioner
status: docs-checked
description: "Edit wails.json: frontend install/build/dev commands, asset and wailsjs dirs, dev server address, output name and which keys the CLI flags update."
sources: [https://wails.io/docs/reference/project-config]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wails.json project configuration

Goal: set the core keys the CLI reads on `wails build` and `wails dev`. A JSON Schema is published at https://wails.io/schemas/config.v2.json.

## Method

Keys (strings unless noted):
- `name`, `version` (config version), `outputfilename` (binary name).
- `assetdir`: compiled assets directory, normally inferred. `reloaddirs`: extra reload dirs (advanced).
- `build:dir` (default `build`), `build:tags` (tags always applied).
- `frontend:dir` (default `frontend`), `frontend:install` (often `npm install`), `frontend:build` (often `npm run build`).
- Dev equivalents: `frontend:dev:install` falls back to frontend:install; `frontend:dev:build` falls back to `frontend:dev`, which in turn falls back to frontend:build (frontend:dev is described as replaced by frontend:dev:build).
- `frontend:dev:watcher`: command run in a separate process on `wails dev` (third-party watchers or dev servers).
- `frontend:dev:serverUrl`: third-party dev server URL; `auto` infers it from Vite output. `viteServerTimeout` (number of seconds to wait for Vite detection when serverUrl is `auto`; default 10).
- `wailsjsdir`: where generated JS modules go. `debounceMS` (default 100). `devServer` (address the dev server binds to; default localhost:34115). `appargs`: arguments passed to the application in shell style in dev mode.
- `obfuscated` and `garbleargs`; `nsisType`: `multiple` (one installer per arch, default) or `single` (universal).

The flags `assetdir`, `reloaddirs`, `wailsjsdir`, `debounceMS`, `devserver`, `frontenddevserverurl` and `viteservertimeout`, when passed to `wails build/dev`, update this config and become defaults.

## Related skills
- computing-software.software-engineering.wails.wails-json-hooks-info-bindings
- computing-software.software-engineering.wails.cli-dev-flags

## Checked

2026-11-07. Read the whole Project Config reference page (website/docs/reference/project-config.mdx: the full annotated wails.json structure, the paragraph on flags that update the config, and the JSON Schema link); no includes. Confirmed the frontend:* fallback chain, the build:dir / frontend:dir / viteServerTimeout / debounceMS / devServer defaults, nsisType values, and the list of flags that update the config. Trimmed: "all optional" (the page never says the keys are optional and some are numbers or booleans). Added what the page says about appargs, devServer and viteServerTimeout. The schema file at the linked URL was not opened.

Method: documentation only; no commands were run.
