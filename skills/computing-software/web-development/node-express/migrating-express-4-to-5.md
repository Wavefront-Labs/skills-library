---
id: computing-software.web-development.node-express.migrating-express-4-to-5
name: migrating-express-4-to-5
category: computing-software
field: web-development
product: node-express
tags: [express-5-migration, express-5, path-to-regexp-v8, express-codemod, async-error-handling, node]
level: practitioner
status: verified
description: "Upgrading Express 4 to 5: new route path syntax (named wildcards, optional braces), removed methods, req.body/req.query changes, promise rejection handling and the codemod."
sources:
  - https://expressjs.com/en/guide/migrating-5.html
  - https://github.com/expressjs/codemod
  - https://github.com/pillarjs/path-to-regexp#express-style-paths
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating Express 4 to 5

Express 5.0.0 was published in September 2024 and became the `latest` npm tag with 5.1.0 (31 March 2025); it requires Node 18+ (`engines`: `>= 18`).

## 1. Run the codemod, then fix the rest
```bash
npx codemod@latest @expressjs/v5-migration-recipe
npm i express@^5
```

## 2. Route path syntax (path-to-regexp v8)
| Express 4 | Express 5 |
|---|---|
| `app.get("*", ...)` | `app.get("/{*splat}", ...)` (matches `/` too) or `"/*splat"` (requires at least one segment; `/` gives 404) |
| `/:file.:ext?` | `/:file{.:ext}` (optional segments in braces) |
| `/user/:id(\\d+)` | regex in strings removed: validate in the handler or use a RegExp route |
| `( ) [ ] ? + !` characters in strings | reserved; escape with `\\` (a bare `?`, `+` or `(` throws at startup) |
Wildcard values are arrays of segments: `req.params.splat` -> `["a", "b"]`.

## 3. Removed / changed APIs
- Number-status signatures: `res.send(200)` now sends the body `200` with status 200 (use `res.sendStatus(200)`); `res.json(obj, 201)` silently ignores the 201 (use `res.status(201).json(obj)`); `res.redirect(url, 301)` throws `Invalid status code` (use `res.redirect(301, url)`). `res.status(301).redirect(url)` does NOT work: `redirect(url)` always answers 302.
- `app.del()` -> `app.delete()`; `req.param(name)` removed (`TypeError: req.param is not a function`) (use `req.params`, `req.body`, `req.query`).
- `res.redirect("back")` / `res.location("back")`: the magic string is no longer supported (it is treated as the literal URL `back`); use `req.get("Referrer") || "/"`.
- `req.body` is `undefined` (not `{}`) when no body parser ran; guard destructuring.
- `req.query` is a getter (not writable) and the default query parser is `"simple"` (no nested `a[b]=c` objects); set `app.set("query parser", "extended")` if you relied on it.
- `express.urlencoded()` defaults `extended: false`; `express.static` ignores dotfiles by default.
- `res.status()` only accepts integers 100-999.

## 4. Async handlers
Rejected promises and thrown errors in async handlers/middleware are passed to `next(err)` automatically. Remove `express-async-errors` and try/catch wrappers that only call `next`.

## Verify
- [ ] Route table tests hit every path pattern (including wildcards and optional segments); error middleware receives async errors; no deprecation warnings at startup.
