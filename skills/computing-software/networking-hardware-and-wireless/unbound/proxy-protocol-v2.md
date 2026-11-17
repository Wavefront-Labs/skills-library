---
id: computing-software.networking-hardware-and-wireless.unbound.proxy-protocol-v2
name: proxy-protocol-v2
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, proxy-protocol, proxyv2, proxy-protocol-port, load-balancer]
level: advanced
status: draft
description: "Accept PROXYv2 headers from a load balancer or proxy in front of Unbound with proxy-protocol-port, and know its limits."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/proxy.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# proxy protocol v2
Supported since 1.17.0, PROXY protocol version 2 only, for downstream connections only. It works over UDP and TCP and can carry any layer 7 protocol including encrypted ones; the header is sent once at the start of a TCP stream, or in every UDP packet. Both the proxy and Unbound must support it.

`proxy-protocol-port` marks a port where PROXYv2 headers are expected. It can sit alongside plain UDP/TCP and DNS-over-TLS ports.

```
server:
    interface: eth0
    proxy-protocol-port: 53
    interface-action: eth0 allow
```

Unbound drops a connection or packet that lacks a valid PROXYv2 header.

Cannot be combined with DNSCrypt or DNS over HTTP.

Address use: the topic page says network-level functions (access control, logging, DNSTAP, RPZ, IP rate limiting) use the actual connecting address, while the unbound.conf manual says the proxied address is used for those; check the version in use.
