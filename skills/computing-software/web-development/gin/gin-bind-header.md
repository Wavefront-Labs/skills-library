---
id: computing-software.web-development.gin.gin-bind-header
name: gin-bind-header
category: computing-software
field: web-development
product: gin
tags: [gin, shouldbindheader, header-tag, request-headers, binding, required]
level: intro
status: docs-checked
description: "Bind HTTP request headers into a Gin struct with ShouldBindHeader and header tags, optionally requiring them with binding:required."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-header.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind request headers with ShouldBindHeader

Goal: read headers such as rate limits, tokens or custom domain headers straight into a struct.

```go
type testHeader struct {
  Rate   int    `header:"Rate"`
  Domain string `header:"Domain"`
}

func main() {
  r := gin.Default()
  r.GET("/", func(c *gin.Context) {
    h := testHeader{}
    if err := c.ShouldBindHeader(&h); err != nil {
      c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
      return
    }
    c.JSON(http.StatusOK, gin.H{"Rate": h.Rate, "Domain": h.Domain})
  })
  r.Run(":8080")
}
```

Test:

```sh
curl -H "Rate:300" -H "Domain:music" http://localhost:8080/
# {"Domain":"music","Rate":300}

curl http://localhost:8080/
# {"Domain":"","Rate":0}
```

Missing headers leave zero values.

## Reject requests missing a header
Add `binding:"required"`:

```go
type authHeader struct {
  Token string `header:"Authorization" binding:"required"`
}
```

## Gotcha
Header names are case-insensitive per HTTP, and the `header` tag value is matched case-insensitively, so `header:"Rate"` matches `Rate`, `rate` or `RATE`.

## Related
The handler above answers 400 itself with the error text. For the general ShouldBind behaviour see gin-bind-query-or-post. Headers are a good source for metadata such as API rate limits, authentication tokens or custom domain headers, as the page describes.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind header (ShouldBindHeader, header tag, case-insensitive match, binding:required tip).
Removed or corrected: unconfirmed claim that ShouldBindHeader returns rather than aborts; reference to a nonexistent skill.

Method: documentation only; no commands were run.
