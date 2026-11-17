---
id: computing-software.software-engineering.crystal.kemal-framework
name: kemal-framework
category: computing-software
field: software-engineering
product: crystal
tags: [kemal-framework, frameworks, kemal, sinatra-like, web-framework, routes, middleware, rest-api, websocket-kemal, crystal]
level: practitioner
status: draft
description: "Build small web apps and APIs with Kemal: routes, params, JSON responses, filters, static files and the middleware stack."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kemal micro framework

Goal: use Kemal (confirm current version and API at kemalcr.com).

```crystal
require "kemal"
get "/" { "hello" }
get "/users/:id" do |env|
  env.response.content_type = "application/json"
  {id: env.params.url["id"]}.to_json
end
post "/items" do |env|
  name = env.params.json["name"].as(String)
  env.response.status_code = 201
end
Kemal.run
```
- Sinatra-like DSL on top of `HTTP::Server`; handlers via `add_handler`; `before_all`/`after_all` filters; `error 404 { }`; `ws "/chat" do |socket| ... end`.
- Params: `env.params.url`, `.query`, `.body`, `.json`, file uploads in `env.params.files`.
- Config: `Kemal.config.port = 3000`, env `KEMAL_ENV=production`; static files from `public/`.

Gotchas:
- Top-level handlers share global state; use a Mutex for shared data.
- Validate JSON params; `as(String)` raises on wrong types.
- Sessions and auth come from add-on shards.

Verify: `curl localhost:3000/users/5`.
