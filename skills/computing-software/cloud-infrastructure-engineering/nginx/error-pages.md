---
id: computing-software.cloud-infrastructure-engineering.nginx.error-pages
name: error-pages
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, error-page, custom-errors, internal, proxy-intercept-errors]
level: practitioner
status: docs-checked
description: "Custom error pages in nginx with error_page, internal locations, changing the response code, proxy_intercept_errors and the internal redirect limit."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`error_page code ... [=[response]] uri;` (contexts `http`, `server`, `location`, `if in location`) sets the URI shown for the given errors. It causes an internal redirect to the URI with the request method changed to `GET` (for all methods other than `GET` and `HEAD`).

```nginx
error_page 404             /404.html;
error_page 500 502 503 504 /50x.html;
error_page 404 =200 /empty.gif;          # change the response code
error_page 404 = @fallback;              # named location, URI and method unchanged

location = /404.html { internal; }
location @fallback   { proxy_pass http://backend; }
```

- `error_page 404 = /404.php;` (no code after `=`) responds with the code returned by the proxied or FastCGI/uwsgi/SCGI/gRPC server.
- A `uri` can be a URL such as `http://example.com/forbidden.html`; the client then gets `302` by default, changeable to 301, 302, 303, 307 or 308 with `=301` and so on.
- If processing of the error URI leads to an error, the status code of the last error is returned.
- `error_page` directives are inherited from the previous level only if the current level defines none.
- `internal;` limits a location to internal requests; external requests get `404`. Internal redirects are limited to 10 per request; at the limit the error is `500` and the error log shows "rewrite or internal redirection cycle".
- By default, error responses from a proxied server pass through unchanged. `proxy_intercept_errors on;` (default `off`) intercepts proxied responses with codes of 300 or greater and handles them with `error_page`.
- The SSL module adds the non-standard codes `495`, `496` and `497` for use with `error_page`.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_core_module` page (`error_page`, `internal`) and `ngx_http_proxy_module` (`proxy_intercept_errors`). Removed: `limit_req_status` mapping note, claims about cascading errors and loop behaviour beyond the documented 10-redirect limit, and the curl Verify step.
Method: documentation only; no commands were run.
