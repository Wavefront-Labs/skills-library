---
id: computing-software.networking-hardware-and-wireless.haproxy.use-backend-and-default-backend-routing
name: use-backend-and-default-backend-routing
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, use-backend, default-backend, content-switching, dynamic-backend-names]
level: practitioner
status: docs-checked
description: "Route requests to backends with use_backend and default_backend conditions, including dynamic backend names from a log-format expression."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# use backend and default backend routing
`use_backend <backend> [if|unless <condition>]` switches a frontend or listen section to a backend. All rules are evaluated in declaration order and the first match wins; with no condition the rule always applies. `default_backend` is used when no rule matched. With no default backend, a `listen` section uses its own servers, while a frontend has no server and returns 503.

```
frontend fe_web
    bind :80
    acl host_shop hdr(host) -i shop.example.com
    acl path_static path_beg /static/ /img/
    use_backend be_static if path_static
    use_backend be_shop   if host_shop
    default_backend be_app
```
A plain backend name is resolved at configuration time and a missing backend is a config error. A log-format expression as the name (`use_backend be_%[req.hdr(host),lower]` style) is resolved at run time, with no config-time check; if the result is not a valid backend, no later rule is evaluated and `default_backend` applies. The docs recommend a name prefix no other backend uses so a request cannot force an unauthorised backend. Rules with explicit names also feed the backend's `fullconn` computation; dynamic names cannot.

It also works in TCP mode, either with stateless ACLs (source address) or after a `tcp-request` rule waits for payload, and a TCP frontend may switch to an HTTP backend.

Verify: `haproxy -c -f <config>`, then request each hostname or path and check which backend the log line names.

## Checked
2026-11-03. Confirmed against configuration.html `use_backend` and `default_backend` keywords. Removed: the example with `map(...)` in a dynamic name (not shown in the docs), "a missing backend yields 503 and an X-Haproxy warning" (the docs say `default_backend` applies), "use_backend decides only after all http-request rules" and "a deny there wins" (not stated for this keyword), and the claim that typos fail only at runtime beyond the documented no-config-check rule.
Method: documentation only; no commands were run.
