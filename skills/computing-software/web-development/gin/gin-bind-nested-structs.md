---
id: computing-software.web-development.gin.gin-bind-nested-structs
name: gin-bind-nested-structs
category: computing-software
field: web-development
product: gin
tags: [gin, nested-struct, struct-pointer, anonymous-struct, form-tag, bind, query-string]
level: intro
status: docs-checked
description: "Bind query or form data into nested, pointer and anonymous inline structs in Gin using plain form tags with flat parameter names."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-form-data-request-with-custom-struct.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/binding-and-validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind into nested structs

Goal: organise complex forms into reusable sub-structs. Gin walks the struct hierarchy and maps each `form` tag to the matching query parameter or form field; nested value structs, pointer fields and anonymous inline structs all work.

```go
type StructA struct {
  FieldA string `form:"field_a"`
}

type StructB struct {
  NestedStruct StructA
  FieldB       string `form:"field_b"`
}

type StructC struct {
  NestedStructPointer *StructA
  FieldC              string `form:"field_c"`
}

type StructD struct {
  NestedAnonyStruct struct {
    FieldX string `form:"field_x"`
  }
  FieldD string `form:"field_d"`
}

router.GET("/getb", func(c *gin.Context) {
  var b StructB
  c.Bind(&b)
  c.JSON(http.StatusOK, gin.H{"a": b.NestedStruct, "b": b.FieldB})
})
```

The `/getc` and `/getd` handlers are the same shape with `StructC` and `StructD`.

Test:

```sh
curl "http://localhost:8080/getb?field_a=hello&field_b=world"
# {"a":{"FieldA":"hello"},"b":"world"}

curl "http://localhost:8080/getc?field_a=hello&field_c=world"
# {"a":{"FieldA":"hello"},"c":"world"}

curl "http://localhost:8080/getd?field_x=hello&field_d=world"
# {"d":"world","x":{"FieldX":"hello"}}
```

## Gotcha
All three patterns bind from the same flat parameter names. Gin does not require any prefix or nesting convention such as `nested.field_a`. For a pointer field, Gin allocates the pointer automatically.

## Related
These handlers use `c.Bind`, the Must-bind variant, which infers the binder from the request. For custom tags on types you cannot modify, see gin-bind-custom-struct-tag. The page's purpose is organising complex forms into reusable sub-structures instead of one flat struct with many fields.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind form-data request with custom struct and Model binding and validation (nested, pointer, anonymous structs; Bind infers binder).
Removed or corrected: nothing (added the second source).

Method: documentation only; no commands were run.
