---
id: computing-software.web-development.gin.gin-html-templates
name: gin-html-templates
category: computing-software
field: web-development
product: gin
tags: [gin, html-rendering, loadhtmlglob, loadhtmlfiles, loadhtmlfs, c-html, sethtmltemplate, html-template]
level: intro
status: docs-checked
description: "Render HTML in Gin with LoadHTMLGlob, LoadHTMLFiles or LoadHTMLFS, including same-named templates in different directories."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/html-rendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin HTML templates

Goal: load templates and render them with `c.HTML`. Gin uses Go's `html/template`.

## Basic
```go
router := gin.Default()
router.LoadHTMLGlob("templates/*")
//router.LoadHTMLFiles("templates/template1.html", "templates/template2.html")
router.GET("/index", func(c *gin.Context) {
  c.HTML(http.StatusOK, "index.tmpl", gin.H{"title": "Main website"})
})
```

`templates/index.tmpl`:
```html
<html><h1>{{ .title }}</h1></html>
```

## Same file name in different directories
Load with `router.LoadHTMLGlob("templates/**/*")` and render with `c.HTML(http.StatusOK, "posts/index.tmpl", ...)`. Each file must wrap its content in a `define` block named by its relative path, otherwise Gin will not parse the templates properly:

```html
{{ define "posts/index.tmpl" }}
<html><h1>{{ .title }}</h1>
<p>Using posts/index.tmpl</p>
</html>
{{ end }}
```

## From an http.FileSystem (v1.11+)
```go
//go:embed templates
var tmplFS embed.FS

r := gin.Default()
sub, _ := fs.Sub(tmplFS, "templates")
r.LoadHTMLFS(http.FS(sub), "**/*.tmpl")
r.GET("/", func(c *gin.Context) {
  c.HTML(http.StatusOK, "index.tmpl", gin.H{"title": "From FS"})
})
```

## Custom renderer
Build your own template set and install it with `router.SetHTMLTemplate(template.Must(template.ParseFiles("file1", "file2")))`.

## Notes
- Use `LoadHTMLGlob()` or `LoadHTMLFiles()` to choose which files are loaded; for placeholder syntax see Go's `text/template` documentation.
- The template name passed to `c.HTML` is the file name (`index.tmpl`) for the flat glob `templates/*`, and the `define` name (`posts/index.tmpl`) for the `templates/**/*` layout.
- Routes in the nested example: `/posts/index` renders `posts/index.tmpl` with title "Posts", and `/users/index` renders `users/index.tmpl` with title "Users".

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: HTML rendering (LoadHTMLGlob, LoadHTMLFiles, LoadHTMLFS v1.11+, define blocks, SetHTMLTemplate).
Removed or corrected: fixed broken source URL path.

Method: documentation only; no commands were run.
