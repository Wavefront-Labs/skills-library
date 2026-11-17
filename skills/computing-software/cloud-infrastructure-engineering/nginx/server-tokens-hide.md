---
id: computing-software.cloud-infrastructure-engineering.nginx.server-tokens-hide
name: server-tokens-hide
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, server-tokens, information-disclosure, hardening, version]
level: practitioner
status: docs-checked
description: "Reducing nginx information leakage: server_tokens off, hiding backend headers, denying dotfiles and turning off autoindex."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/ngx_http_access_module.html", "https://nginx.org/en/docs/http/ngx_http_autoindex_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`server_tokens` (default `on`; contexts `http`, `server`, `location`) controls emitting the nginx version on error pages and in the `Server` response header. Its values are `on`, `off`, `build` (adds the build name) or, in the commercial subscription, a `string`.

```nginx
http {
    server_tokens off;
    proxy_hide_header X-Powered-By;   # do not pass this upstream header to clients
}

location ~ /\.(?!well-known) { deny all; }
```

- With `off` the version is no longer emitted. In the commercial subscription (1.9.13+) an explicit `string` can set the signature, and an empty string disables the `Server` field.
- By default nginx does not pass the `Date`, `Server`, `X-Pad` and `X-Accel-...` fields from a proxied response; `proxy_hide_header` adds more fields to that list, `proxy_pass_header` permits passing the disabled ones.
- Upstream error pages can be replaced with nginx's own: `proxy_intercept_errors on` passes proxied responses with code 300 or above to `error_page` (default off).
- `autoindex` defaults to `off`; keep it off unless a listing is intended.
- `deny all` (ngx_http_access_module) refuses access; `limit_except` restricts HTTP methods in a location.

## Checked
Date: 2026-11-03.
Confirmed in the core, proxy, access and autoindex module pages: everything above.
Removed as unconfirmed: the "obscurity, not a fix" framing, the headers-more module advice, generic patching/module-disabling advice, and the curl verify step.
Method: documentation only; no commands were run.
