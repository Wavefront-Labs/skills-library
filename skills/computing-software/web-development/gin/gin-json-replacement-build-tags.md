---
id: computing-software.web-development.gin.gin-json-replacement-build-tags
name: gin-json-replacement-build-tags
category: computing-software
field: web-development
product: gin
tags: [gin, build-tags, go-json, jsoniter, sonic, avx, json, performance]
level: advanced
status: docs-checked
description: "Swap Gin's encoding/json for go-json, jsoniter or sonic at compile time with go build -tags, with platform limits for sonic (AVX)."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/build-tags/json-replacement.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/build-tags/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replace the JSON encoder with build tags

Goal: speed up JSON serialization without changing application code. Gin uses `encoding/json` by default; one build tag swaps it.

| Tag | Replacement |
|---|---|
| `go_json` | go-json (pure Go, all platforms) |
| `jsoniter` | jsoniter (pure Go, API-compatible, flexible configuration) |
| `sonic avx` | sonic by ByteDance (JIT and SIMD) |

```sh
go build -tags=go_json .
go build -tags=jsoniter .
go build -tags="sonic avx" .
```

The tag works with other commands too:

```sh
go run -tags=go_json .
go test -tags=go_json ./...
```

Tags are comma-separated when combining, e.g. `go build -tags=nomsgpack,go_json .`.

## Choosing
- go-json: safe default, works everywhere, meaningful speedup.
- sonic: highest throughput, x86_64 with AVX only (Intel Sandy Bridge and later, AMD Bulldozer and later); it will not work on ARM or older x86. Use go-json or jsoniter if the target lacks AVX.
- jsoniter: pick it for its configuration features or if you already use it.

## Check it is active
```sh
go build -tags=go_json -o myapp .
go tool nm myapp | grep goccy
```

## Gotchas
- Use only one JSON replacement tag at a time; with several (e.g. `go_json,jsoniter`) behaviour is undefined.
- `nomsgpack` can be combined with any JSON tag.
- Build tags change only how Gin is compiled; handlers and middleware stay the same.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Build Tags index and Build with JSON replacement (go_json, jsoniter, sonic avx, AVX limits, one-tag rule, nomsgpack, nm check).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
