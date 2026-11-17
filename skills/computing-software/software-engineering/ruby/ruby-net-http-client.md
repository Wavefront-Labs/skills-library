---
id: computing-software.software-engineering.ruby.ruby-net-http-client
name: ruby-net-http-client
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, net-http-client, http]
level: practitioner
status: docs-checked
description: "Call HTTP APIs with Net::HTTP: TLS, timeouts, JSON bodies, response classes, redirects and retries."
sources: ["https://docs.ruby-lang.org/en/master/Net/HTTP.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP clients with Net::HTTP

```ruby
require "net/http"; require "json"
uri = URI("https://api.example.com/v1/items")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
http.open_timeout = 3; http.read_timeout = 10; http.write_timeout = 10
req = Net::HTTP::Post.new(uri, "Content-Type" => "application/json",
                               "Authorization" => "Bearer #{token}")
req.body = { name: "x" }.to_json
res = http.request(req)
case res
when Net::HTTPSuccess then JSON.parse(res.body)
when Net::HTTPRedirection then # follow res["location"] yourself
else raise "HTTP #{res.code}: #{res.body[0, 200]}"
end
```
One-shot form: `Net::HTTP.get_response(uri)`; `Net::HTTP.start(host, port, use_ssl: true) { |h| ... }` calls `start` before the block and `finish` after it, which suits many requests to one host.

## Gotchas
- The default `open_timeout`, `read_timeout` and `write_timeout` are each 60 seconds, so an outage can stall a worker for a minute per stage. Set shorter values and rescue `Net::OpenTimeout` and `Net::ReadTimeout` (both subclasses of `Timeout::Error`).
- `max_retries` defaults to 1: Net::HTTP retries an idempotent request after errors such as `Net::ReadTimeout`, `IOError`, `EOFError` or `Errno::ECONNRESET`. Set `max_retries = 0` if you need no retries.
- Responses are instances of subclasses of `Net::HTTPResponse`; test with `Net::HTTPSuccess` or `Net::HTTPRedirection` in a `case`, because a 4xx/5xx is a response, not an exception here. Following a redirect is your code's job (the docs show a recursive pattern with a limit).
- Do not disable certificate verification (`verify_mode = OpenSSL::SSL::VERIFY_NONE`); use `ca_file` or `ca_path` to supply a CA bundle.
- Build query strings with `URI.encode_www_form(params)` rather than concatenation.
- Non-idempotent POSTs should not be retried blindly; add an idempotency key on the server side.

Verify: set `read_timeout = 1` against an endpoint that responds slowly and confirm `Net::ReadTimeout` is raised.

## Checked
2026-11-03. Confirmed against ruby/ruby `lib/net/http.rb` rdoc (default 60 second timeouts, `max_retries` default 1 and retried errors, `start` with a block, `get_response`, `use_ssl`, `ca_file`/`ca_path`, `verify_mode`, response classes and redirect example, `URI.encode_www_form`) and `lib/net/protocol.rb` (`OpenTimeout`/`ReadTimeout` are `Timeout::Error` subclasses). Fixed: the old text said Net::HTTP never retries; it retries idempotent requests once by default. Removed: gem recommendations (Faraday, HTTP.rb), the httpbin.org exercise, SocketError/ECONNREFUSED advice.
Method: documentation only; no commands were run.
