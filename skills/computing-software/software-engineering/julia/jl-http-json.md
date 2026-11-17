---
id: computing-software.software-engineering.julia.jl-http-json
name: jl-http-json
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-web, http-json]
level: practitioner
status: draft
description: "Make HTTP requests with timeouts and retries and parse JSON into typed structs."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP.jl requests and JSON parsing
- `r = HTTP.get(url; readtimeout = 10, retries = 3)`; `r.status`, `String(r.body)`; `HTTP.post(url, headers, body)`.
- By default HTTP.jl throws `StatusError` on 4xx/5xx; pass `status_exception = false` to inspect.
- `JSON3.read(str, MyStruct)` with `StructTypes.StructType(::Type{MyStruct}) = StructTypes.Struct()`; `JSON3.write(obj)`; JSON.jl (`JSON.parse`) is simpler.
- Servers: `HTTP.serve` or Oxygen.jl.
Verify: test with a local `HTTP.serve` or mocked response.
