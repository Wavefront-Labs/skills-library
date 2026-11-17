---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-cache-key-bypass
name: proxy-cache-key-bypass
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-cache-key, proxy-cache-bypass, proxy-no-cache]
level: advanced
status: docs-checked
description: "Controlling nginx proxy cache keys, bypass and no-cache conditions, cached methods, and how Vary and Set-Cookie affect caching."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`proxy_cache_key string;` default `$scheme$proxy_host$request_uri` (close to `$scheme$proxy_host$uri$is_args$args`). The page's example is `proxy_cache_key "$host$request_uri $cookie_user";`. Anything that changes the response but is not in the key will be shared between requests. The default key has `$proxy_host` (the proxied server), not the client `Host`, so add `$host` if several virtual hosts share one backend.

```nginx
map $http_cookie $skip_cache { default 0; ~*session= 1; }
proxy_cache_bypass $skip_cache;   # do not take the response from the cache
proxy_no_cache     $skip_cache;   # do not save the response to the cache
```

- `proxy_cache_bypass string ...;` defines conditions under which the response is not taken from the cache; `proxy_no_cache string ...;` defines conditions under which it is not saved. If at least one value is not empty and not `0`, the condition applies. They can be used together; the page's examples use `$cookie_nocache $arg_nocache$arg_comment` and `$http_pragma $http_authorization`.
- `proxy_cache_methods` default `GET HEAD`; `GET` and `HEAD` are always added. `proxy_cache_convert_head` (default `on`) converts `HEAD` to `GET` for caching; when disabled, the key should include `$request_method`.
- Response headers can affect caching: `X-Accel-Expires`, then `Expires` or `Cache-Control`; a response with `Set-Cookie` is not cached; `Vary: *` is not cached, while any other `Vary` value is cached taking the corresponding request header fields into account (1.7.7). `proxy_ignore_headers` can disable the processing of these fields.
- `proxy_cache_min_uses` sets the number of requests after which a response is cached (default `1`).

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_proxy_module` page. Fixed: the draft claimed nginx ignores most `Vary` values; the page says a non-`*` `Vary` is honoured using the named request headers. Removed: the `X-Cache-Status` verification, the `$request_body` caching claim, query-string normalisation advice and the cookie curl Verify step.
Method: documentation only; no commands were run.
