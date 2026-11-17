---
id: computing-software.software-engineering.v-lang.v-veb-vs-vweb-migration
name: v-veb-vs-vweb-migration
category: computing-software
field: software-engineering
product: v-lang
tags: [v-veb-vs-vweb-migration, web-framework-veb, vweb migration, veb migration, deployment, reverse proxy, nginx, systemd, docker, production, v-lang]
level: advanced
status: draft
description: "Migrate old vweb code to veb, run behind a reverse proxy, set timeouts and ports, and package a server binary."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vweb to veb migration and deployment notes

Goal: upgrade and ship.

- Migration (confirm exact steps in the release notes): `import vweb` -> `import veb`; `vweb.Context` -> `veb.Context` embedded in your own `Context` struct; handlers take `mut ctx Context` instead of using `app.Context`; `vweb.run(&App{}, port)` -> `veb.run[App, Context](mut app, port)`; `vweb.Result` -> `veb.Result`.
- Middleware and static handling were redesigned; re-read the veb docs.
- Deploy: `v -prod -o server .`; put behind nginx/Caddy for TLS and gzip; run with systemd (`Restart=on-failure`), or in a minimal container (`FROM scratch` needs static linking, otherwise slim Debian).
- Config via env: `port := os.getenv_opt('PORT') or { '8080' }.int()`.
- Health route returning `ctx.text('ok')`.

Gotchas:
- Production GC/memory flags matter for long uptime: test with `-gc boehm` or default per your version.
- Without a proxy, set conservative request size/timeouts (`veb.RunParams`; confirm).

Verify: load test with `wrk` or `hey` and watch memory.
