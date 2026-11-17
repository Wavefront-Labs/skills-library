---
id: computing-software.web-development.gin.gin-querymap-postformmap
name: gin-querymap-postformmap
category: computing-software
field: web-development
product: gin
tags: [gin, c-querymap, c-postformmap, bracket-notation, map-parameters, query-string, post-form]
level: practitioner
status: docs-checked
description: "Parse bracket-notation parameters like ids[a]=1234 into a map in Gin using c.QueryMap and c.PostFormMap."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/map-as-querystring-or-postform.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin QueryMap and PostFormMap

Goal: receive key-value pairs whose keys are not known in advance (dynamic filters, user-defined metadata).

- `c.QueryMap("key")` parses `key[subkey]=value` pairs from the URL query string into a `map[string]string`.
- `c.PostFormMap("key")` does the same for pairs in the request body.

```go
router.POST("/post", func(c *gin.Context) {
  ids := c.QueryMap("ids")
  names := c.PostFormMap("names")

  fmt.Printf("ids: %v; names: %v\n", ids, names)
  c.JSON(http.StatusOK, gin.H{
    "ids":   ids,
    "names": names,
  })
})
router.Run(":8080")
```

Test:

```sh
curl -X POST "http://localhost:8080/post?ids[a]=1234&ids[b]=hello" \
  -d "names[first]=thinkerou&names[second]=tianou"
# Output: {"ids":{"a":"1234","b":"hello"},"names":{"first":"thinkerou","second":"tianou"}}
```

## Gotcha
Gin takes the text inside the brackets as the map key. Only single-level brackets are supported: `ids[a][b]=value` is not parsed as a nested map.

## When to use which
Use `c.QueryMap("ids")` for pairs in the URL such as `?ids[a]=1234&ids[b]=hello`, and `c.PostFormMap("names")` for pairs sent in the request body such as `names[first]=thinkerou`. Both calls can sit in the same handler, as in the POST example above, and each returns its own map. Related single-value readers are `c.Query`, `c.DefaultQuery`, `c.PostForm` and `c.DefaultPostForm`, covered in the query and form parameters skill.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: routing/map-as-querystring-or-postform.md. Confirmed: QueryMap and PostFormMap return map[string]string from key[subkey]=value pairs, the example output, and that only single-level brackets are parsed. Trimmed nothing. Fixed the source (bogus website/ segment).

Method: documentation only; no commands were run.
