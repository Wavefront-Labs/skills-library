---
id: computing-software.web-development.gin.gin-api-error-middleware
name: gin-api-error-middleware
category: computing-software
field: web-development
product: gin
tags: [gin, c-error, c-errors, errors-as, error-handler, custom-error-type, c-next, api-design]
level: advanced
status: docs-checked
description: "Centralise Gin API errors with a custom AppError type, c.Error in handlers and an ErrorHandler middleware that renders c.Errors.Last()."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/routing/api-design.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin structured API errors via middleware

Goal: handlers report errors with `c.Error(...)`; one middleware turns them into consistent JSON.

Define an error type carrying status and code (the status is hidden from JSON with `json:"-"`):

```go
type AppError struct {
  Status  int    `json:"-"`
  Code    string `json:"code"`
  Message string `json:"message"`
}

func (e *AppError) Error() string { return e.Message }

var (
  ErrNotFound     = &AppError{Status: 404, Code: "NOT_FOUND", Message: "resource not found"}
  ErrUnauthorized = &AppError{Status: 401, Code: "UNAUTHORIZED", Message: "authentication required"}
  ErrBadRequest   = &AppError{Status: 400, Code: "BAD_REQUEST", Message: "invalid request"}
)
```

Middleware: call `c.Next()` first, then inspect `c.Errors`:

```go
func ErrorHandler() gin.HandlerFunc {
  return func(c *gin.Context) {
    c.Next()
    if len(c.Errors) == 0 {
      return
    }
    err := c.Errors.Last().Err
    var appErr *AppError
    if errors.As(err, &appErr) {
      c.JSON(appErr.Status, gin.H{
        "success": false,
        "error":   gin.H{"code": appErr.Code, "message": appErr.Message},
      })
    } else {
      c.JSON(http.StatusInternalServerError, gin.H{
        "success": false,
        "error":   gin.H{"code": "INTERNAL", "message": "an unexpected error occurred"},
      })
    }
  }
}
```

Use it:

```go
r := gin.Default()
r.Use(ErrorHandler())
r.GET("/api/items/:id", func(c *gin.Context) {
  if c.Param("id") == "0" {
    _ = c.Error(ErrNotFound)
    return
  }
  c.JSON(http.StatusOK, gin.H{"success": true, "data": gin.H{"id": c.Param("id")}})
})
```

Unrecognised errors become a 500 with code `INTERNAL`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: API Design Patterns (custom error types, ErrorHandler).
Removed or corrected: broken source URL path (website/ prefix).

Method: documentation only; no commands were run.
