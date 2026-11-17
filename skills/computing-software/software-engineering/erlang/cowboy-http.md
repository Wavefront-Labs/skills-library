---
id: computing-software.software-engineering.erlang.cowboy-http
name: cowboy-http
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-web, cowboy-http]
level: practitioner
status: draft
description: "Cowboy 2 HTTP: router dispatch, handler init callback, replying, start_clear and TLS listeners."
sources:
  - https://ninenines.eu/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cowboy HTTP server
**Goal:** serve HTTP from an Erlang release.

```erlang
Dispatch = cowboy_router:compile([{'_', [{"/hello/:name", hello_h, []}]}]),
{ok, _} = cowboy:start_clear(http, [{port, 8080}], #{env => #{dispatch => Dispatch}}).
-module(hello_h).
-export([init/2]).
init(Req0, State) ->
    Name = cowboy_req:binding(name, Req0),
    Req = cowboy_req:reply(200, #{<<"content-type">> => <<"text/plain">>},
                           <<"hello ", Name/binary>>, Req0),
    {ok, Req, State}.
```
- Cowboy 2.x is built on Ranch (acceptor pool). Add `cowboy` to `deps` and `applications`.
- `cowboy:start_tls/3` for HTTPS with `certfile`/`keyfile` transport options.
- Handlers run in a process per request: a crash gives a 500 and does not affect others.
- Read bodies with `cowboy_req:read_body/1` (check `more` vs `ok` for large bodies); set body size and timeout limits.

## Gotchas
- Cowboy 2 handler return values and map-style options differ from 1.x; check docs matching your version.

## Self-check
Start the listener and `curl localhost:8080/hello/world`.
