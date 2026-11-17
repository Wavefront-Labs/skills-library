---
id: computing-software.cloud-infrastructure-engineering.nginx.stub-status
name: stub-status
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, stub-status, metrics, active-connections, monitoring]
level: practitioner
status: docs-checked
description: "Exposing nginx stub_status for connection counters, what each field means, and restricting access with allow and deny."
sources: ["https://nginx.org/en/docs/http/ngx_http_stub_status_module.html", "https://nginx.org/en/docs/http/ngx_http_access_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`ngx_http_stub_status_module` is not built by default; it needs `--with-http_stub_status_module`. `stub_status;` goes in a `server` or `location`.

```nginx
server {
    listen 127.0.0.1:8081;
    location = /nginx_status {
        stub_status;
        allow 127.0.0.1;
        deny all;
    }
}
```

Sample output from the module page:

```
Active connections: 291
server accepts handled requests
 16630948 16630948 31070465
Reading: 6 Writing: 179 Waiting: 106
```

- Active connections: current active client connections including Waiting.
- accepts / handled / requests: totals of accepted connections, handled connections and client requests. `handled` normally equals `accepts` unless a resource limit such as `worker_connections` was reached.
- Reading: connections where nginx is reading the request header. Writing: connections where nginx is writing the response. Waiting: idle client connections waiting for a request.
- Embedded variables (1.3.14): `$connections_active`, `$connections_reading`, `$connections_writing`, `$connections_waiting`.
- Before 1.7.5 the directive needed an argument (`stub_status on;`).
- `allow` / `deny` (ngx_http_access_module) take an address, CIDR, `unix:` or `all`.

## Checked
Date: 2026-11-03.
Confirmed in the stub_status and access module pages: all of the above.
Removed as unconfirmed: nginx-prometheus-exporter usage, the "alert on rates" advice, the open-source metrics limitation, the `access_log off` line, and the curl verify step.
Method: documentation only; no commands were run.
