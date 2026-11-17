---
id: computing-software.cloud-infrastructure-engineering.nginx.http-to-https-redirect
name: http-to-https-redirect
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [return-301, redirect, return, https, host]
level: intro
status: docs-checked
description: "Redirecting HTTP to HTTPS in nginx with return 301, using $host and $request_uri, and the 307/308 codes."
sources: ["https://nginx.org/en/docs/http/ngx_http_rewrite_module.html", "https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`return code URL;` (contexts `server`, `location`, `if`) stops processing and returns the code; for 301, 302, 303, 307 and 308 the second argument is a redirect URL, which can contain variables. A catch-all redirect on the plain-HTTP port:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    return 301 https://$host$request_uri;
}
```

- `$host` is, in this order of precedence, the host name from the request line, the host name from the `Host` request header, or the server name matching the request. `$request_uri` is the full original request URI with arguments.
- `$server_name` is the name of the server that accepted the request, so it forces a fixed name instead of echoing the requested host.
- `default_server` makes the block the default for that address:port pair; without it the first `server` for the pair is the default.
- `307` was not treated as a redirect code before 1.1.16 and 1.0.13, and `308` not before 1.13.0.
- The non-standard code `444` closes the connection without sending a response header.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_rewrite_module` page (`return`) and `ngx_http_core_module` (`listen`, `$host`, `$request_uri`, `$server_name`). Removed: ACME challenge carve-out, claims about browser caching of 301, Host-header reflection, method conversion by clients, `server_name _`, and the curl Verify step.
Method: documentation only; no commands were run.
