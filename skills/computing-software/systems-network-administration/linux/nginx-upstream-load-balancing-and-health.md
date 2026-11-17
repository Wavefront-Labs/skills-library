---
id: computing-software.systems-network-administration.linux.nginx-upstream-load-balancing-and-health
name: nginx-upstream-load-balancing-and-health
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, upstream-load-balancing, nginx-upstream, least-conn, max-fails, haproxy, keepalive-upstream]
level: practitioner
status: verified
description: "Load balance with nginx upstream blocks: round robin, least_conn, ip_hash, weights, passive health via max_fails, backup servers, upstream keepalive and Apache mod_proxy_balancer."
sources:
  - https://github.com/nginx/nginx.org/blob/main/xml/en/docs/http/ngx_http_upstream_module.xml
  - https://github.com/nginx/nginx.org/blob/main/xml/en/docs/http/ngx_http_proxy_module.xml
  - https://github.com/apache/httpd/blob/trunk/docs/manual/mod/mod_proxy.xml
  - https://github.com/apache/httpd/blob/trunk/docs/manual/mod/mod_proxy_hcheck.xml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Upstream load balancing and health

## nginx upstream
```nginx
upstream app {
    least_conn;                                  # or: (default round robin) | ip_hash | hash $cookie_sid consistent
    server 10.0.0.11:8080 weight=2 max_fails=3 fail_timeout=10s;
    server 10.0.0.12:8080 max_fails=3 fail_timeout=10s;
    server 10.0.0.13:8080 backup;                # used only when all primaries are down
    server 10.0.0.14:8080 down;                  # drained
    keepalive 32;                                # max idle upstream connections cached per worker (default 32 local since nginx 1.29.7)
}
server {
    listen 443 ssl;
    location / {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Connection "";           # clear the Connection header so keepalive works; proxy_http_version 1.1 is the default only since 1.29.7
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_next_upstream error timeout http_502 http_503;
        proxy_next_upstream_tries 2;
        proxy_connect_timeout 2s;
        proxy_read_timeout 30s;
    }
}
```

## Health checking in open-source nginx is passive
- A server is considered unavailable after `max_fails` unsuccessful attempts within `fail_timeout`, and then stays unavailable for `fail_timeout` (defaults: `max_fails=1`, `fail_timeout=10s`; `max_fails=0` disables the accounting). What counts as unsuccessful is defined by `proxy_next_upstream` (default `error timeout`).
- Active probes (`health_check` directive, `ngx_http_upstream_hc_module`) are part of the commercial subscription (NGINX Plus). For open source use HAProxy, Envoy, or an external checker that edits the upstream and reloads.
- With `proxy_next_upstream` a request with a non-idempotent method (such as POST) is not passed to the next server once it has been sent, unless you add `non_idempotent`; leave it off to avoid duplicate orders.
- `backup` cannot be combined with the `hash`, `ip_hash` and `random` methods.

## Choosing the method
| Method | When |
|---|---|
| round robin | stateless, uniform requests |
| least_conn | long or uneven requests (uploads, websockets) |
| ip_hash / hash consistent | sticky sessions without shared session store; consistent hashing for caches |

## DNS-named servers
nginx resolves `server app.internal:8080` once at startup. For changing IPs (containers, cloud), use `resolver 10.0.0.2 valid=10s;` with a variable in `proxy_pass`, or the `resolve` parameter on `server` (open source since 1.27.3; before that commercial subscription only). `resolve` needs a `resolver` in the http block or the upstream block and the upstream group in a shared-memory `zone`:
```nginx
upstream app { zone app 64k; resolver 10.0.0.2; server app.internal:8080 resolve; }
```

## Apache equivalent
```apache
<Proxy balancer://app>
    BalancerMember http://10.0.0.11:8080 retry=10
    BalancerMember http://10.0.0.12:8080 retry=10
    BalancerMember http://10.0.0.13:8080 status=+H        # hot standby
    ProxySet lbmethod=bybusyness
</Proxy>
ProxyPass "/" "balancer://app/"
```
`mod_proxy_hcheck` adds active checks (`hcmethod=GET hcuri=/health`).

## Verify
- [ ] Stop one backend: requests keep succeeding; the error log shows upstream errors, then no further traffic goes to it until `fail_timeout` passes.
- [ ] `ss -tn state established dst 10.0.0.11` shows reused connections when keepalive is on.

## Checked

Checked 2026-10-26 against nginx/nginx.org (last commit 2026-10-21: ngx_http_upstream_module.xml and ngx_http_proxy_module.xml) and apache/httpd docs (mod_proxy.xml, mod_proxy_hcheck.xml, mod_lbmethod_bybusyness.xml; last commit 2026-10-25). Confirmed: max_fails and fail_timeout semantics and defaults (1 and 10 s), backup and down parameters and the backup restriction, hash consistent, keepalive and the 1.29.7 default change, proxy_http_version default change, resolve parameter (open source since 1.27.3, needs resolver and a zone), non_idempotent, health_check being commercial, Apache BalancerMember status=+H, retry, bybusyness and hcmethod/hcuri. Corrected: resolve requires the upstream group in a shared-memory zone.

Run 2026-11-01 on nginx 1.30.6 (Windows, 127.0.0.1 only): the upstream block (`least_conn`, `weight`, `max_fails`, `fail_timeout`, `backup`, `down`, `keepalive 32`) and the proxy location pass `nginx -t` and balance requests across the two live servers with the backup unused; `ip_hash` plus a `backup` server fails with `balancing method does not support parameter "backup"`; `hash $cookie_sid consistent` and `ip_hash` pass; `server ... resolve` without a `zone` fails with `resolving names at run time requires upstream "u" ... to be in shared memory`, and with `zone app2 64k` plus `resolver` it passes. Not run: Apache mod_proxy_balancer (no Apache binary; documentation only), failover timing, `ss` keepalive reuse and the NGINX Plus `health_check`.
