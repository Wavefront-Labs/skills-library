---
id: computing-software.cloud-infrastructure-engineering.nginx.hsts-security-headers
name: hsts-security-headers
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [add-header, always, add-header-inherit, response-headers, inheritance]
level: practitioner
status: docs-checked
description: "Using nginx add_header with always, the status codes it applies to, the inheritance rule that drops parent headers, and add_header_inherit."
sources: ["https://nginx.org/en/docs/http/ngx_http_headers_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`add_header name value [always];` (contexts `http`, `server`, `location`, `if in location`) adds a response header field only when the response code is 200, 201, 204, 206, 301, 302, 303, 304, 307 or 308. With `always` (1.7.5) it is added regardless of the code, so error pages carry it too. The value can contain variables.

```nginx
add_header X-Example "value" always;
```

Inheritance trap: `add_header` directives are inherited from the previous level if and only if the current level defines none. A single `add_header` inside a `location` therefore drops every `add_header` set at `server` or `http` level for that location.

From 1.29.3, `add_header_inherit on | off | merge;` (default `on`) changes this: `merge` appends the values from the previous level to those defined at the current level, `off` cancels inheritance. Its own setting is inherited in the standard way, so `add_header_inherit merge;` at the top applies to nested levels unless redefined.

`add_trailer` works the same way for trailers (1.13.2), with its own `add_trailer_inherit` (1.29.3). `expires` adds `Expires` and `Cache-Control` for the same set of response codes as `add_header`.

The values of specific security headers (HSTS and others) are defined by their own specifications, not by the nginx documentation, and are not covered here.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_headers_module` page. Removed: all HSTS, `X-Frame-Options`, `Referrer-Policy` and `preload` values and advice, the headers-more module note, the include snippet recommendation and the curl Verify step, because the nginx pages do not document them.
Method: documentation only; no commands were run.
