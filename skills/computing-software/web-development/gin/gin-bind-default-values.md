---
id: computing-software.web-development.gin.gin-bind-default-values
name: gin-bind-default-values
category: computing-software
field: web-development
product: gin
tags: [gin, default, form-tag, collection-format, binding, shouldbind, v1-11]
level: practitioner
status: docs-checked
description: "Give Gin form fields fallback values with the default option in the form tag, including slices and arrays with collection_format separators."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-default-values.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Default values for form fields

Goal: let a field fall back to a value when the client sends nothing. Scalars work with `default`; collection defaults were added in Gin v1.11.

Rules:
- Put the default right after the form key: `form:"name,default=William"`.
- For collections set `collection_format:"multi|csv|ssv|tsv|pipes"`.
- For `multi` and `csv`, separate default values with semicolons (`default=1;2;3`); Gin converts them to commas internally.
- For `ssv` (space), `tsv` (tab) and `pipes` (|), use the natural separator.

```go
type Person struct {
  Name      string    `form:"name,default=William"`
  Age       int       `form:"age,default=10"`
  Friends   []string  `form:"friends,default=Will;Bill"`
  Addresses [2]string `form:"addresses,default=foo bar" collection_format:"ssv"`
  LapTimes  []int     `form:"lap_times,default=1;2;3" collection_format:"csv"`
}

r.POST("/person", func(c *gin.Context) {
  var req Person
  if err := c.ShouldBind(&req); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  c.JSON(http.StatusOK, req)
})
```

`curl -X POST http://localhost:8080/person` (no body) responds with the defaults: Name "William", Age 10, Friends ["Will","Bill"], Addresses ["foo","bar"], LapTimes [1,2,3].

## Gotchas
- Commas separate options in Go struct tags, so avoid commas inside default values.
- For `multi` and `csv`, do not put semicolons inside an individual default.
- An invalid `collection_format` value results in a binding error.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind default values (default option, collection_format, semicolon rule, v1.11).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
