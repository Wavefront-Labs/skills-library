---
id: computing-software.software-engineering.go.html-template-and-text-template
name: html-template-and-text-template
category: computing-software
field: software-engineering
product: go
tags: [go, golang, html-template, text-template, server-side-rendering, xss, contextual-escaping, go-embed, go-templates-embed, go-template-funcs]
level: practitioner
status: verified
description: "Render pages with Go's html/template (contextual auto-escaping, layouts, blocks, FuncMap, embed) and text/template for config and code, avoiding XSS escapes."
sources: ["https://pkg.go.dev/html/template", "https://pkg.go.dev/text/template", "https://pkg.go.dev/embed"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# html/template and text/template

**Goal:** server-rendered HTML that is safe against XSS by construction, and plain-text generation
(configs, emails, code) with the same template language.

## Choose the package
- `html/template` for anything a browser renders: it escapes values according to context (HTML
  text, attribute, URL, JS, CSS).
- `text/template` for non-HTML output only. Using it for HTML is an XSS bug.
Both share syntax: `{{.Field}}`, `{{if}}`, `{{range}}`, `{{with}}`, `{{template "name" .}}`,
`{{block "name" .}}default{{end}}`, pipelines `{{.Name | printf "%q"}}`, `{{- trim -}}`.

## Layouts with embed
```go
//go:embed templates
var tmplFS embed.FS   // embeds the whole directory; 'templates/*.html' alone would miss templates/partials/

var base = template.Must(template.New("").Funcs(funcs).ParseFS(tmplFS, "templates/layout.html", "templates/partials/*.html"))

func page(name string) *template.Template {
    t := template.Must(base.Clone())                // each page gets its own copy
    return template.Must(t.ParseFS(tmplFS, "templates/"+name))
}
```
layout.html: `<main>{{block "content" .}}{{end}}</main>`; page file: `{{define "content"}}...{{end}}`.
Parse at startup, not per request; `template.Must` panics early on syntax errors.
Pages that each `define "content"` must be parsed into separate clones, otherwise the last
definition wins for all pages.

## Executing
```go
var buf bytes.Buffer
if err := tpl.ExecuteTemplate(&buf, "layout.html", data); err != nil {
    http.Error(w, "render error", 500); return
}
buf.WriteTo(w)
```
Render into a buffer first so a mid-template error does not send a half page with a 200 status.

## Escaping rules to know
- `<a href="{{.URL}}">` - unsafe schemes like `javascript:` are replaced with `#ZgotmplZ`.
- `<script>var u = {{.User}};</script>` - values are JSON-encoded safely.
- `template.HTML`, `template.URL`, `template.JS` mark content as trusted and bypass escaping.
  Only use them for content you generated or sanitised (e.g. bluemonday output for user markdown).
- Seeing `ZgotmplZ` in output means a value was rejected for its context: fix the data, do not cast
  to a trusted type.

## FuncMap
```go
funcs := template.FuncMap{
    "upper": strings.ToUpper,
    "date":  func(t time.Time) string { return t.Format("2 Jan 2006") },
}
```
Register before parsing (parsing a template that uses an unregistered function returns an error). Functions may return `(value, error)`; a non-nil error aborts execution, but whatever was already written stays in the writer (render into a buffer).
Keep logic in Go, not templates.

## text/template uses
Kubernetes-style config generation, emails, code generation (`go generate` + `go/format`).
`Option("missingkey=error")` makes missing map keys fail instead of printing `<no value>`.

## Verify
- [ ] Rendering `<script>alert(1)</script>` as user data shows escaped text.
- [ ] No `template.HTML(` conversions of user-controlled data (code search).
- [ ] Template parse errors fail at startup, not on first request.

## Checked
2026-10-21 on Go 1.27.3 (Windows), scratch module with embedded templates: the layout/clone pattern rendered two pages; `//go:embed templates/*.html` does NOT include `templates/partials/*.html` (`pattern matches no files` panic), so the skill's embed line was fixed to embed the directory; a shared template with both pages parsed into it rendered page B's content for the layout (last define wins); `javascript:` in href became `#ZgotmplZ`; a map value in a script was emitted as JSON with `\u003c` escapes; `template.HTML` bypassed escaping and a plain string did not; a FuncMap function returning an error aborted `Execute` after already writing `before ` into the writer (hence the buffer); a function used before `Funcs` registration makes `Parse` return an error; text/template printed `<no value>` for a missing map key and `Option("missingkey=error")` returned `map has no entry for key`; `{{.Name | printf "%q"}}` output is HTML-escaped in html/template (`&#34;n&#34;`).
