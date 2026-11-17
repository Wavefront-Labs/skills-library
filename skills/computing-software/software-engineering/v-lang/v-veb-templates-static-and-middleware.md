---
id: computing-software.software-engineering.v-lang.v-veb-templates-static-and-middleware
name: v-veb-templates-static-and-middleware
category: computing-software
field: software-engineering
product: v-lang
tags: [v-veb-templates-static-and-middleware, web-framework-veb, veb templates, veb.html, static files, middleware, include, csrf, cookies, sessions, v-lang]
level: advanced
status: draft
description: "Render HTML templates with $veb.html(), serve static assets with StaticHandler, and add middleware for auth and logging."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# veb templates, static files and middleware

Goal: build real pages.

- Templates: file with the same name as the handler in `templates/` (e.g. `index.html`); render with `return $veb.html()`. Template syntax uses `@name` variables, `@if cond {}`, `@for item in items {}`, `@include 'partial.html'`, `@{expr}`.
- Assets: embed a `static/` dir: `app.mount_static_folder_at('static', '/static')` or struct embedding `veb.StaticHandler` and `app.handle_static('assets', true)!` (confirm API in your version).
- Middleware: embed `veb.Middleware[Context]` in App and register with `app.use(handler: auth_check)`; per-route: `@[middleware: auth_check]`.
- Cookies: `ctx.set_cookie(http.Cookie{ name: 'sid', value: id, http_only: true })`, read `ctx.get_cookie('sid')`.
- CSRF: `ctx.csrf_token_input()` helpers in `veb.csrf` (confirm).
- Set `Content-Type` and caching headers via `ctx.set_header`.

Gotchas:
- Template files are compiled in; changes require rebuild (use `v -d veb_livereload`, confirm).
- Auto-escape: templates escape HTML by default; use `@{x}` carefully with trusted raw content.

Verify: render a list page and view source for escaped output.
