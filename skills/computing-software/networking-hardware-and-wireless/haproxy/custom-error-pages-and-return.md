---
id: computing-software.networking-hardware-and-wireless.haproxy.custom-error-pages-and-return
name: custom-error-pages-and-return
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, errorfile, errorfiles, http-request-return, custom-503-page, http-error]
level: practitioner
status: docs-checked
description: "Replace HAProxy's built-in error responses with errorfile, errorfiles sections and http-request return, including http-after-response headers."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom error pages and return
`errorfile` replaces errors that HAProxy itself generates (not errors returned by servers). The codes it can generate are 200, 400, 401, 403, 404, 405, 407, 408, 410, 413, 425, 429, 500, 501, 502, 503 and 504 (200 answers a `monitor-uri` match).

The file must hold a full, valid HTTP response, headers included; the docs suggest naming it `.http` and using an absolute path (files are read before any chroot):
```
HTTP/1.0 503 Service Unavailable
Cache-Control: no-cache
Connection: close
Content-Type: text/html

<html><body><h1>Back soon</h1></body></html>
```
```
defaults
    errorfile 503 /etc/haproxy/errors/503.http
http-errors myerrors
    errorfile 404 /etc/haproxy/errors/404.http
frontend fe_web
    errorfiles myerrors 404
    http-request return status 200 content-type text/plain string "ok" if { path /ping }
    http-request return status 503 content-type text/html file /etc/haproxy/errors/maint.html if { nbsrv(be_app) lt 1 }
    http-after-response set-header Cache-Control no-store if { status 503 }
```
`http-errors <name>` defines a reusable group; `errorfiles <name> [codes]` imports all or the listed codes of it into a proxy. `return` generates a response without contacting a server: `status`, `content-type`, a body from `string`, `lf-string` (log-format), `file`, `lf-file`, `errorfile`/`errorfiles`/`default-errorfiles`, plus `hdr <name> <fmt>`. `errorloc302 <code> <url>` (and `errorloc303`, which uses a 303 so non-GET methods are refetched with GET) redirects to the Location instead of serving a page.

Gotchas: error files are parsed when HAProxy starts and kept in memory, so changes need a reload; a response must not exceed `tune.bufsize` minus `tune.maxrewrite` (otherwise an internal error is returned); avoid references to local content such as images, which loop when all servers are down.

Verify: with all backends down, `curl -i http://lb/` returns your page with 503 and `Cache-Control: no-store`.

## Checked
2026-11-03. Confirmed against configuration.html: `errorfile`, `errorfiles`, `http-errors` (section 3.8), `errorloc302/303`, `return` (http-request), `http-after-response set-header`, `status` and `nbsrv` fetches. Corrected: oversize pages cause an internal error rather than truncation. Removed: the CRLF remark, the explicit list of a few codes (replaced with the documented list), and `lf-string`-only phrasing.
Method: documentation only; no commands were run.
