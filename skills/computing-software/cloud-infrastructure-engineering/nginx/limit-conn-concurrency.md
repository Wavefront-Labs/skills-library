---
id: computing-software.cloud-infrastructure-engineering.nginx.limit-conn-concurrency
name: limit-conn-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, limit-conn, limit-conn-zone, concurrent-connections, slowloris]
level: practitioner
status: docs-checked
description: "Capping concurrent connections per key with limit_conn_zone and limit_conn: counting rules, zone size, status code, dry run and log level."
sources: ["https://nginx.org/en/docs/http/ngx_http_limit_conn_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`limit_conn_zone key zone=name:size;` (context `http`) defines a shared memory zone; `limit_conn zone number;` (contexts `http`, `server`, `location`) sets the maximum connections per key value. Requests with an empty key are not accounted.

```nginx
limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name        zone=perserver:10m;

server {
    limit_conn perip 10;
    limit_conn perserver 100;
    limit_conn_status 429;
}
```

- A connection is counted only if it has a request being processed and the whole request header has been read.
- In HTTP/2 and HTTP/3 each concurrent request counts as a separate connection.
- Several `limit_conn` directives can apply at once (per IP and per virtual server in the example). They are inherited only if the current level defines none.
- `$binary_remote_addr` is 4 bytes for IPv4 and 16 bytes for IPv6, and the stored state is 64 bytes on 64-bit platforms; a 1 MB zone holds about 16 thousand 64-byte states. If the zone is exhausted the server returns the error to all further requests.
- `limit_conn_status` (default `503`, 1.3.15) sets the rejection code; `limit_conn_log_level` (default `error`) sets the log level; `limit_conn_dry_run on` (1.17.6) counts without limiting.
- `$limit_conn_status` holds `PASSED`, `REJECTED` or `REJECTED_DRY_RUN`.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_limit_conn_module` page. Removed: slowloris claims, NAT and CDN advice, the `client_*_timeout` values (they live on the core module page), the ab Verify step and the error log text.
Method: documentation only; no commands were run.
