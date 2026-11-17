---
id: computing-software.software-engineering.prolog.http-server-handlers
name: http-server-handlers
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-http, http-server-handlers, http-handler]
level: advanced
status: draft
description: "Serve routes with library(http/http_server): http_handler/3, http_server/2, reply_json_dict/1 and format of request parsing."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP server
```prolog
:- use_module(library(http/http_server)).
:- use_module(library(http/http_json)).
:- http_handler(root(hello), hello, []).
:- http_handler(root(api/echo), echo, [method(post)]).
hello(_Request) :- format("Content-type: text/plain~n~n"), format("hi~n").
echo(Request) :- http_read_json_dict(Request, D), reply_json_dict(D).
server(Port) :- http_server([port(Port)]).
?- server(8080).
```
- `http_parameters/3` parses query/form params with type checks.
- Test with `curl localhost:8080/hello`.
## Gotchas
- Bind to localhost during development, put TLS and auth in front for production.
- Handlers run in worker threads: avoid unsynchronised global state.
- `http_server` library name differs from older `http_unix_daemon`.
## Self-check
Start the server and call `/hello` and a JSON echo with curl.
