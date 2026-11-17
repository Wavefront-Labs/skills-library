---
id: computing-software.networking-hardware-and-wireless.caddy.forward-auth-gateway
name: forward-auth-gateway
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [forward-auth, authelia, tailscale, copy-headers, auth-gateway, sso, caddyfile]
level: advanced
status: docs-checked
description: "Delegate authentication to an external gateway with forward_auth: 2xx grants access, copy_headers (with renaming), the expanded reverse_proxy form, Authelia and Tailscale."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/forward_auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let an auth service decide whether a request may continue.

`forward_auth [<matcher>] [<upstreams...>] { uri <to>  copy_headers <fields...> { <fields...> } }` proxies a clone of the request to the gateway as a `GET` with the URI rewritten (so the body is not consumed). A `2xx` answer grants access: headers named in `copy_headers` are copied from the gateway response to the original request and processing continues. Any other status is copied back to the client, normally a redirect to the gateway's login page. `uri` (specify once) is the gateway's verification endpoint. A `copy_headers` entry can rename with `>`, as `Before>After`; a block lists fields one per line. All `reverse_proxy` subdirectives pass through.

Expanded equivalent: `reverse_proxy <upstreams...> { method GET  rewrite <to>  header_up X-Forwarded-Method {method}  header_up X-Forwarded-Uri {uri}  @good status 2xx  handle_response @good { request_header Remote-User {rp.header.Remote-User} ... } }`. Borrow from it if your gateway needs something different.

Authelia: serve the gateway with `auth.example.com { reverse_proxy authelia:9091 }`, then protect an app with `forward_auth authelia:9091 { uri /api/authz/forward-auth  copy_headers Remote-User Remote-Groups Remote-Name Remote-Email }` followed by `reverse_proxy app1:8080`.

Tailscale (nginx-auth): `forward_auth unix//run/tailscale.nginx-auth.sock { uri /auth  header_up Remote-Addr {remote_host}  header_up Remote-Port {remote_port}  header_up Original-URI {uri}  copy_headers { Tailscale-User>X-Webauth-User ... } }`.

## Checked
2026-11-03. Confirmed against the Caddy forward_auth directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
