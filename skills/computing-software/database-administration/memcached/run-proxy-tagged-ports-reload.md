---
id: computing-software.database-administration.memcached.run-proxy-tagged-ports-reload
name: run-proxy-tagged-ports-reload
category: computing-software
field: database-administration
product: memcached
tags: [proxy-run, tagged-ports, sighup, reload, proxy-arg]
level: advanced
status: docs-checked
description: "Run the proxy with proxy_config and proxy_arg, tagged -l listeners, and reload config with SIGHUP without dropping clients."
sources:
  - https://docs.memcached.org/features/proxy/run/
  - https://docs.memcached.org/features/proxy/configure/
  - https://docs.memcached.org/features/proxy/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```
memcached -o proxy_config=routelib,proxy_arg=/path/to/my_config.lua -p 11212 &
```
Use a file path instead of `routelib` to load a modified library.

Tagged ports: repeat `-l TAG:HOST:PORT`, mixing tagged and untagged.
```
-l 127.0.0.1:11211 -l main:127.0.0.1:11212 -l alt:127.0.0.1:11213
```
Each tag selects a `routes{ tag = "..." }` tree; the untagged tree is the default.

Reload: edit the config, then `kill -HUP <pid>`. Valid config is applied; invalid config is rejected and the old one remains. Read errors with `watch proxyevents`. In-flight requests finish on the old routes; new ones use the new. Avoid Lua globals, use closures.

Test: `telnet localhost 11212`, `get proxy-test`, expect `END`.

## Checked

Confirmed 2026-11-09: `proxy_config` and `proxy_arg` options with the built-in `routelib` or a file path, `-l TAG:HOST:PORT` tagged listeners mixed with untagged, one `routes{}` tree per tag with an untagged default, SIGHUP reload that keeps the old configuration when the new one is invalid, errors visible with `watch proxyevents`, in-flight requests immune to reloads and the advice to use closures instead of globals, and the telnet `get` test returning `END` (Run, Configure and FAQ pages of the built-in proxy). Changed the test port to 11212 to match the example command.

Method: docs-checked 2026-11-09 against docs.memcached.org Run the built-in proxy, Configure the built-in proxy and proxy FAQ pages
