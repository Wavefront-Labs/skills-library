---
id: computing-software.web-development.gin.gin-collection-format
name: gin-collection-format
category: computing-software
field: web-development
product: gin
tags: [gin, collection-format, csv, ssv, tsv, pipes, multi, query-string, binding]
level: practitioner
status: docs-checked
description: "Control how Gin splits list query values into slices with collection_format: multi, csv, ssv, tsv or pipes (v1.11+)."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/collection-format-for-arrays.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# collection_format for slice and array fields

Goal: choose how a list value in a query or form is split into a Go slice. The formats below are listed as supported from v1.11.

| Format | Meaning |
|---|---|
| `multi` (default) | repeated keys or comma-separated values |
| `csv` | comma-separated |
| `ssv` | space-separated |
| `tsv` | tab-separated |
| `pipes` | pipe-separated |

```go
type Filters struct {
  Tags   []string `form:"tags" collection_format:"csv"`     // /search?tags=go,web,api
  Labels []string `form:"labels" collection_format:"multi"` // /search?labels=bug&labels=helpwanted
  IdsSSV []int    `form:"ids_ssv" collection_format:"ssv"`  // /search?ids_ssv=1 2 3
  IdsTSV []int    `form:"ids_tsv" collection_format:"tsv"`  // /search?ids_tsv=1\t2\t3
  Levels []int    `form:"levels" collection_format:"pipes"` // /search?levels=1|2|3
}

r.GET("/search", func(c *gin.Context) {
  var f Filters
  if err := c.ShouldBind(&f); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  c.JSON(http.StatusOK, f)
})
```

## Defaults for collections (v1.11+)
Use `default` in the `form` tag to set fallback values. For `multi` and `csv`, separate default values with semicolons: `default=1;2;3`. For `ssv`, `tsv` and `pipes`, use the natural separator in the default.

## Note
`multi` is the default format when no `collection_format` tag is given. The page cross-references its "Bind default values for form fields" example for more on defaults.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Collection format for arrays (multi, csv, ssv, tsv, pipes; v1.11+; defaults with semicolons).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
