---
id: computing-software.software-engineering.wails.architecture-overview
name: architecture-overview
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, architecture, webview]
level: practitioner
status: docs-checked
description: "Describe how a Wails app is structured: Go backend, webview frontend, runtime library and bound methods, and the wails.Run entry point."
sources: [https://wails.io/docs/howdoesitwork]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How a Wails application works

Goal: understand the moving parts before designing an app.

## Method

A Wails app is a normal Go application with a webkit frontend:
1. Go side: your application code plus a runtime library (window control and similar operations).
2. Frontend: a webview window displaying your frontend assets. A JavaScript version of the runtime library is available to it (`window.runtime`).
3. Bindings: Go methods can be bound so they appear as JavaScript methods that return Promises.

The main program is a single call to `wails.Run()` with an `options.App` describing the window title, size, assets, callbacks and bound structs. The frontend is described as a browser and webserver in one; the two interaction points between frontend and Go are calling bound Go methods and calling runtime methods.

Minimal shape (abridged from the docs):

```go
//go:embed all:frontend/dist
var assets embed.FS

err := wails.Run(&options.App{
	Title:  "Basic Demo",
	Width:  1024,
	Height: 768,
	AssetServer: &assetserver.Options{Assets: assets},
	OnStartup:  app.startup,
	OnShutdown: app.shutdown,
	Bind: []interface{}{app},
})
```

## Gotchas
- A very small subset of libraries use features unsupported in WebViews; the docs say alternatives or workarounds often exist.

## Related skills
- computing-software.software-engineering.wails.app-options-and-lifecycle
- computing-software.software-engineering.wails.bind-go-methods
- computing-software.software-engineering.wails.call-go-from-frontend

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "How does it work" (howdoesitwork).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
