---
id: computing-software.web-development.gin.gin-static-files
name: gin-static-files
category: computing-software
field: web-development
product: gin
tags: [gin, static, staticfs, staticfile, http-dir, directory-listing, path-traversal]
level: practitioner
status: docs-checked
description: "Serve static assets in Gin with router.Static, StaticFS and StaticFile, and avoid exposing sensitive files or directory listings."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/serving-static-files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serving static files in Gin

Goal: expose a directory or single file over HTTP.

- `router.Static(relativePath, root)`: maps requests under `relativePath` to files under `root`, so `router.Static("/assets", "./assets")` serves `./assets/style.css` at `/assets/style.css`.
- `router.StaticFS(relativePath, fs)`: same, but takes an `http.FileSystem`, for embedded filesystems or customised directory-listing behaviour.
- `router.StaticFile(relativePath, filePath)`: a single file, e.g. `/favicon.ico` or `/robots.txt`.

```go
router := gin.Default()
router.Static("/assets", "./assets")
router.StaticFS("/more_static", http.Dir("my_file_system"))
router.StaticFile("/favicon.ico", "./resources/favicon.ico")

// Listen and serve on 0.0.0.0:8080
router.Run(":8080")
```

## Gotchas (path traversal / exposure)
- Everything in the directory passed to `Static()` or `http.Dir()` is reachable by any client; keep config files, `.env` files, private keys and database files out of it.
- Use a dedicated directory containing only public files; avoid `"."` or `"/"`, which could expose the whole project or filesystem.
- The standard `http.Dir` enables directory listing by default. To disable listings, use `StaticFS` with a custom `http.FileSystem` implementation.

## Choosing a method
Pick `Static` for a whole folder of assets, `StaticFile` for one-off files like `/favicon.ico` and `/robots.txt`, and `StaticFS` when files come from an embedded filesystem or need custom resolution. In the example, `http.Dir("my_file_system")` is served at `/more_static`.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: rendering/serving-static-files.md. Confirmed: Static, StaticFS and StaticFile descriptions, the example, and the three security bullets (whole directory exposed, avoid "." and "/", http.Dir enables directory listing). Trimmed nothing. Fixed the source (bogus website/ segment).

Method: documentation only; no commands were run.
