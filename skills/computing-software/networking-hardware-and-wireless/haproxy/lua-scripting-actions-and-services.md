---
id: computing-software.networking-hardware-and-wireless.haproxy.lua-scripting-actions-and-services
name: lua-scripting-actions-and-services
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, lua, load-lua, register-action, lua-fetch, haproxy-lua]
level: practitioner
status: docs-checked
description: "Extend HAProxy with Lua: lua-load, register_action, register_fetches, register_service and the core.* APIs, with performance cautions."
sources:
  - https://www.haproxy.org/download/3.0/doc/lua.txt
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua scripting actions and services
Lua runs inside HAProxy for custom logic. Lua actions, sample fetches, converters and services are added with the `core` register functions: `core.register_action()`, `core.register_converters()`, `core.register_fetches()`, `core.register_init()`, `core.register_service()` and `core.register_task()`. These are the entry points; registered names become usable in the configuration.

Load scripts from the `global` section:
- `lua-load <file> [args]`: one shared state visible to all threads; the recommended easy way, but only one thread runs on the global state at a time, so it does not scale if many Lua calls are made. Scripts see 0 in `core.thread`. Arguments are read with `local args = table.pack(...)`.
- `lua-load-per-thread <file> [args]`: an independent copy per thread, running concurrently and highly scalable; recommended for simple functions that register fetches, converters, actions or services and do not depend on global variables (globals are thread-local, so avoid them). Check `core.thread` for work that must happen once.
Both directives may be used several times.

Use a service from the config with `http-request use-service <service-name>`: the service replies to the request and the rule is final (no further rules of that set run). Custom TCP and HTTP services can be written in Lua.

Cautions (from the Lua documentation):
- HAProxy is event driven. A blocking call in the data path stalls the whole process: no accepting or forwarding. It looks fine with one test stream and fails under production load.
- Filesystem functions (`io.*`, `os.remove`, `os.rename`, `os.tmpname`, `package.*`, `file.*`) are prohibited at runtime, and `os.execute()` blocks HAProxy; blocking is fine only during initialisation (typically loading files). Avoid `print()`; use `core.log()` or the transaction log.
- The socket class and `core.sleep()` look blocking in Lua but are compatible with the non-blocking design.
- Lua execution is interrupted after a configurable number of instructions so HAProxy stays responsive.
- An HTTP action should manipulate HTTP headers only. Using the channel object on an HTTP request can corrupt it so the action never resumes, and HAProxy drops it after the reception timeout.
- If Lua runs out of memory the current Lua action fails and processing continues, so do not rely on a Lua action alone for a security decision.
- Limits: `tune.lua.maxmem` (megabytes per process, default 0 = unlimited; set one), `tune.lua.service-timeout` and `tune.lua.session-timeout` (pure Lua runtime only, sleeps not counted; default 4s each).

Verify: `haproxy -c -f <config>` accepts the configuration, then exercise the registered action or service with a request and confirm the response.

## Checked
2026-11-09. Confirmed against the HAProxy 3.0 Lua overview (lua.txt: register functions, non-blocking design, prohibited functions, HTTP action warning, memory-failure behaviour) and the 3.0 configuration manual (`lua-load`, `lua-load-per-thread`, `tune.lua.*` defaults, `use-service`). Removed: the example script (the txn, applet and core method names are in the Lua API reference, not read), the `-vv | grep lua` check, the "2.4+" version note, the luasocket and `core.tcp()` remarks, the default-deny claim, curl check values.
Method: documentation only; no commands were run.
