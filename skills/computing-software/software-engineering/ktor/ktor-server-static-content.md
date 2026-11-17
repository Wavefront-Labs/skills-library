---
id: computing-software.software-engineering.ktor.ktor-server-static-content
name: ktor-server-static-content
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, static-content, staticfiles, staticresources, staticzip, caching, precompressed]
level: practitioner
status: docs-checked
description: "Serve static files in Ktor from folders, ZIP archives or classpath resources, with index, pre-compressed, default, fallback, caching, exclude and content-type options."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-static-content.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving static content in Ktor

Three sources, each a function used inside routing:
- `staticFiles()`: local folder; relative paths use the current working directory. A request under the URL prefix maps to the physical folder (for example `/resources` to the `files` folder) and Ktor serves files recursively when URL path and filename match.
- `staticZip()`: maps requests to the contents of a ZIP file (for example root `/` to `text-files.zip`). It reloads automatically: if the ZIP's parent directory changes, the ZIP file system is reloaded on the next request.
- `staticResources()`: classpath; maps a URL prefix to a resource package (for example `/resources` to the `static` package).

## Options (inside the static block)
- Index: `index.html` is served for a directory by default; set another with the `index` parameter (then `/custom` serves `/custom_index.html`).
- `preCompressed()`: with the supported formats listed, Ktor checks the client's encodings and serves a matching file such as `/js/script.js.br` or `/js/script.js.gz` instead of compressing dynamically with the Compression plugin.
- `enableAutoHeadResponse()`: answers `HEAD` for every path that has a `GET`.
- `default()`: file to reply with when a request has no corresponding file (e.g. `index.html`).
- `contentType()`: Ktor guesses `Content-Type` from the extension; use this to set it explicitly for chosen files.
- `cacheControl()`: sets `Cache-Control`. With the ConditionalHeaders plugin installed, supply `etag` and `lastModified` values per resource so unchanged content is not resent. A predefined provider generates a strong `ETag` from the SHA-256 hash of the content; on an I/O error no `ETag` is generated.
- `exclude()`: excluded files answer `403 Forbidden`.
- Extension fallbacks: given extensions are appended when a file is not found (`/index` finds `/index.html`).
- `fallback()`: inspect the requested path and the `ApplicationCall` and redirect, return a status or serve another file; works inside `staticFiles()`, `staticResources()`, `staticZip()` and `staticFileSystem()`.
- `modify()`: apply custom changes to the resulting response.

Missing content gives `404 Not Found` automatically; customise via the StatusPages plugin.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-static-content.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
