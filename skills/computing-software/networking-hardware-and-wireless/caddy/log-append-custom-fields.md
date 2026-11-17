---
id: computing-software.networking-hardware-and-wireless.caddy.log-append-custom-fields
name: log-append-custom-fields
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [log-append, access-log, custom-fields, early-field, upstream-duration, caddyfile]
level: practitioner
status: docs-checked
description: "Add custom fields to Caddy access logs with log_append: early versus late fields, upstream timing placeholders and debug body capture."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/log_append
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enrich access log lines with your own keys.

Syntax: `log_append [<matcher>] [<]<key> <value>`. It needs the `log` directive in the site to enable access logging at all. The value is a static string or a placeholder resolved at request time.

Timing: by default a field is added late, on the way back up the middleware chain after handlers like `reverse_proxy`, `respond` or `file_server` have finished, so it records final state. A `<` prefix on the key (`log_append <original_path {http.request.uri.path}`) adds it early, before the next handler, capturing the request before rewrites; the page's example logs the pre-`rewrite /new-base{uri}` path.

Examples: tag the area of the site, `log_append area "static"` inside `handle /static*` and `log_append area "dynamic"` in the proxy branch. After a `reverse_proxy node1:80 node2:80 node3:80 { lb_policy random_choose 2 }` you can log `upstream_host {rp.upstream.host}`, `upstream_duration_ms {rp.upstream.duration_ms}` and `upstream_latency_ms {rp.upstream.latency_ms}`, which show which upstream served and how long it took to proxy and to produce response headers.

Debug only, never production: `{http.request.body}`, `{http.request.body_base64}`, `{http.response.body}` and `{http.response.body_base64}` are specially handled. Request body placeholders force early mode and buffer the request; response body placeholders enable response buffering and are added late. This harms performance and makes logs noisy. Prefer the base64 variants for binary data.

## Checked

2026-11-03: read caddyfile/directives/log_append against this skill. Confirmed: log_append syntax, late versus < early timing, upstream placeholders, body placeholders and their performance warning.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
