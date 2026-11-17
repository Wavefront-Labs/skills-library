---
id: computing-software.networking-hardware-and-wireless.envoy.lua-http-filter
name: lua-http-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, lua, envoy-on-request, envoy-on-response, luajit, lua-per-route, scripting]
level: practitioner
status: docs-checked
description: "Add request and response logic to Envoy with the Lua HTTP filter, per-route overrides, and the no-blocking rule."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/lua_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua http filter
The Lua filter runs LuaJIT (mostly Lua 5.1 with some 5.2) scripts on the request and response flows. Design points from the docs: Lua environments are per worker thread (no true globals); scripts run as coroutines, so they are written synchronously while Envoy suspends and resumes around async work; never perform blocking operations, use Envoy APIs for all IO. Supported: header/body/trailer inspection (streaming or buffered), header and trailer edits, async HTTP calls to an upstream cluster, and direct responses that skip further filters (for example 403 after a call to an auth service).

```yaml
http_filters:
- name: envoy.filters.http.lua
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.lua.v3.Lua
    default_source_code:
      inline_string: |
        function envoy_on_request(request_handle)
          request_handle:headers():add("x-seen", "1")
        end
        function envoy_on_response(response_handle)
        end
```
`default_source_code` runs for every request. Named scripts live in `source_codes` and `LuaPerRoute` on a virtual host, route or weighted cluster can disable the filter, select a named script, or inline source (sendable through RDS).

Gotchas: the API surface is deliberately small; very complex or high-performance use cases are assumed to use the native C++ filter API. Because state is per worker, globals differ across workers. Each configured script gets one Lua VM per worker thread plus one on the main thread; the process-wide `lua.lua_vm_count` gauge counts them. `source_codes` selects scripts but does not make them requirable; use `package_paths` to load modules.

## Checked
2026-11-03. Confirmed against lua_filter.rst and the lua.proto reference. Removed or corrected: the unverified x-seen/stats verify step; the filter name now follows the docs.
Method: documentation only; no commands were run.
