---
id: computing-software.software-engineering.ktor.ktor-html-dsl
name: ktor-html-dsl
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, html, kotlinx-html, templates, dsl, server]
level: intro
status: docs-checked
description: "Respond with HTML from Ktor using the kotlinx.html DSL: respondHtml, respondHtmlPartial for HTMX fragments, and Template, Placeholder and respondHtmlTemplate layouts."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-html-dsl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor HTML DSL

HTML DSL integrates kotlinx.html so you can write HTML in Kotlin, interpolate variables, and build layouts from templates. It needs no installation, only the artifact `io.ktor:ktor-server-html-builder`.

## Full documents

Call `call.respondHtml` inside a route; the builder emits `html`, `head`, `body` and so on. A typical page has a `title` in the head and an `h1` in the body. For forms, build a `form` with `action`, `method` and `input` elements (the page shows a login form posting `username` and `password` to `/login`).

## Fragments

`call.respondHtmlPartial()` renders only what you put in the builder, with no root `html` element. Use it for partial markup such as dynamic updates with HTMX, e.g. a `div` with class `fragment` containing a `span`.

## Templates

For layouts, use `call.respondHtmlTemplate(SomeTemplate()) { ... }`. The block exposes the template so you can set placeholder values.

- Implement the `Template` interface and override `apply` to emit HTML.
- `Placeholder` inserts content; `PlaceholderList` inserts repeated content (list items).
- `TemplatePlaceholder` inserts a child template for nested layouts.

The page's example splits a page into a root `LayoutTemplate` (properties `header` and `content`), an article child template (`articleTitle`, `articleText`, `list`), and a list template using `PlaceholderList` to build a `UL`, wrapping the first item in `<b>`.

```kotlin
get("/") {
    call.respondHtmlTemplate(LayoutTemplate()) {
        // set header, content ...
    }
}
```

More on kotlinx.html is in its wiki; form parameters on the server side are covered by the Ktor requests docs.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-html-dsl.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
