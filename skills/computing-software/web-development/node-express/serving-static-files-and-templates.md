---
id: computing-software.web-development.node-express.serving-static-files-and-templates
name: serving-static-files-and-templates
category: computing-software
field: web-development
product: node-express
tags: [express, express-static, template-engines, ejs, cache-control, sendfile, views, web-development]
level: practitioner
status: verified
description: "Serving static assets and server-rendered views in Express: express.static options and caching, sendFile safety, view engines, escaping and production offload."
sources:
  - https://expressjs.com/en/starter/static-files.html
  - https://expressjs.com/en/api.html#express.static
  - https://expressjs.com/en/guide/using-template-engines.html
  - https://ejs.co/#docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving static files and templates in Express

**Goal:** assets served fast with correct caching; views rendered with auto-escaping.

## 1. express.static
```js
import path from "node:path";
const pub = path.join(import.meta.dirname, "public");     // Node 20.11+; CJS: __dirname

app.use("/assets", express.static(path.join(pub, "assets"), {
  immutable: true, maxAge: "1y",         // only for content-hashed filenames
  index: false, fallthrough: true,
}));
app.use(express.static(pub, { maxAge: "1h" }));          // robots.txt, favicon, un-hashed files
```
- Always pass an absolute path; relative paths depend on the process cwd.
- Register static before routes that would shadow it, after middleware that must run on every request (logging). Put it before session/auth middleware so assets don't create sessions.
- `dotfiles` defaults to ignore (`.env` in `public/` is not served - but don't put it there).
- `setHeaders: (res, filePath) => {...}` for per-type headers.

## 2. Cache strategy
Hashed names (`app.3f9a1c.js`) -> `Cache-Control: public, max-age=31536000, immutable`. HTML -> `no-cache` (revalidate with ETag; express sets ETag/Last-Modified by default).

## 3. sendFile safely
```js
app.get("/files/:name", (req, res, next) => {
  res.sendFile(req.params.name, { root: path.join(import.meta.dirname, "files"), dotfiles: "deny" }, (err) => err && next(err));
});
```
Using `root` makes `send` reject `..` traversal. Never `res.sendFile(path.join(dir, req.query.f))` without that. `res.download()` adds `Content-Disposition: attachment`.

## 4. View engines
```js
app.set("views", path.join(import.meta.dirname, "views"));
app.set("view engine", "ejs");
app.get("/", (req, res) => res.render("index", { user: req.user }));
```
- EJS `<%= %>` escapes, `<%- %>` outputs raw HTML (only for trusted partials). Pug escapes `#{}`, `!{}` is raw. Handlebars `{{ }}` escapes, `{{{ }}}` raw.
- `res.locals` for per-request template data (CSP nonce, current user); `app.locals` for app-wide.
- `app.set("view cache", true)` is automatic when `NODE_ENV=production`.

## 5. Production offload
Put nginx/a CDN in front for static assets (gzip/brotli, HTTP/2, range requests). Keep `express.static` for dev or small apps; add `compression` middleware only if no proxy compresses.

## 6. SPA fallback
```js
app.get("/{*splat}", (req, res) => res.sendFile("index.html", { root: pub }));   // Express 5 wildcard syntax; v4: "*"
```
Register after API routes and exclude `/api` so unknown API paths return 404 JSON, not HTML.

## Verify
- [ ] `curl -I /assets/app.<hash>.js` shows `immutable`; `curl -I /` shows no long max-age on HTML.
- [ ] `curl /files/..%2f..%2fetc%2fpasswd` returns 403/404.
- [ ] Rendering a user value containing `<script>` shows it escaped.
