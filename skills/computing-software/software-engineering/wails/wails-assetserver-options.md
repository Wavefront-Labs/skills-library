---
id: computing-software.software-engineering.wails.wails-assetserver-options
name: wails-assetserver-options
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, assetserver, options, assets]
level: practitioner
status: docs-checked
description: "Configure options.App.AssetServer in Wails: static Assets fs.FS, fallback Handler, Middleware, and the per-platform HTTP feature matrix."
sources: [https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails AssetServer options

Goal: serve the frontend (and dynamic content) through `options.App.AssetServer`, of type `*assetserver.Options`.

## Method

```go
AssetServer: &assetserver.Options{
    Assets:     assets,            // fs.FS
    Handler:    assetsHandler,     // http.Handler
    Middleware: assetsMidldeware,  // assetserver.Middleware
},
```

- `Assets` (`fs.FS`): static frontend files. A GET request is tried here first; if the FS returns `os.ErrNotExist`, handling falls back to `Handler`. If `Assets` is nil, all GET requests go to `Handler`.
- `Handler` (`http.Handler`): called for every GET not served from `Assets` and for all non-GET requests. If not defined, the fallback results are `http.StatusNotFound` for GET and `http.StatusMethodNotAllowed` for other requests.
- `Middleware` (`assetserver.Middleware`): builds a new `http.Handler` for the AssetServer and receives the default handler as an argument, so you can skip the default handler dynamically (for example specialised routing). If undefined, the default request chain runs.

The top-level `Assets` and `AssetsHandler` fields on `options.App` are deprecated; use the ones under `AssetServer`.

## Gotchas stated by the docs

- `Handler` does not work with Vite 5.0.0+ and Wails v2 (changes planned in v3). Stay on Vite 4 if you need it (issue 3240).
- With a frontend dev server there can be limits; for example Vite serves index.html on every path with no file extension.
- Not every `http.Request` feature is supported on every platform. Linux needs WebKit2GTK 2.36+ and build tag `webkit2_36` for POST/PUT/PATCH/DELETE, request headers, and response status codes/headers; request body and body streaming need 2.40+ and build tag `webkit2_40`. WebSockets are unsupported everywhere. Response body streaming is unsupported on Windows. HTTP 30x redirects work only on Windows.
- Enabling those build tags raises your app's minimum WebKit2GTK version.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx), including the AssetServer request-feature matrix with both footnotes (WebKit2GTK 2.36 with tag webkit2_36, 2.40 with tag webkit2_40), the Assets, Handler (Vite 5 info box, issue 3240) and Middleware sections, and the deprecated top-level Assets/AssetsHandler notes. Each platform statement in the Gotchas list was checked against the matrix rows (headers, status codes, body, streaming, WebSockets, 30x redirects). No claims were trimmed.

Method: documentation only; no commands were run.
