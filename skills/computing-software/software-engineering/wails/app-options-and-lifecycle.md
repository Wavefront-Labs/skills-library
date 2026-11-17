---
id: computing-software.software-engineering.wails.app-options-and-lifecycle
name: app-options-and-lifecycle
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, options, lifecycle, embed]
level: practitioner
status: docs-checked
description: "Configure wails.Run options (title, size, embedded assets) and use OnStartup, OnDomReady, OnBeforeClose and OnShutdown callbacks with the context."
sources: [https://wails.io/docs/howdoesitwork]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails app options and lifecycle callbacks

Goal: set up `options.App` correctly: assets plus lifecycle hooks that keep the runtime context.

## Method

Options used in the docs example:
- `Title`: window title bar text. `Width` and `Height`: window size.
- `AssetServer: &assetserver.Options{Assets: assets}`: the frontend assets. The page calls the `Assets` option mandatory.
- `OnStartup`: called when the window is created and about to load the frontend assets.
- `OnShutdown`: called when the app is about to quit.
- `Bind`: struct instances exposed to the frontend.

Assets: embed the built frontend and Wails finds `index.html` itself.

```go
//go:embed all:frontend/dist
var assets embed.FS
```

At startup Wails iterates the embedded files looking for the directory containing `index.html` and loads other assets relative to it, so the embed path can be nested. Plain files work; no asset bundle is required. Production binaries use the embedded files, so nothing external needs shipping. Under `wails dev` assets are loaded from disk with live reload, the location inferred from the `embed.FS`.

`OnStartup` and `OnShutdown` receive a standard Go `context.Context`. The runtime calls need this context, so the usual pattern is to save it in `OnStartup`:

```go
func (b *App) startup(ctx context.Context) { b.ctx = ctx }
func (b *App) shutdown(ctx context.Context) {}
```

Also available: `OnDomReady` (frontend finished loading everything in index.html, like body onload) and `OnBeforeClose` (hook window close or app quit).

## Gaps
The full option list lives in the Options reference, not on these pages.

## Related skills
- computing-software.software-engineering.wails.architecture-overview

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "How does it work" (howdoesitwork).

Corrected or removed: Reworded "mandatory AssetServer" to say the page calls the Assets option mandatory; limited the context.Context statement to OnStartup and OnShutdown, which are the callbacks the page says receive it.

Method: documentation only; no commands were run.
