---
id: computing-software.networking-hardware-and-wireless.apache-httpd.forward-proxy-and-security
name: forward-proxy-and-security
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy, forward-proxy, proxyrequests, proxyvia, connect, proxyremote]
level: advanced
status: docs-checked
description: "Run a forward proxy safely: ProxyRequests, locking down Proxy sections, CONNECT matching limits, ProxyVia, ProxyRemote and NoProxy for intranets."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forward proxy and its security
Clients must be configured to use a forward proxy, which is enabled with `ProxyRequests On`.

```apache
ProxyRequests On
ProxyVia On
<Proxy "*">
  Require host internal.example.com
</Proxy>
```
Warning from the docs: do not enable `ProxyRequests` until the server is secured; open proxies endanger your network and the Internet.

## Access control
- `<Proxy "*">` applies to all requests including CONNECT tunnels.
- CONNECT matching uses only host and port, so path-based rules do not work.
- `<Proxy>` and `<ProxyMatch>` do not canonicalise URLs: deny by default and allow expected hosts.

## ProxyVia
`Off` (default), `On` adds a Via line, `Full` adds the server version, `Block` removes Via headers.

## Intranet routing
Use `ProxyRemote`, `NoProxy` and `ProxyDomain` to send external traffic through a firewall proxy and serve internal hosts directly. With `ProxyRemote`, DNS lookups happen only at the remote proxy, so `ProxyBlock` IP rules belong there.

## Modules
`mod_proxy_connect` handles HTTPS via CONNECT; `mod_proxy_ftp` handles FTP.

## Checked

2026-11-08. ProxyRequests activation and warning, the Proxy wildcard and CONNECT host-and-port matching, no canonicalisation in Proxy and ProxyMatch, ProxyVia modes and default, NoProxy, ProxyDomain, ProxyRemote DNS note and ProxyBlock placement, and the protocol module table confirmed against the mod_proxy page.

Method: documentation only; no commands were run.
