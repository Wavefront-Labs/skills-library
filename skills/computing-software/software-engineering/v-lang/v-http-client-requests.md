---
id: computing-software.software-engineering.v-lang.v-http-client-requests
name: v-http-client-requests
category: computing-software
field: software-engineering
product: v-lang
tags: [v-http-client-requests, net-http, net.http, http client, http.get, post_json, fetch, headers, status code, tls, rest, v-lang]
level: practitioner
status: draft
description: "Make HTTP requests with http.get, http.post_json and http.fetch, set headers, timeouts and handle status codes and TLS."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP client: get, post, fetch

Goal: call web APIs.

- Simple: `import net.http; resp := http.get('https://example.com/api')!; println(resp.status_code); println(resp.body)`.
- POST JSON: `resp := http.post_json(url, json.encode(payload))!`; form: `http.post_form(url, {'k': 'v'})!`.
- Custom: `resp := http.fetch(http.FetchConfig{ url: url, method: .put, header: http.new_header_from_map({.authorization: 'Bearer <TOKEN>'}), data: body, user_agent: 'myapp/1.0' })!`.
- Handle statuses yourself: `if resp.status() != .ok { return error('http ${resp.status_code}') }`.
- TLS uses OpenSSL (or mbedtls in some builds; confirm); ensure libssl is installed on Linux.
- Decode: `data := json.decode(Item, resp.body)!`.

Gotchas:
- Network failure returns an error; HTTP 4xx/5xx are not errors by default.
- Never hard-code tokens; read from env (`os.getenv`).
- Set timeouts through FetchConfig fields (confirm names).

Verify: request a local test server and assert the body.
