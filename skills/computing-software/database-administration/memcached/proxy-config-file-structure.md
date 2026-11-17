---
id: computing-software.database-administration.memcached.proxy-config-file-structure
name: proxy-config-file-structure
category: computing-software
field: database-administration
product: memcached
tags: [proxy-config, pools, routes, lua, settings]
level: advanced
status: docs-checked
description: "Structure of a proxy Lua configuration: optional verbose/debug, settings{}, pools{} with backends and options, routes{}."
sources:
  - https://docs.memcached.org/features/proxy/configure/
  - https://docs.memcached.org/features/proxy/quickstart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Four parts: optional `verbose(true)` / `debug(true)`; optional `settings{}`; one or more `pools{}`; one or more `routes{}`.

```
settings { backend_connect_timeout = 3, active_req_limit = 5 }
pools {
  main_pool = {
    backend_options = { connecttimeout = 5 },
    backends = { "192.0.2.1", "192.0.2.3:11212",
                 { host = "203.0.113.20", port = 11212, connecttimeout = 10 } }
  }
}
routes { default = route_direct{ child = "main_pool" } }
```
Port defaults to 11211. Pool names must not start with `set_`. Pool `options` and `backend_options` are optional tables.

Minimal quickstart: two pools, `map = { quickstart = route_direct{child="quickstart_pool"} }`, `default = route_direct{ child = "fallback" }`.

Run with `memcached -o proxy_config=routelib,proxy_arg=config.lua`.

Mark a backend down with `"192.0.2.2 _down_"` or `down=true`: no traffic goes there and keys are not remapped.

## Checked

2026-11-04. Confirmed against the Configure the built-in proxy page, the Quickstart and the Run page (four parts, pool syntax, port default, set_ reservation, _down_/down=true, proxy_config and proxy_arg). Removed: nothing.

Method: documentation only; no commands were run.
