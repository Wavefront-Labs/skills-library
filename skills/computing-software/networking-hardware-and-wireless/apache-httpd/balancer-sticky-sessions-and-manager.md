---
id: computing-software.networking-hardware-and-wireless.apache-httpd.balancer-sticky-sessions-and-manager
name: balancer-sticky-sessions-and-manager
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy-balancer, sticky-sessions, stickysession, balancer-manager, route]
level: advanced
status: docs-checked
description: "Pin clients to a backend with route and stickysession (cookie or URL), diagnose lost stickiness, and manage members live with balancer-manager."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy_balancer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sticky sessions and balancer-manager
## Stickiness
Give each member a `route`; `stickysession` names the cookie or URL parameter carrying it. mod_headers can set the cookie when the backend does not:
```apache
Header add Set-Cookie "ROUTEID=.%{BALANCER_WORKER_ROUTE}e; path=/" env=BALANCER_ROUTE_CHANGED
<Proxy "balancer://mycluster">
    BalancerMember "http://192.168.1.50:80" route=1
    BalancerMember "http://192.168.1.51:80" route=2
    ProxySet stickysession=ROUTEID
</Proxy>
```
Cookie and URL together: `stickysession=JSESSIONID|jsessionid scolonpathdelim=On`; the URL parameter wins. For Tomcat set `jvmRoute` to match the route; Apache uses the part after the dot.

## Debugging
Add to a `LogFormat`: `%{MYCOOKIE}C`, `%{Set-Cookie}o`, `%{BALANCER_SESSION_ROUTE}e`, `%{BALANCER_WORKER_ROUTE}e`, `%{BALANCER_ROUTE_CHANGED}e`. `LogLevel debug` gives detail but adds volume.

## Balancer manager
Changes member settings (such as balance factor) or takes members offline at runtime. Requires `mod_status`:
```apache
<Location "/balancer-manager">
    SetHandler balancer-manager
    Require host example.com
</Location>
```
Only balancers defined outside `<Location>` containers can be managed dynamically.

## Checked
2026-11-04. Confirmed against the mod_proxy_balancer reference: route and stickysession behaviour, mod_headers cookie example, cookie plus URL form with scolonpathdelim, Tomcat jvmRoute and dot handling, debugging LogFormat fields, balancer-manager requirements and Location restriction. Nothing removed.
Method: documentation only; no commands were run.
