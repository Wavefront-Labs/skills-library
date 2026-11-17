---
id: computing-software.web-development.gin.gin-route-groups-and-http-methods
name: gin-route-groups-and-http-methods
category: computing-software
field: web-development
product: gin
tags: [gin, router-group, grouping-routes, http-methods, api-versioning, nested-groups, group-use, router-run]
level: intro
status: docs-checked
description: "Register Gin routes for each HTTP verb and organise them with router.Group prefixes, group middleware and nested groups."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/http-method.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/grouping-routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin HTTP method routes and route groups

## Verbs
Each router method registers a route for one HTTP verb: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`.

```go
router := gin.Default()
router.GET("/someGet", getting)
router.POST("/somePost", posting)
router.PUT("/somePut", putting)
router.DELETE("/someDelete", deleting)
router.PATCH("/somePatch", patching)
router.HEAD("/someHead", head)
router.OPTIONS("/someOptions", options)

// By default it serves on :8080 unless a PORT environment variable was defined.
router.Run()
// router.Run(":3000") for a hard coded port
```

Test with `curl -X POST http://localhost:8080/somePost`; use `curl -I` for HEAD.

## Groups
Groups share a URL prefix, middleware, and keep related handlers together (for example `/v1` and `/v2`).

```go
v1 := router.Group("/v1")
v1.POST("/login", loginEndpoint)
v1.POST("/submit", submitEndpoint)

v2 := router.Group("/v2")
v2.POST("/login", loginEndpoint)
```

Middleware: pass it to `router.Group()` or call `Use()` on the group.

```go
private := router.Group("/api")
private.Use(AuthRequired())
{
  private.GET("/profile", getProfile)
}
```

Nest groups for deeper hierarchies; each level inherits its parent prefix:

```go
api := router.Group("/api")
v1 := api.Group("/v1")
users := v1.Group("/users")
users.GET("/:id", getUser) // /api/v1/users/:id
```

## Notes
- Typical REST use: GET retrieves, POST creates, PUT replaces, PATCH partially updates, DELETE removes, HEAD is GET without a body, OPTIONS describes communication options.
- The resulting nested routes above are `/api/v1/users/` and `/api/v1/users/:id`.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Pages read: routing/http-method.md and routing/grouping-routes.md. Confirmed: the seven verbs and their typical REST use, the PORT-or-:8080 default of Run(), group prefixes, Group()/Use() middleware, nested groups and the resulting paths. Trimmed nothing. Fixed both sources (bogus website/ segment).

Method: documentation only; no commands were run.
