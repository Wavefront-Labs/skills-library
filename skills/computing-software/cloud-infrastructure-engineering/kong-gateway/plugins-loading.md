---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.plugins-loading
name: plugins-loading
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, bundled, plugins-setting, vaults, kong-conf, lua-package-path]
level: practitioner
status: docs-checked
description: "Control which plugins and vaults Kong loads with the plugins and vaults settings (default bundled, off loads none) and where custom plugins are found."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading plugins and vaults

| Setting | Default | Meaning |
|---|---|---|
| `plugins` | `bundled` | which plugins to load; `off` loads none |
| `vaults` | `bundled` | which vault backends to load |

Loading a plugin does not enable it: you still create a plugin entity (global, or scoped to a Service, Route or Consumer).

Custom plugin code is found through the Lua module path:
- `lua_package_path` default `./?.lua;./?/init.lua;`
- `lua_package_cpath` default empty

In hybrid mode, custom plugins must be installed on both the control plane and the data planes. Data plane plugin versions must match the control plane major version, and a data plane's plugin minor version cannot be newer than the control plane's.

Some bundled plugins need a database and are not supported in DB-less mode.

Related: `tracing_instrumentations` (default `off`) and `tracing_sampling_rate` (default `0.01`).

## Checked

2026-11-04. Confirmed against kong.conf.default (`plugins` and `vaults` defaults and `off`, loading versus enabling, `lua_package_path` and `lua_package_cpath` defaults, tracing defaults) and the Hybrid mode and DB-less mode pages (custom plugins on both planes, plugin version rules, DB-less plugin support). Nothing removed.
Method: documentation only; no commands were run.
