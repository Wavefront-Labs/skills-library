---
id: computing-software.web-development.gin.gin-asciijson-purejson
name: gin-asciijson-purejson
category: computing-software
field: web-development
product: gin
tags: [gin, asciijson, purejson, c-asciijson, c-purejson, abortwithstatuspurejson, html-escaping]
level: intro
status: docs-checked
description: "Choose between Gin c.JSON, c.AsciiJSON and c.PureJSON to control escaping of non-ASCII and HTML characters in JSON output."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/ascii-json.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/pure-json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin AsciiJSON vs PureJSON

Goal: control how special characters are escaped in JSON responses.

## AsciiJSON
`c.AsciiJSON` escapes every non-ASCII character to a `\uXXXX` sequence and also escapes HTML-special characters like `<` and `>`, so the body is 7-bit ASCII only. Use it only when consumers require ASCII-safe output; plain `c.JSON()` is enough for most APIs.

```go
router.GET("/someJSON", func(c *gin.Context) {
  data := map[string]interface{}{
    "lang": "GO语言",
    "tag":  "<br>",
  }
  // will output : {"lang":"GO\u8bed\u8a00","tag":"\u003cbr\u003e"}
  c.AsciiJSON(http.StatusOK, data)
})
```

## PureJSON
Standard JSON (`json.Marshal`) turns `<` into `\u003c`. `c.PureJSON` uses `json.Encoder` with `SetEscapeHTML(false)`, so `<`, `>` and `&` stay literal. Use it for pure APIs; use `c.JSON` when the response might be embedded in an HTML page.

```go
c.JSON(http.StatusOK, gin.H{"html": "<b>Hello, world!</b>"})
// {"html":"\u003cb\u003eHello, world!\u003c/b\u003e"}
c.PureJSON(http.StatusOK, gin.H{"html": "<b>Hello, world!</b>"})
// {"html":"<b>Hello, world!</b>"}
```

Tip: `c.AbortWithStatusPureJSON` (v1.11+) returns unescaped JSON while aborting the middleware chain, handy in auth or validation middleware.

## Choosing
- Consumers need strict ASCII (legacy transports, some logging systems), or you want `<`, `>` and `&` escaped when JSON is embedded in HTML: `c.AsciiJSON`. In the example, the characters of `语言` become `\u8bed\u8a00` and `<br>` becomes `\u003cbr\u003e`.
- Pure API clients expect literal characters: `c.PureJSON`.
- Everything else: `c.JSON`, which outputs valid UTF-8.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: AsciiJSON and PureJSON pages (escaping behaviour, SetEscapeHTML(false), AbortWithStatusPureJSON v1.11+).
Removed or corrected: restored lost \uXXXX escapes in outputs and prose; fixed source URL paths.

Method: documentation only; no commands were run.
