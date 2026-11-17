---
id: computing-software.web-development.gin.gin-debug-print-route-func
name: gin-debug-print-route-func
category: computing-software
field: web-development
product: gin
tags: [gin, logging, debugprintroutefunc, gin-debug, routes, startup, custom-format]
level: practitioner
status: docs-checked
description: "Change how Gin prints registered routes at startup by assigning a function to gin.DebugPrintRouteFunc(httpMethod, absolutePath, handlerName, nuHandlers)."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/logging/define-format-for-the-log-of-routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Define the format of the route log

Goal: control the lines Gin prints for each registered route at startup.

In debug mode Gin prints all routes when it starts. The default format:

```
[GIN-debug] POST   /foo                      --> main.main.func1 (3 handlers)
[GIN-debug] GET    /bar                      --> main.main.func2 (3 handlers)
[GIN-debug] GET    /status                   --> main.main.func3 (3 handlers)
```

Assign a function to `gin.DebugPrintRouteFunc` to emit JSON, key-value pairs or whatever your logging pipeline expects:

```go
router := gin.Default()

gin.DebugPrintRouteFunc = func(httpMethod, absolutePath, handlerName string, nuHandlers int) {
  log.Printf("endpoint %v %v %v %v\n", httpMethod, absolutePath, handlerName, nuHandlers)
}

router.POST("/foo", func(c *gin.Context) {
  c.JSON(http.StatusOK, "foo")
})
router.GET("/bar", func(c *gin.Context) {
  c.JSON(http.StatusOK, "bar")
})
router.GET("/status", func(c *gin.Context) {
  c.JSON(http.StatusOK, "ok")
})

router.Run(":8080")
```

## Resulting output (from the docs)
Instead of the `[GIN-debug]` lines:

```
endpoint POST /foo main.main.func2 3
endpoint GET /bar main.main.func3 3
endpoint GET /status main.main.func4 3
```

## Gotchas
- The function signature is `func(httpMethod, absolutePath, handlerName string, nuHandlers int)`.
- Assign `gin.DebugPrintRouteFunc` before registering routes, as in the docs example, where it is set right after `gin.Default()` and before `router.POST`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Define format for the log of routes (DebugPrintRouteFunc signature, default and custom output).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
