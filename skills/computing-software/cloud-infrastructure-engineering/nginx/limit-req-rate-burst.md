---
id: computing-software.cloud-infrastructure-engineering.nginx.limit-req-rate-burst
name: limit-req-rate-burst
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, limit-req, limit-req-zone, burst, nodelay, rate-limiting]
level: practitioner
status: docs-checked
description: "Rate limiting requests in nginx with limit_req_zone and limit_req: leaky bucket, burst, nodelay, delay, status code and dry run."
sources: ["https://nginx.org/en/docs/http/ngx_http_limit_req_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`limit_req_zone key zone=name:size rate=rate;` (context `http`) defines the zone; `limit_req zone=name [burst=number] [nodelay | delay=number];` (contexts `http`, `server`, `location`) applies it. The module uses the leaky bucket method.

```nginx
limit_req_zone $binary_remote_addr zone=perip:10m rate=10r/s;
server {
    location /login/ {
        limit_req zone=perip burst=20 nodelay;
        limit_req_status 429;
        limit_req_log_level warn;
    }
}
```

- The rate is in requests per second (`r/s`); for less than one per second use `r/m` (30r/m is half a request per second).
- Excess requests are delayed so that processing stays at the configured rate, until their number exceeds `burst`, after which the request is terminated with an error. The default burst is zero.
- `nodelay` serves excess requests within the burst without delaying them. `delay=number` (1.15.7) sets the point at which excess requests start being delayed; the default is zero, so all excess requests are delayed.
- `limit_req_status` default is `503`; `limit_req_log_level` default is `error`, and delays are logged one level lower than refusals.
- `limit_req_dry_run on` (1.17.1) accounts for excess requests in the zone without limiting.
- `$binary_remote_addr` is 4 bytes (IPv4) or 16 bytes (IPv6); one megabyte of zone keeps about 16 thousand 64-byte or 8 thousand 128-byte states. When the zone is full the least recently used state is removed; if no state can then be created the request is terminated with an error. Requests with an empty key are not accounted.
- Several `limit_req` directives may apply together (for example per IP and per server). They are inherited only if the current level defines none.
- `$limit_req_status` is `PASSED`, `DELAYED`, `REJECTED`, `DELAYED_DRY_RUN` or `REJECTED_DRY_RUN`.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_limit_req_module` page. Removed: the "one request per 100 ms" interval arithmetic, the "confirm" marker on zone capacity (now stated from the page), realip and proxy advice, and the curl loop Verify step.
Method: documentation only; no commands were run.
