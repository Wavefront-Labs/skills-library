---
id: computing-software.web-development.gin.gin-embed-and-multitemplate
name: gin-embed-and-multitemplate
category: computing-software
field: web-development
product: gin
tags: [gin, go-embed, embed-fs, parsefs, sethtmltemplate, multitemplate, htmlrender, single-binary]
level: practitioner
status: docs-checked
description: "Embed HTML templates into a Gin binary with go:embed and template.ParseFS, or use gin-contrib/multitemplate for several template sets."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/bind-single-binary-with-template.md
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/rendering/multiple-template.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin: embed templates and use multiple template sets

## Single binary with go:embed (recommended)
Since Go 1.16 the standard library can embed files; no third-party dependency is needed.

```go
//go:embed templates/*
var templateFS embed.FS

func main() {
  router := gin.Default()

  t := template.Must(template.ParseFS(templateFS, "templates/*.tmpl"))
  router.SetHTMLTemplate(t)

  router.GET("/", func(c *gin.Context) {
    c.HTML(http.StatusOK, "index.tmpl", nil)
  })
  router.Run(":8080")
}
```

Imports used: `embed`, `html/template`, `net/http`, and Gin.

A third-party alternative is go-assets (github.com/jessevdk/go-assets): load the generated `Assets.Files` into a `template.Template` in a `loadTemplate()` helper, call `router.SetHTMLTemplate(t)`, and render with names like `/html/index.tmpl`. See the `assets-in-binary/example01` directory of github.com/gin-gonic/examples for a full example.

## Multiple template sets
By default Gin allows only one `html.Template`. For features like block templates use github.com/gin-contrib/multitemplate:

```go
func createMyRender() multitemplate.Renderer {
  r := multitemplate.NewRenderer()
  r.AddFromFiles("index", "templates/base.html", "templates/index.html")
  r.AddFromFiles("article", "templates/base.html", "templates/article.html")
  return r
}

router := gin.Default()
router.HTMLRender = createMyRender()
router.GET("/", func(c *gin.Context) {
  c.HTML(200, "index", gin.H{"title": "Home"})
})
```

## Notes
`router.HTMLRender = createMyRender()` sets the renderer; the names passed to `c.HTML` ("index", "article") are the names given to `AddFromFiles`. Each entry lists a shared `templates/base.html` plus a page-specific file. In the embed example, `c.HTML(http.StatusOK, "index.tmpl", nil)` passes nil as data.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Build a single binary with templates and Multitemplate (go:embed, ParseFS, SetHTMLTemplate, go-assets, multitemplate AddFromFiles, HTMLRender).
Removed or corrected: fixed broken source URL paths; dropped unconfirmed "replaces the default renderer" wording.

Method: documentation only; no commands were run.
