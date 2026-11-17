---
id: computing-software.software-engineering.elixir.http-client-req-finch
name: http-client-req-finch
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, req, finch, httpoison, tesla, http-client, retry, timeouts, connection-pool, http-client-req, elixir-http-clients]
level: practitioner
status: draft
description: "Make HTTP calls with Req (built on Finch) including JSON decoding, retries, timeouts and connection pools; start Finch pools in the supervision tree."
sources: ["https://hexdocs.pm/req", "https://hexdocs.pm/finch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP requests with Req and Finch

**Goal:** robust outbound HTTP.

```elixir
# deps: {:req, "~> 0.5"}   (check the current version)
resp = Req.get!("https://api.example.com/items", params: [page: 1], headers: [accept: "application/json"], receive_timeout: 10_000)
resp.status ; resp.body            # body is JSON-decoded automatically for JSON responses
Req.post!(url, json: %{a: 1}, auth: {:bearer, token}, retry: :transient, max_retries: 3)
{:ok, resp} = Req.request(url: url, method: :get)    # non-raising variants return {:ok, resp} | {:error, exception}
# custom pool: {Finch, name: MyFinch, pools: %{default: [size: 50]}}  then Req.get(url, finch: MyFinch)
```

## Rules
- Always set timeouts (`receive_timeout`, `connect_options: [timeout: ...]`); the defaults are finite but check them for your version.
- `Req.get!` raises on transport errors, not on 4xx/5xx (check `resp.status` or use `Req.get(..., raise: ...)` options per docs).
- For tests, use `Req.Test` stubs or a behaviour wrapper with Mox rather than hitting real services.
- Retry only idempotent requests; use backoff.
- Older code uses HTTPoison/Tesla/`:httpc`; keep one client per project.

## Self-check
Call an endpoint returning 500 with `retry: :transient` and confirm the number of attempts in logs.
