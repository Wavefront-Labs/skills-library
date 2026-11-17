---
id: computing-software.networking-hardware-and-wireless.apache-httpd.reverse-proxy-proxypass
name: reverse-proxy-proxypass
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy, reverse-proxy, proxypass, proxypassreverse, proxypassmatch]
level: practitioner
status: docs-checked
description: "Configure a reverse proxy with ProxyPass, ProxyPassReverse and ProxyPassMatch: required modules, matching order, exclusions and cookie rewriting."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse proxy with ProxyPass
Load `mod_proxy` plus a protocol module (`mod_proxy_http`, `_fcgi`, `_ajp`, `_scgi`, `_uwsgi`, `_wstunnel`, `_http2`...). Keep `ProxyRequests Off` for reverse proxying.

```apache
ProxyPass "/foo" "http://foo.example.com/bar"
ProxyPassReverse "/foo" "http://foo.example.com/bar"
```

## Rules
- `ProxyPass` uses prefix matching; rules are checked in config order and the first match wins, so put longer URLs first.
- `ProxyPassReverse` rewrites `Location`, `Content-Location` and `URI` headers on redirects.
- `ProxyPassMatch` uses regex. Back-references create per-request URLs with no worker, so define an explicit worker for pooling:
```apache
ProxyPass        "/notused" "http://backend.example.com/" connectiontimeout=5 timeout=30
ProxyPassMatch   "^/(.*\.gif)$" "http://backend.example.com/$1"
```
- Exclude a path with `ProxyPass "/mirror/foo/i" "!"` placed before the general rule.
- `ProxyPassReverseCookieDomain` and `ProxyPassReverseCookiePath` rewrite `Set-Cookie` Domain and Path.

## Errors
`ProxyErrorOverride On [code ...]` (default `Off`) serves the proxy's own error pages instead of the backend's; with no codes it affects 400 up to but excluding 600. Example: `ProxyErrorOverride On 403 405 500 501 502 503 504`.

## Access
With a reverse proxy, clients reach only configured backends, so access control matters less than for a forward proxy.

## Checked

2026-11-08. Protocol modules, rule ordering, ProxyPassReverse headers, ProxyPassMatch worker note, exclusion with !, cookie directives, access-control note and ProxyErrorOverride syntax confirmed against the mod_proxy page. Replaced the ProxyErrorOverride example codes with the page's own.

Method: documentation only; no commands were run.
