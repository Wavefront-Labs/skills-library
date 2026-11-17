---
id: computing-software.cloud-infrastructure-engineering.nginx.limit-rate-bandwidth
name: limit-rate-bandwidth
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, limit-rate, limit-rate-after, bandwidth, downloads]
level: practitioner
status: docs-checked
description: "Throttling download speed in nginx with limit_rate, limit_rate_after, variables, X-Accel-Limit-Rate and proxy_limit_rate."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`limit_rate rate;` (default `0`, no limit; contexts `http`, `server`, `location`, `if in location`) limits the response transmission rate to a client in bytes per second. The limit is per request, so a client with two simultaneous connections gets twice the rate.

`limit_rate_after size;` (default `0`) sets the initial amount after which transmission is rate limited.

```nginx
location /flv/ {
    flv;
    limit_rate_after 500k;
    limit_rate       50k;
}

map $slow $rate {
    1  4k;
    2  8k;
}
limit_rate $rate;
```

- The value can contain variables (1.17.0), useful to limit by condition as in the `map` example.
- Setting the `$limit_rate` variable also works but has not been recommended since 1.17.0.
- A proxied server can set the rate with the `X-Accel-Limit-Rate` response header; `proxy_ignore_headers X-Accel-Limit-Rate` disables that.
- `proxy_limit_rate rate;` (1.7.7, default `0`) limits the speed of reading the response from the proxied server, per request, and works only if proxy buffering is enabled.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_core_module` page (`limit_rate`, `limit_rate_after`) and `ngx_http_proxy_module` (`proxy_limit_rate`, `proxy_ignore_headers`). Removed: HTTP/2 per-stream claim (which carried a confirm marker), advice about `limit_conn`, worker connections and `sendfile_max_chunk`, and the curl Verify step.
Method: documentation only; no commands were run.
