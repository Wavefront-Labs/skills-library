---
id: computing-software.web-development.gin.gin-nomsgpack-build-tag
name: gin-nomsgpack-build-tag
category: computing-software
field: web-development
product: gin
tags: [gin, nomsgpack, build-tags, msgpack, binary-size, go-build]
level: practitioner
status: docs-checked
description: "Build a Gin app without MsgPack rendering and binding using the nomsgpack build tag to shrink the binary, and what stops working."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/build-tags/nomsgpack.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/build-tags/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Build Gin without MsgPack

Goal: drop the MsgPack dependency from the compiled binary when you only serve JSON and similar formats.

Gin includes MsgPack rendering and binding by default (through `c.Bind()` and `c.Render()` with the matching content type). The `nomsgpack` build tag excludes that code at compile time.

```sh
go build -tags=nomsgpack .
go run -tags=nomsgpack .
go test -tags=nomsgpack ./...
```

## What changes
- The binary is smaller because the MsgPack serialization library is not linked in.
- Any handler that renders or binds MsgPack no longer works.
- JSON, XML, YAML, TOML and ProtoBuf features keep working; `c.ProtoBuf()` and other non-MsgPack renderers are unaffected.

## Compare sizes
```sh
go build -o gin-app .
ls -lh gin-app

go build -tags=nomsgpack -o gin-app-nomsgpack .
ls -lh gin-app-nomsgpack
```

The exact saving depends on your app; the page says removing MsgPack typically shaves a small amount off the binary.

## Gotchas
- Safe only if you do not call `c.MsgPack()` anywhere and do not serve MsgPack responses.
- It can be combined with a JSON replacement tag, e.g. `-tags=nomsgpack,go_json`.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: build-tags/nomsgpack.md and build-tags/index.md. Confirmed: the three go build/run/test commands, the binary-size effect, MsgPack handlers stop working, JSON/XML/YAML/TOML/ProtoBuf unaffected, and the nomsgpack,go_json combination (shown on the index page). Trimmed nothing. Fixed sources: added build-tags/index.md, which is where the combined-tags example lives.

Method: documentation only; no commands were run.
