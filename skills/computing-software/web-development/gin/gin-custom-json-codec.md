---
id: computing-software.web-development.gin.gin-custom-json-codec
name: gin-custom-json-codec
category: computing-software
field: web-development
product: gin
tags: [gin, json, json-api, json-core, jsoniter, codec, marshal, unmarshal]
level: advanced
status: docs-checked
description: "Swap Gin's JSON library at runtime by implementing json.Core and assigning json.API from github.com/gin-gonic/gin/codec/json, shown with jsoniter."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/custom-json-codec.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin custom JSON codec at runtime

Goal: replace Gin's JSON serialization without compile tags.

Steps:
1. Define a struct that implements the `json.Core` interface (package `github.com/gin-gonic/gin/codec/json`).
2. Before the engine starts, assign an instance to `json.API`.

```go
import (
  "io"

  "github.com/gin-gonic/gin"
  "github.com/gin-gonic/gin/codec/json"
  jsoniter "github.com/json-iterator/go"
)

var customConfig = jsoniter.Config{
  EscapeHTML:             true,
  SortMapKeys:            true,
  ValidateJsonRawMessage: true,
}.Froze()

type customJsonApi struct{}

func (j customJsonApi) Marshal(v any) ([]byte, error) {
  return customConfig.Marshal(v)
}
func (j customJsonApi) Unmarshal(data []byte, v any) error {
  return customConfig.Unmarshal(data, v)
}
func (j customJsonApi) MarshalIndent(v any, prefix, indent string) ([]byte, error) {
  return customConfig.MarshalIndent(v, prefix, indent)
}
func (j customJsonApi) NewEncoder(writer io.Writer) json.Encoder {
  return customConfig.NewEncoder(writer)
}
func (j customJsonApi) NewDecoder(reader io.Reader) json.Decoder {
  return customConfig.NewDecoder(reader)
}

func main() {
  // Replace the default json api
  json.API = customJsonApi{}

  router := gin.Default()
  router.Run(":8080")
}
```

## Gotcha
The five methods shown (`Marshal`, `Unmarshal`, `MarshalIndent`, `NewEncoder`, `NewDecoder`) are what the page's implementation provides. Assign `json.API` before starting the engine.

## Checklist
- Import the codec package as `github.com/gin-gonic/gin/codec/json` and your chosen library (the page uses `github.com/json-iterator/go` aliased as `jsoniter`).
- Build the library config once (`jsoniter.Config{...}.Froze()` with `EscapeHTML`, `SortMapKeys`, `ValidateJsonRawMessage` set to true in the page's example).
- Assign `json.API = customJsonApi{}` first thing in `main`, before `gin.Default()` and `router.Run`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Custom JSON codec at runtime (json.Core, json.API, jsoniter config, five methods).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
