---
id: computing-software.networking-hardware-and-wireless.apache-httpd.proxy-headers-and-preserve-host
name: proxy-headers-and-preserve-host
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy, proxypreservehost, x-forwarded-for, proxyaddheaders, host-header]
level: practitioner
status: docs-checked
description: "Control which headers the proxy sends to backends: ProxyPreserveHost, ProxyAddHeaders and the X-Forwarded-* headers, plus ProxyPassReverse redirect rewriting."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy.html
  - https://httpd.apache.org/docs/2.4/urlmapping.html
  - https://httpd.apache.org/docs/2.4/mod/mod_remoteip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy headers and ProxyPreserveHost
## ProxyPreserveHost
`Off` by default. `On` forwards the client's `Host:` header to the backend, useful for mass name-based virtual hosting.

## ProxyAddHeaders
Default `On`. Adds `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Server`. With several proxies the values are appended comma-separated, so verify them on the origin.

## Redirects and cookies
`ProxyPassReverse` rewrites `Location`, `Content-Location` and `URI`. Links inside documents are not rewritten; urlmapping.html suggests `mod_substitute`:
```apache
Substitute "s/internal\.example\.com/www.example.com/i"
```
`ProxyPassReverseCookieDomain` / `ProxyPassReverseCookiePath` adjust cookies.

## Via and bodies
`ProxyVia` controls the Via header. `proxy-sendcl` forces Content-Length; `proxy-sendchunked` uses chunked encoding for request bodies.

## Real client address on the backend
Use mod_remoteip on the backend with `RemoteIPHeader X-Forwarded-For` and a trusted proxy list (`RemoteIPTrustedProxy`); without one, mod_remoteip trusts every host that sends the header.

## Checked

2026-11-08. ProxyPreserveHost and ProxyAddHeaders defaults, the three X-Forwarded-* headers and comma-separated values, ProxyPassReverse header list, cookie directives, mod_substitute example, proxy-sendcl and proxy-sendchunked, ProxyVia, and RemoteIPHeader trust behaviour confirmed against the mod_proxy, urlmapping and mod_remoteip pages.

Method: documentation only; no commands were run.
