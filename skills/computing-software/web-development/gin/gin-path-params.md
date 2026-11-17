---
id: computing-software.web-development.gin.gin-path-params
name: gin-path-params
category: computing-software
field: web-development
product: gin
tags: [gin, c-param, path-parameters, wildcard, named-parameter, route-conflict, httprouter]
level: intro
status: docs-checked
description: "Capture dynamic URL segments in Gin with :name and *action routes and read them with c.Param, including wildcard slash behaviour."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/param-in-path.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin path parameters

Goal: capture parts of the URL path. Gin routing is built on httprouter, a radix tree matcher.

- `:name` matches one path segment. `/user/:name` matches `/user/john` but not `/user/` or `/user`.
- `*action` matches everything after the prefix, including slashes, and the captured value includes the leading `/`. `/user/:name/*action` matches `/user/john/send` and `/user/john/`.

Read values with `c.Param("name")`.

```go
router := gin.Default()

// matches /user/john, not /user/ or /user
router.GET("/user/:name", func(c *gin.Context) {
  name := c.Param("name")
  c.String(http.StatusOK, "Hello %s", name)
})

// matches /user/john/ and /user/john/send
// If no other routers match /user/john, it will redirect to /user/john/
router.GET("/user/:name/*action", func(c *gin.Context) {
  name := c.Param("name")
  action := c.Param("action")
  c.String(http.StatusOK, name+" is "+action)
})
router.Run(":8080")
```

```sh
curl http://localhost:8080/user/john        # Hello john
curl http://localhost:8080/user/john/send   # john is /send
curl http://localhost:8080/user/john/       # john is /
```

## Gotchas
- `c.Param("action")` returns `/send`, not `send`.
- Defining `/user/:name` and `/user/:name/*action` when they conflict at the same path depth makes Gin panic at startup on ambiguous routes.

## Notes
Routing in Gin is built on httprouter, which stores routes in a radix tree (compressed trie); the page says this makes matching fast with zero allocations per lookup.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: routing/param-in-path.md and routing/index.md. Confirmed: :name versus *action behaviour, leading slash in the wildcard value, the curl outputs, the startup panic on ambiguous routes, and httprouter radix tree with zero allocations per lookup. Trimmed nothing. Fixed both sources, which had a bogus website/ path segment and did not resolve.

Method: documentation only; no commands were run.
