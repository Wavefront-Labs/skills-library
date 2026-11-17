---
id: computing-software.web-development.gin.gin-bind-vs-shouldbind
name: gin-bind-vs-shouldbind
category: computing-software
field: web-development
product: gin
tags: [gin, binding, shouldbind, bind, mustbindwith, shouldbindwith, validation, required]
level: practitioner
status: docs-checked
description: "Choose between Gin Bind (auto 400 abort) and ShouldBind (returns error) families, and use binding:required or binding:- tags with go-playground validator."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/binding-and-validation.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin Bind vs ShouldBind and the required tag

Goal: bind a request body into a struct and decide who handles the error.

Gin binds JSON, XML, YAML, TOML and form values, plus query strings, URI params and headers. Set the matching tag on every field (`json`, `xml`, `yaml`, `form`, `uri`, `header`). Validation rules go in `binding` and use go-playground/validator v10 syntax.

| Family | Methods | On error |
|---|---|---|
| Must bind | `Bind`, `BindJSON`, `BindXML`, `BindQuery`, `BindYAML` (use `MustBindWith`) | calls `c.AbortWithError(400, err).SetType(ErrorTypeBind)` |
| Should bind | `ShouldBind`, `ShouldBindJSON`, `ShouldBindXML`, `ShouldBindQuery`, `ShouldBindYAML` (use `ShouldBindWith`) | returns the error; you respond |

The docs recommend `ShouldBind` in most cases for control over the error response. `Bind`/`ShouldBind` infer the binder from the Content-Type header; use `MustBindWith` or `ShouldBindWith` when you know the format.

```go
type Login struct {
  User     string `form:"user" json:"user" xml:"user"  binding:"required"`
  Password string `form:"password" json:"password" xml:"password" binding:"required"`
}

router.POST("/loginJSON", func(c *gin.Context) {
  var json Login
  if err := c.ShouldBindJSON(&json); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
})
```

Posting `{ "user": "manu" }` returns 400 with `{"error":"Key: 'Login.Password' Error:Field validation for 'Password' failed on the 'required' tag"}`.

## Gotchas
- A `binding:"required"` field with an empty value produces an error.
- For nested structs, the inner fields also need `binding:"required"`.
- Use `binding:"-"` on a field to skip validation for it.
- After a Must-bind failure the 400 is already written (Content-Type `text/plain; charset=utf-8`); setting another status afterwards logs a warning about headers already written.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Model binding and validation and Binding index (Must bind vs Should bind, AbortWithError 400, text/plain, nested required, binding:"-").
Removed or corrected: nothing.

Method: documentation only; no commands were run.
