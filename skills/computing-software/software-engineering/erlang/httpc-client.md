---
id: computing-software.software-engineering.erlang.httpc-client
name: httpc-client
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-web, httpc-client]
level: practitioner
status: draft
description: "Erlang httpc HTTP client from inets: request/4, TLS options, timeouts, profiles and result shapes."
sources:
  - https://ninenines.eu/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# httpc in inets
**Goal:** make HTTP requests from the standard library.

```erlang
{ok, _} = application:ensure_all_started(inets),
{ok, _} = application:ensure_all_started(ssl),
{ok, {{_, 200, _}, Headers, Body}} =
    httpc:request(get, {"https://example.org/", [{"user-agent", "myapp"}]},
                  [{timeout, 5000}, {ssl, [{verify, verify_peer},
                                           {cacerts, public_key:cacerts_get()}]}],
                  [{body_format, binary}]).
```
- Signature `httpc:request(Method, Request, HTTPOptions, Options)`. Request is `{Url, Headers}` or `{Url, Headers, ContentType, Body}`.
- Header names and URLs are strings (lists) unless noted; pass `{body_format, binary}` to get binaries back.
- Set both `timeout` and `connect_timeout`; there is a default connection limit per profile.
- For large or high-throughput clients prefer dedicated libraries such as gun or hackney.

## Gotchas
- Older OTP does not verify certificates by default; always pass SSL options.

## Self-check
Request a page and print the status line and header count.
