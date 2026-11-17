---
id: computing-software.web-development.gin.gin-bind-custom-struct-tag
name: gin-bind-custom-struct-tag
category: computing-software
field: web-development
product: gin
tags: [gin, custom-binding, mapformwithtag, mustbindwith, struct-tag, binding-interface, form]
level: advanced
status: docs-checked
description: "Bind form data in Gin using a non-form struct tag (such as url) for types you cannot edit, via a custom binding.Binding and binding.MapFormWithTag."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-form-data-custom-struct-tag.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind form data with a custom struct tag

Goal: fill a struct whose fields carry a tag other than `form` (for example `url` on a third-party type you cannot modify).

Implement `binding.Binding`: a `Name() string` method and a `Bind(*http.Request, any) error` method. Inside `Bind`, call `binding.MapFormWithTag` with your tag name, then validate.

```go
const (
  customerTag   = "url"
  defaultMemory = 32 << 20
)

type customerBinding struct{}

func (customerBinding) Name() string { return "form" }

func (customerBinding) Bind(req *http.Request, obj any) error {
  if err := req.ParseForm(); err != nil {
    return err
  }
  if err := req.ParseMultipartForm(defaultMemory); err != nil {
    if err != http.ErrNotMultipart {
      return err
    }
  }
  if err := binding.MapFormWithTag(obj, req.Form, customerTag); err != nil {
    return err
  }
  return validate(obj)
}

func validate(obj any) error {
  if binding.Validator == nil {
    return nil
  }
  return binding.Validator.ValidateStruct(obj)
}

// FormA is an external type that we can't modify its tag
type FormA struct {
  FieldA string `url:"field_a"`
}

router.GET("/list", func(c *gin.Context) {
  var urlBinding = customerBinding{}
  var opt FormA
  if err := c.MustBindWith(&opt, urlBinding); err != nil {
    return
  }
  c.JSON(http.StatusOK, gin.H{"field_a": opt.FieldA})
})
```

Test:

```sh
curl "http://localhost:8080/list?field_a=hello"   # {"field_a":"hello"}
curl "http://localhost:8080/list"                 # {"field_a":""}
```

## Note
`binding.MapFormWithTag` does the mapping of form values to struct fields using your tag; the custom binding is then passed to `c.MustBindWith`.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind form-data with custom struct tag (binding.Binding, MapFormWithTag, MustBindWith, curl results).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
