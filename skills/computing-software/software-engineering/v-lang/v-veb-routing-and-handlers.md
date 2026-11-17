---
id: computing-software.software-engineering.v-lang.v-veb-routing-and-handlers
name: v-veb-routing-and-handlers
category: computing-software
field: software-engineering
product: v-lang
tags: [v-veb-routing-and-handlers, web-framework-veb, veb, vweb, web framework, routes, get, post, context, mvc, http server, v-lang]
level: practitioner
status: draft
description: "Create a veb app with an App struct, Context, route attributes like @[get] and @[post], path params, and veb.run."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# veb app structure, routes and handlers

Goal: serve routes with V's web framework (vweb was renamed veb in 2024; older code imports `vweb`, confirm for your version).

```v
import veb
pub struct Context { veb.Context }
pub struct App {}
@['/']
pub fn (app &App) index(mut ctx Context) veb.Result { return ctx.text('hello') }
@['/user/:id']
pub fn (app &App) user(mut ctx Context, id int) veb.Result { return ctx.json({'id': id}) }
@[post]
pub fn (app &App) create(mut ctx Context) veb.Result { return ctx.text(ctx.form['name']) }
fn main() { mut app := &App{}; veb.run[App, Context](mut app, 8080) }
```
- Method name is the route unless an attribute path is given; `@[get]`, `@[post]`, `@[put]`, `@[delete]` restrict methods.
- Query: `ctx.query['q']`; form: `ctx.form['x']`; headers `ctx.get_header(.content_type)`; redirects `ctx.redirect('/')`.
- Handlers returning `veb.Result` use `ctx.html`, `ctx.text`, `ctx.json`, `ctx.file`, `ctx.not_found()`.

Gotchas:
- Handlers run on multiple threads; keep App state behind `shared` or mutexes.
- Context type name and generics changed between vweb and veb; follow your version's examples.

Verify: `curl localhost:8080/user/3` returns JSON.
