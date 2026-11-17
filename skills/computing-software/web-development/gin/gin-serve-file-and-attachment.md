---
id: computing-software.web-development.gin.gin-serve-file-and-attachment
name: gin-serve-file-and-attachment
category: computing-software
field: web-development
product: gin
tags: [gin, c-file, c-filefromfs, c-fileattachment, content-disposition, path-traversal, http-filesystem]
level: practitioner
status: docs-checked
description: "Serve files from Gin with c.File, c.FileFromFS and c.FileAttachment, and avoid path traversal by confining access to an http.FileSystem."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/serving-data-from-file.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serving files and downloads in Gin

Goal: return a file from a handler, inline or as a download.

- `c.File(path)`: serves a local file; content type is detected automatically.
- `c.FileFromFS(path, fs)`: serves from an `http.FileSystem` (embed.FS, custom storage, or a directory tree you want to confine access to).
- `c.FileAttachment(path, filename)`: sets `Content-Disposition: attachment`, so the browser offers a save dialog using the filename you supply regardless of the on-disk name.

```go
router.GET("/local/file", func(c *gin.Context) {
  c.File("local/file.go")
})

var fs http.FileSystem = http.Dir("/var/www/assets")
router.GET("/fs/file", func(c *gin.Context) {
  c.FileFromFS("fs/file.go", fs)
})

router.GET("/download", func(c *gin.Context) {
  c.FileAttachment("local/report-2024-q1.xlsx", "quarterly-report.xlsx")
})
```

```sh
# -v shows the Content-Disposition header
curl -v http://localhost:8080/download --output report.xlsx
```

## Gotcha: path traversal
Never pass user input straight to `c.File()` or `c.FileAttachment()`; a path like `../../etc/passwd` would expose arbitrary files. Validate and sanitize paths, or confine access with `c.FileFromFS()`:

```go
// DANGEROUS
router.GET("/files/:name", func(c *gin.Context) {
  c.File(c.Param("name"))
})

// SAFE: restricted to one directory
var safeFS http.FileSystem = http.Dir("/var/www/public")
router.GET("/files/:name", func(c *gin.Context) {
  c.FileFromFS(c.Param("name"), safeFS)
})
```

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: rendering/serving-data-from-file.md. Confirmed: File, FileFromFS and FileAttachment behaviour, the example handlers, curl -v for Content-Disposition, and the path-traversal caution with the safe http.Dir example. Trimmed nothing. Fixed the source (bogus website/ segment).

Method: documentation only; no commands were run.
