---
id: computing-software.software-engineering.wails.migrating-v1-to-v2
name: migrating-v1-to-v2
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, migration, v1, v2, bindings, assets, lifecycle]
level: practitioner
status: docs-checked
description: "Port a Wails v1 app to v2: replace CreateApp with wails.Run, move binding and lifecycle hooks into options, embed assets, and convert project.json to wails.json."
sources: [https://wails.io/docs/guides/migrating]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating a Wails v1 app to v2

Goal: convert an existing v1 project to the v2 structure without guessing which API went where.

## Method

1. **Entry point.** v1 used `wails.CreateApp(&wails.AppConfig{...})`, `app.Bind(x)`, `app.Run()`. v2 has one call, `wails.Run(&options.App{...})`, taking the application options (Title, Width, Height, AssetServer, Bind, ...).
2. **Binding.** Only structs can be bound now (v1 also allowed arbitrary functions). Pass instances in the `Bind` field:
   ```go
   err := wails.Run(&options.App{
       Bind: []interface{}{ basic },
   })
   ```
   In the frontend, bound methods moved from `window.backend` to `window.go`.
3. **Lifecycle.** The special struct methods `WailsInit()` and `WailsShutdown()` are gone. Use the `OnStartup`, `OnShutdown` and `OnDomReady` options. `OnDomReady` replaces the v1 `wails:ready` system event. A common pattern keeps them as methods on a struct that stores the context:
   ```go
   func (b *Basic) startup(ctx context.Context) { b.ctx = ctx }
   ```
4. **Runtime.** The runtime now lives in its own package, `github.com/wailsapp/wails/v2/pkg/runtime`, and each call takes the `context.Context` handed to `OnStartup` (e.g. `runtime.LogInfo(ctx, "...")`). Method signatures changed slightly, so check the runtime reference for each call you used.
5. **Assets.** Biggest change. v1 took `JS` and `CSS` options, forcing a bundler to produce one file of each. v2 takes an `embed.FS` and serves it like a web server; Wails finds `index.html` in it and uses that location as the root. No bundling, base64 images or font tricks are required:
   ```go
   //go:embed all:frontend/dist
   var assets embed.FS
   // ...
   AssetServer: &assetserver.Options{ Assets: assets },
   ```
6. **Project config.** `project.json` becomes `wails.json`. Key renames: `binaryname` -> `outputfilename`, `frontend/install` -> `frontend:install`, `frontend/build` -> `frontend:build`. Removed: `description`, `frontend/dir`, `frontend/bridge`, `frontend/serve`, `tags`. New: `wailsjsdir` (where the wailsjs modules are generated), `assetdir` (compiled assets for dev mode, normally inferred), `reloaddirs` (extra comma-separated dirs to watch in dev mode, only for advanced asset setups). `name`, `author` (name/email) and `version` carry over.

## Gotchas

- Bundlers are still allowed; the only requirement is that the final output directory is what you embed and pass to `Assets`.
- Anything that depended on `window.backend` or the `wails:ready` event will stop working until changed.

## Gaps

The page does not list runtime method renames individually; consult the runtime reference.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Migrating from v1" guide.

Corrected or removed: Removed "silently"; the page does not say how old v1 usage fails.

Method: documentation only; no commands were run.
