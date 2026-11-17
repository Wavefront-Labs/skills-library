---
id: computing-software.web-development.gin.gin-should-bind-body-with
name: gin-should-bind-body-with
category: computing-software
field: web-development
product: gin
tags: [gin, shouldbindbodywith, request-body, binding-json, io-readcloser, multiple-binds, binding]
level: practitioner
status: docs-checked
description: "Try several struct shapes against one Gin request body using ShouldBindBodyWith, which caches the body in the context instead of consuming it."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-body-into-different-structs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind the body into different structs with ShouldBindBodyWith

Goal: attempt to bind one request body against several struct types.

Methods like `c.ShouldBind` consume `c.Request.Body` (an `io.ReadCloser`), which cannot be read twice. `c.ShouldBindBodyWith` reads the body once, stores it in the context, and lets later calls reuse it.

```go
type formA struct {
  Foo string `json:"foo" xml:"foo" binding:"required"`
}

type formB struct {
  Bar string `json:"bar" xml:"bar" binding:"required"`
}

router.POST("/bind", func(c *gin.Context) {
  objA := formA{}
  objB := formB{}
  // This reads c.Request.Body and stores the result into the context.
  if errA := c.ShouldBindBodyWith(&objA, binding.JSON); errA == nil {
    c.JSON(http.StatusOK, gin.H{"message": "matched formA", "foo": objA.Foo})
    return
  }
  // At this time, it reuses body stored in the context.
  if errB := c.ShouldBindBodyWith(&objB, binding.JSON); errB == nil {
    c.JSON(http.StatusOK, gin.H{"message": "matched formB", "bar": objB.Bar})
    return
  }
  c.JSON(http.StatusBadRequest, gin.H{"error": "request body did not match any known format"})
})
```

Test:

```sh
curl -X POST http://localhost:8080/bind -H "Content-Type: application/json" -d '{"foo":"hello"}'
# {"foo":"hello","message":"matched formA"}
curl -X POST http://localhost:8080/bind -H "Content-Type: application/json" -d '{"bar":"world"}'
# {"bar":"world","message":"matched formB"}
```

## Gotchas
- Caching the body has a slight performance cost; use it only when you need to bind more than once.
- Formats that do not read the body (`Query`, `Form`, `FormPost`, `FormMultipart`) can be bound repeatedly with `c.ShouldBind()` without issue.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: binding/bind-body-into-different-structs.md. Confirmed: ShouldBind consumes the io.ReadCloser body, ShouldBindBodyWith caches it in the context, the formA/formB example and outputs, the slight performance cost, and that Query, Form, FormPost and FormMultipart can be bound repeatedly. Trimmed nothing.

Method: documentation only; no commands were run.
