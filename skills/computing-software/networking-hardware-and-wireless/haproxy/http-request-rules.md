---
id: computing-software.networking-hardware-and-wireless.haproxy.http-request-rules
name: http-request-rules
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, http-request, http-request-deny, set-header, set-var, http-request-auth]
level: practitioner
status: docs-checked
description: "Apply http-request rules for allow, deny, auth, redirect, set-header, set-var and track-sc in HAProxy, with ordering and final-action semantics."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http request rules
`http-request <action> [options] [ { if | unless } <condition> ]` rules are evaluated in declaration order, in a frontend, listen or backend section. There is no limit to the number of rules. The condition is evaluated just before the action runs, and each action runs exactly once.

```
frontend fe_web
    http-request set-header X-Request-Id %[uuid()] unless { req.hdr(X-Request-Id) -m found }
    http-request del-header X-Internal
    http-request deny deny_status 403 if { path_beg /admin } !{ src 10.0.0.0/8 }
    http-request auth realm Admin if { path_beg /metrics } !{ http_auth(users) }
    http-request set-var(txn.site) hdr(host),lower
    http-request track-sc0 src table st_abuse
    http-request return status 204 if { path /ping }
```
- Final actions: `deny`, `auth`, `silent-drop` and `tarpit` stop rule evaluation (for `deny` the manual says no further rules from the same rule set are evaluated for the current section). `track-sc0` does not stop evaluation.
- `deny [ { status | deny_status } <code> ]` defaults to HTTP 403 for requests (502 for responses). `deny deny_status <code>` is an alias of `deny status <code> default-errorfiles`; use `return` for a custom body or headers.
- `auth [realm <realm>]` answers 401 or 407 and stops evaluation; the proxy's error message is used and can be customised with `errorfile` or `http-error`.
- `silent-drop` makes the connection disappear without notifying the client; stateful devices between HAProxy and the client keep the connection in their session tables, so use it with care.
- `set-header` removes an existing header of that name first (the new value is computed before the removal, so it can append to the old one). `add-header` adds without removing.
- Rules from a named `defaults` section run before those of the proxy section; `http-request` rules are not allowed in an anonymous `defaults` section.
- A named `defaults` section that holds such rules cannot be shared between frontend-capable and backend-capable proxies, so a `listen` section cannot use it.

Verify: a request to `/admin` from outside the allowed network gets 403; the log shows termination flags `PR` (the proxy blocked the client request because a deny filter matched).

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `http-request` keyword text (order, no limit, condition semantics, named-defaults rules), actions `auth`, `deny`, `return`, `set-header`, `del-header`, `set-var`, `silent-drop`, `tarpit`, `track-sc0`, the fetches `uuid`, `req.hdr`, `path_beg`, `http_auth`, `src`, and the `PR` termination flags. Removed: the claim that the rules run "before backend selection" and that frontend rules run before backend rules, `errorfile 403 /etc/haproxy/errors/403.http` and `curl` details, the claim that the first `redirect`/`allow` is terminal beyond what the manual lists, and the "header normalisation, then access control, then tracking" ordering advice (a convention, not documented). Read as sections of the manual only.
Method: documentation only; no commands were run.
