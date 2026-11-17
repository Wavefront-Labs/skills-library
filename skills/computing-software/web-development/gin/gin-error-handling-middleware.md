---
id: computing-software.web-development.gin.gin-error-handling-middleware
name: gin-error-handling-middleware
category: computing-software
field: web-development
product: gin
tags: [gin, middleware, error-handling, c-error, c-errors, json-error, centralized-errors]
level: practitioner
status: docs-checked
description: "Centralize Gin error responses: handlers call c.Error(err), and a middleware checks c.Errors after c.Next() and returns a consistent JSON error body."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/error-handling-middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Error handling middleware

Goal: stop repeating error-response code in every handler. A middleware runs after each request, looks at errors added with `c.Error(err)`, and sends one structured JSON response.

```go
// ErrorHandler captures errors and returns a consistent JSON error response
func ErrorHandler() gin.HandlerFunc {
  return func(c *gin.Context) {
    c.Next() // Process the request first

    // Check if any errors were added to the context
    if len(c.Errors) > 0 {
      err := c.Errors.Last().Err

      c.JSON(http.StatusInternalServerError, gin.H{
        "success": false,
        "message": err.Error(),
      })
    }
  }
}

func main() {
  r := gin.Default()
  r.Use(ErrorHandler())

  r.GET("/ok", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{
      "success": true,
      "message": "Everything is fine!",
    })
  })

  r.GET("/error", func(c *gin.Context) {
    c.Error(errors.New("something went wrong"))
  })

  r.Run(":8080")
}
```

## Test it
```sh
curl http://localhost:8080/ok
# Output: {"message":"Everything is fine!","success":true}

curl http://localhost:8080/error
# Output: {"message":"something went wrong","success":false}
```

## Notes from the docs
- The check must come after `c.Next()` so handlers have already run and added their errors.
- The example reads the error with `c.Errors.Last().Err`.
- Tip from the page: extend the pattern to map specific error types to different HTTP status codes, or log errors to an external service before responding. The example always uses 500.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Error handling middleware (ErrorHandler after c.Next(), c.Errors, outputs, extension tip).
Removed or corrected: unconfirmed claim that Last() is the most recent error.

Method: documentation only; no commands were run.
