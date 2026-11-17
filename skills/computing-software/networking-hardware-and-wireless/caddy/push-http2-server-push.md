---
id: computing-software.networking-hardware-and-wireless.caddy.push-http2-server-push
name: push-http2-server-push
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [push, http2, server-push, link-header, preload, caddyfile]
level: advanced
status: docs-checked
description: "Configure HTTP/2 server push in Caddy with push: Link header formats, same-host rule, copied request headers and pushing fixed resources."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/push
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: preemptively send resources to the client over HTTP/2.

Syntax: `push [<matcher>] [<resource>] { [GET|HEAD] <resource>  headers { [+]<field> [<value|regexp> [<replacement>]]  -<field> } }`. In the block the resource can be preceded by a method (the text says GET or POST, with GET default, while the syntax line shows GET|HEAD).

Link-driven push: with a bare `push`, Caddy pushes whatever the upstream's `Link` response headers describe, in forms like `<resource>; as=script`, a comma list `<resource>; as=script,<resource>; as=style`, `<resource>; nopush`, or `<resource>;<resource2>;...`. A resource must begin with `/` (same host). External resources and ones with `nopush` are not pushed.

Request headers on pushed requests: `Accept-Encoding`, `Accept-Language`, `Accept`, `Cache-Control` and `User-Agent` are copied by default because many requests would fail without them. The `headers` block edits others using the same syntax as the `header` directive. Push requests are virtualised internally, so they are very light.

Examples: `push` (Link-driven only); `push * /resources/style.css` (also push that stylesheet on all requests); `push /foo.html /foo.jpg` (push `/foo.jpg` only when `/foo.html` is requested).

## Checked

2026-11-03: read caddyfile/directives/push against this skill. Confirmed: Link header formats, same-host and nopush rules, default copied headers, virtualised requests, push examples; the page itself is inconsistent about GET|HEAD versus GET or POST and the skill says so.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
