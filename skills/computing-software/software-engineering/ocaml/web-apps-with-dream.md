---
id: computing-software.software-engineering.ocaml.web-apps-with-dream
name: web-apps-with-dream
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dream-web, ocaml-web-db, dream-framework, web-server, http-routes, middleware]
level: practitioner
status: docs-checked
description: "Build routes, middleware, sessions and templates with the Dream web framework and run it with Dream.run."
sources: ["https://github.com/camlworks/dream", "https://raw.githubusercontent.com/camlworks/dream/master/src/dream.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dream

```lisp
(executable (name main) (libraries dream) (preprocess (pps lwt_ppx)))
```
```ocaml
let () =
  Dream.run
  @@ Dream.logger
  @@ Dream.router [
       Dream.get "/" (fun _ -> Dream.html "hello");
       Dream.get "/user/:id" (fun r -> Dream.html (Dream.param r "id"));
       Dream.post "/echo" (fun r -> let%lwt body = Dream.body r in Dream.respond body);
     ]
```

## Notes
- `type handler = request -> response promise` and `type middleware = handler -> handler`; promises are Lwt (`'a promise = 'a Lwt.t`).
- `Dream.run` listens on http://localhost:8080 by default; `~port` or the `DREAM_PORT` variable changes the port, `~interface:"0.0.0.0"` listens on all interfaces. It calls `Lwt_main.run`, so it is the program's main loop.
- Without `Dream.set_secret`, a random secret is generated per process: restarts cannot verify earlier CSRF tokens or decrypt earlier cookies, and load-balanced servers will not accept each other's. Set a fixed secret in production.
- `Dream.csrf_tag request` renders a CSRF-safe form field; sessions, cookies, WebSockets and GraphQL are built in.
- Built-in templates: a `template.eml.ml` file turned into `template.ml` by a dune rule running `dream_eml %{deps} --workspace %{workspace_root}`. Alternatives named in the docs are TyXML and mlx.
- The README says Dream runs HTTPS and HTTP/2 without a proxy; Opium is credited as the origin of its handler and middleware types.

## Self-check
- [ ] `curl localhost:8080/` returns "hello".

## Checked

2026-11-08. Read in full: Dream README (camlworks/dream) and src/dream.mli signatures and docs for run, set_secret, csrf_tag, param, body, router, get, post, handler, middleware, templates.
Removed: unconfirmed alternative libraries (piaf, cohttp-eio, Tapir, httpun), ocaml.org landing source.
Method: documentation only; no commands were run.
