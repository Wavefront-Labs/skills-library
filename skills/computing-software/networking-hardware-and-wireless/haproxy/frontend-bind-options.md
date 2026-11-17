---
id: computing-software.networking-hardware-and-wireless.haproxy.frontend-bind-options
name: frontend-bind-options
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, bind-line, bind-options, reuseport, defer-accept, so-reuseport]
level: practitioner
status: docs-checked
description: "Bind HAProxy listeners with address, port, ssl, alpn, interface, defer-accept, transparent and thread options."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# frontend bind options
The `bind` line defines listeners: `bind <address>:<port> [options]`. Several `bind` lines may share one frontend.

```
frontend fe_web
    bind 192.0.2.10:80
    bind [2001:db8::10]:443 v6only ssl crt /etc/haproxy/certs/site.pem alpn h2,http/1.1
    bind /run/haproxy/internal.sock mode 660 user haproxy
    bind :8443 ssl crt /etc/haproxy/certs/ ca-file /etc/haproxy/ca.pem verify required
```
Options: `ssl` with `crt` enables TLS; `alpn` advertises protocols (ALPN is required for HTTP/2 on an HTTPS frontend; with none of `npn`, `alpn` or `no-alpn` set, `h2,http/1.1` is the default, and `alpn h2` alone refuses HTTP/1.1); `ssl-min-ver TLSv1.2`, `ciphers` and `ciphersuites` pin the protocol and ciphers; `verify required` plus `ca-file` is mutual TLS; `accept-proxy` enforces a PROXY header on every connection from that line (restrict it with `tcp-request connection expect-proxy` for finer control); `transparent` binds addresses that are not local (needs a build with `USE_LINUX_TPROXY=1`, normally IP forwarding, and never use it with `*`); `interface eth1` restricts the socket to a device (Linux, needs root); `thread <set>` limits which threads run the listener; `defer-accept` accepts a connection only when data arrives (Linux, for protocols where the client talks first such as HTTP); `v6only`/`v4v6` choose IPv6-only or dual-stack for the default address; `mode`, `user` and `uid` set permissions and owner of UNIX sockets. SO_REUSEPORT is used unless disabled by the global `noreuseport`.

Gotcha: binding an address the node does not own (for example a VRRP virtual IP on the backup) is rejected by the system; on Linux set `net.ipv4.ip_nonlocal_bind=1`, as the management guide advises, rather than delaying the service start.

Verify: `haproxy -c -f <config>` accepts the bind line; check the listeners with the OS socket list and, for `alpn`, a client that reports the negotiated protocol.

## Checked
2026-11-03. Confirmed against configuration.html bind options (`accept-proxy`, `alpn`, `defer-accept`, `interface`, `thread`, `transparent`, `user`, `v6only`, `v4v6`, `ssl-min-ver`, `ca-file`, `verify`, global `noreuseport`) and management.html (`ip_nonlocal_bind`). Removed: "transparent needs CAP_NET_ADMIN", the "since 2.x SO_REUSEPORT default confirm" marker (now stated via `noreuseport`), `freebind`, "ports below 1024 need root", and the `ss`/`openssl s_client` verify commands. The description no longer lists `reuseport` as a bind option.
Method: documentation only; no commands were run.
