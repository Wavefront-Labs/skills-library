---
id: computing-software.web-development.gin.gin-securejson-jsonp
name: gin-securejson-jsonp
category: computing-software
field: web-development
product: gin
tags: [gin, securejson, securejsonprefix, jsonp, c-jsonp, json-hijacking, callback]
level: intro
status: docs-checked
description: "Use Gin c.SecureJSON to prefix array responses against JSON hijacking and c.JSONP for callback-wrapped cross-domain responses."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/secure-json.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/jsonp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin SecureJSON and JSONP

Goal: serve legacy-browser-safe JSON arrays, or JSONP callbacks.

## SecureJSON
Protects against JSON hijacking in old browsers (mainly IE9 and earlier), where a hostile page could load a top-level JSON array through a `<script>` tag. When the data is an array, `c.SecureJSON` prepends an unparseable prefix, `while(1);` by default. API clients simply strip the prefix before parsing.

```go
// optional custom prefix
// router.SecureJsonPrefix(")]}',\n")

router.GET("/someJSON", func(c *gin.Context) {
  names := []string{"lena", "austin", "foo"}
  // Will output  :   while(1);["lena","austin","foo"]
  c.SecureJSON(http.StatusOK, names)
})
```

Modern browsers fixed the issue, so it matters mainly for legacy support or defence in depth.

## JSONP
`c.JSONP` looks for a `callback` query parameter. If present, the body becomes `callbackName({"foo":"bar"})` with `Content-Type: application/javascript`; otherwise it behaves like `c.JSON()`.

```go
router.GET("/JSONP", func(c *gin.Context) {
  data := map[string]interface{}{"foo": "bar"}
  c.JSONP(http.StatusOK, data)
})
```

```sh
curl "http://localhost:8080/JSONP?callback=handleData"  # handleData({"foo":"bar"});
curl "http://localhost:8080/JSONP"                      # {"foo":"bar"}
```

## Gotchas
- JSONP is legacy; prefer CORS for modern apps.
- Gin sanitizes the callback name, but still limit JSONP endpoints to non-sensitive read-only data because any page can load them via `<script>`.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: rendering/secure-json.md and rendering/jsonp.md. Confirmed: IE9-and-earlier hijacking scenario, default while(1); prefix, SecureJsonPrefix, modern browsers fixed, the callback query parameter, application/javascript content type, fallback to c.JSON, curl outputs, CORS advice and callback sanitisation caution. Trimmed nothing. Fixed both sources (bogus website/ segment).

Method: documentation only; no commands were run.
