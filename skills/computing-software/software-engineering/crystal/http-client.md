---
id: computing-software.software-engineering.crystal.http-client
name: http-client
category: computing-software
field: software-engineering
product: crystal
tags: [http-client, http-server-client, get, post, headers, timeouts, tls, form-data, https, response-status, params, crystal]
level: practitioner
status: draft
description: "Make GET and POST requests with HTTP::Client, set headers, timeouts, form and JSON bodies, TLS and handle redirects."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP::Client requests

Goal: call APIs.

```crystal
require "http/client"
res = HTTP::Client.get("https://example.com/x", headers: HTTP::Headers{"Accept" => "application/json"})
res.status_code; res.body
HTTP::Client.post("https://x/y", form: {"a" => "1"})
HTTP::Client.post("https://x/y", headers: HTTP::Headers{"Content-Type" => "application/json"}, body: data.to_json)
```
- Reuse a connection: `HTTP::Client.new(URI.parse("https://x")) { |c| c.get("/a"); c.get("/b") }`.
- Timeouts: `client.connect_timeout = 5.seconds`, `read_timeout`, `write_timeout`.
- Streaming: `HTTP::Client.get(url) { |res| res.body_io.each_line { ... } }`.
- Errors: `Socket::ConnectError`, `IO::TimeoutError`, `OpenSSL::SSL::Error`.

Gotchas:
- Redirects are not followed automatically; check `res.headers["Location"]`.
- No default timeouts: set them.
- Use `res.success?` and `raise_for_status`-style checks yourself.
- TLS needs libssl at build and runtime.

Verify: request a local server and compare body.
