---
id: computing-software.networking-hardware-and-wireless.apache-httpd.proxy-balancer-load-balancing
name: proxy-balancer-load-balancing
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy-balancer, load-balancing, balancermember, lbmethod, failover]
level: advanced
status: docs-checked
description: "Build a load-balanced backend pool with mod_proxy_balancer, BalancerMember, an lbmethod scheduler module and balancer:// URLs."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy_balancer.html
  - https://httpd.apache.org/docs/2.4/rewrite/avoid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancing with mod_proxy_balancer
Needs `mod_proxy`, `mod_proxy_balancer` and at least one scheduler module.

| Module | Algorithm |
|---|---|
| `mod_lbmethod_byrequests` | request counting |
| `mod_lbmethod_bytraffic` | weighted traffic |
| `mod_lbmethod_bybusyness` | pending requests |
| `mod_lbmethod_heartbeat` | heartbeat traffic |

The algorithm is the `lbmethod` value of the balancer definition.

```apache
<Proxy "balancer://mycluster">
    BalancerMember "http://192.168.1.50:80"
    BalancerMember "http://192.168.1.51:80"
</Proxy>
ProxyPass        "/test" "balancer://mycluster"
ProxyPassReverse "/test" "balancer://mycluster"
```

## Member settings
Worker parameters such as `timeout`, `retry`, `ttl` and `max` apply on `BalancerMember` (see the mod_proxy reference). The balancer page does not document `loadfactor`, status flags or failover detail.

## Environment variables exported
`BALANCER_NAME`, `BALANCER_WORKER_NAME`, `BALANCER_WORKER_ROUTE`, `BALANCER_SESSION_STICKY`, `BALANCER_SESSION_ROUTE`, `BALANCER_ROUTE_CHANGED`.

Balancing also works for FastCGI backends: `BalancerMember "fcgi://localhost:4000"`.

## Checked
2026-11-04. Confirmed against the mod_proxy_balancer and mod_proxy references: required modules, the four lbmethod modules, example configuration, exported environment variables, and the BalancerMember worker parameters named (timeout, retry, ttl, max). Nothing removed.
Method: documentation only; no commands were run.
