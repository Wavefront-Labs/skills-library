---
id: computing-software.web-development.gin.gin-render-formats
name: gin-render-formats
category: computing-software
field: web-development
product: gin
tags: [gin, rendering, c-json, c-xml, c-yaml, c-toml, c-protobuf, indentedjson, content-negotiation]
level: intro
status: docs-checked
description: "Render JSON, XML, YAML, TOML or ProtoBuf from a Gin handler with c.JSON, c.XML, c.YAML, c.ProtoBuf and switch format by query parameter."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/index.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/rendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rendering JSON, XML, YAML, TOML and ProtoBuf in Gin

Goal: send a response in a chosen format. Every renderer takes an HTTP status code and data; Gin sets `Content-Type` and writes the body.

```go
c.JSON(http.StatusOK, data)     // application/json
c.XML(http.StatusOK, data)      // application/xml
c.YAML(http.StatusOK, data)     // application/x-yaml
c.TOML(http.StatusOK, data)     // application/toml
c.ProtoBuf(http.StatusOK, data) // application/x-protobuf
```

Serve one handler in several formats by switching on a query parameter:

```go
router.GET("/user", func(c *gin.Context) {
  user := gin.H{"name": "Lena", "role": "admin"}
  switch c.Query("format") {
  case "xml":
    c.XML(http.StatusOK, user)
  case "yaml":
    c.YAML(http.StatusOK, user)
  default:
    c.JSON(http.StatusOK, user)
  }
})
```

## Data shapes
- `gin.H` is a shortcut for `map[string]interface{}`.
- Structs work too; a tag such as `json:"user"` renames the field in the output.
- `c.IndentedJSON()` gives human-readable JSON during development.
- ProtoBuf output is binary and needs a shared `.proto` schema; the page's example uses `protoexample.Test` from `github.com/gin-gonic/gin/testdata/protoexample` with `Label` and `Reps` fields.

## When to pick which
JSON for REST and browsers, XML for legacy or SOAP-style integrations, YAML for config-oriented tools (Kubernetes, CI/CD), ProtoBuf for compact high-performance service-to-service traffic.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: rendering/index.md and rendering/rendering.md. Confirmed: the five renderer calls and their content types, the query-parameter format switch, gin.H, the json tag rename, IndentedJSON, the protoexample.Test example with Label and Reps, and the when-to-use guidance. Trimmed nothing.

Method: documentation only; no commands were run.
