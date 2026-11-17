---
id: computing-software.web-development.leptos.document-head-with-leptos-meta
name: document-head-with-leptos-meta
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, leptos-meta, head, seo, title]
level: practitioner
status: docs-checked
description: "Set title, meta, link, style, script and html or body attributes from any component with leptos_meta, and render them into the head during SSR."
sources: [https://book.leptos.dev/metadata.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change `<head>` content (title, meta tags, stylesheets) using components.

## Components
From the `leptos_meta` crate:
- `<Title/>`: set the document title; takes a `formatter`. With `<Title formatter=|text| format!("{text} — My Awesome Site")/>` in `<App/>`, a route's `<Title text="Page 1"/>` yields `Page 1 — My Awesome Site`.
- `<Link/>`: inject a `<link>`.
- `<Stylesheet/>`: `<link rel="stylesheet">` with your `href`.
- `<Style/>`: a `<style>` with children, e.g. `<Style>{include_str!("my_route.css")}</Style>`.
- `<Meta/>`: `<meta>` tags such as description.
- `<Script/>`: a script in the `<head>`.
- `<Html/>` and `<Body/>`: add attributes to `<html>`/`<body>` using spread syntax:

```rust
<Html
    {..}
    lang="he"
    dir="rtl"
    data-theme="dark"
/>
```

## Script vs script
Capital `<Script/>` renders in the `<head>`; lowercase `<script>` renders where you place it in the body. They load and run at different times; choose accordingly.

## Gotchas
- Use these components in the body of your app, inside components. Do not put them inside a `<head>` you write yourself (e.g. under SSR); there, use the plain HTML elements.
- With server rendering the crate collects all declared head content and injects it into the real `<head>`. The page says this matters for SEO: crawlers prefer pages rendered to HTML with metadata in the `<head>`.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/metadata.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
