---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-remoteip-behind-proxy
name: mod-remoteip-behind-proxy
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-remoteip, remoteipheader, trusted-proxy, proxy-protocol, client-ip]
level: practitioner
status: docs-checked
description: "Recover the real client IP behind a proxy or load balancer with mod_remoteip: trusted vs internal proxies, PROXY protocol, and effect on logging and Require ip."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_remoteip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_remoteip
Replaces the connection's client IP with the one a proxy reports in a header, for the request. Enable only for trusted intermediaries; the user agent can impersonate others.

```apache
RemoteIPHeader X-Client-IP
RemoteIPInternalProxy 10.0.2.0/24
```
```apache
RemoteIPHeader X-Forwarded-For
RemoteIPTrustedProxy 10.0.2.16/28
RemoteIPProxiesHeader X-Forwarded-By
```

## Directives
- `RemoteIPHeader` names the header; without proxy directives all presenters are trusted.
- `RemoteIPInternalProxy` trusts proxies to present any address, including private.
- `RemoteIPTrustedProxy` trusts these proxies to present public addresses only; private, loopback and link-local addresses they report are not trusted and stay in the header. `...List` variants read a file.
- `RemoteIPProxiesHeader` records intermediates.
- `RemoteIPProxyProtocol On|Off` and `RemoteIPProxyProtocolExceptions` (2.4.31+) require the HAProxy PROXY header.

Multiple addresses are processed right to left, stopping at the first one the previous proxy is not trusted to vouch for.

## Effects
- `%a` logs the overridden IP; `%{c}a` the underlying connection IP.
- `Require ip` uses the overridden address; `CONN_REMOTE_ADDR` gives the connection one.
- `%{remoteip-proxy-ip-list}n` logs the proxy list.

## Checked
2026-11-04. Confirmed against the mod_remoteip reference: header override and trust warning, directive semantics for InternalProxy, TrustedProxy and ProxiesHeader, PROXY protocol directives (2.4.31+), right-to-left processing, %a, %{c}a, CONN_REMOTE_ADDR, Require ip and the proxy list note. Tightened the TrustedProxy wording to match the page.
Method: documentation only; no commands were run.
