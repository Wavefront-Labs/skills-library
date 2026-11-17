---
id: computing-software.web-development.gin.gin-bind-html-checkboxes
name: gin-bind-html-checkboxes
category: computing-software
field: web-development
product: gin
tags: [gin, html-checkbox, form-tag, slice, shouldbind, loadhtmlglob, binding]
level: intro
status: docs-checked
description: "Bind multiple HTML checkbox values with the same name into a Gin []string field using a form tag that matches the name attribute, such as colors[]."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/bind-html-checkbox.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/binding/multipart-urlencoded-binding.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bind HTML checkboxes into a slice

Goal: collect all checked boxes sharing one `name` into a `[]string`.

```go
type myForm struct {
  Colors []string `form:"colors[]"`
}

router := gin.Default()
router.LoadHTMLGlob("templates/*")

router.GET("/", func(c *gin.Context) {
  c.HTML(http.StatusOK, "form.html", nil)
})

router.POST("/", func(c *gin.Context) {
  var fakeForm myForm
  if err := c.ShouldBind(&fakeForm); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  c.JSON(http.StatusOK, gin.H{"color": fakeForm.Colors})
})
```

`templates/form.html`:

```html
<form action="/" method="POST">
    <input type="checkbox" name="colors[]" value="red" id="red">
    <input type="checkbox" name="colors[]" value="green" id="green">
    <input type="checkbox" name="colors[]" value="blue" id="blue">
    <input type="submit">
</form>
```

Test:

```sh
curl -X POST http://localhost:8080/ -d "colors[]=red&colors[]=green&colors[]=blue"
# {"color":["red","green","blue"]}
curl -X POST http://localhost:8080/
# {"color":[]}
```

## Gotcha
The `[]` suffix is an HTML convention, not a Go requirement. The struct tag must match the HTML `name` attribute exactly: with `name="colors"` use `form:"colors"`.

## When to use
This suits forms where users select one or more options, such as color pickers, permission selectors or multi-select filters. With no boxes checked the slice is empty. The handler uses ShouldBind, so it picks the form binder from the Content-Type; for the general form case see gin-bind-multipart-urlencoded.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Bind html checkboxes and Multipart/Urlencoded binding (colors[] tag, empty slice, ShouldBind by Content-Type).
Removed or corrected: wording about the page linking elsewhere.

Method: documentation only; no commands were run.
