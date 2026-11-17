---
id: computing-software.networking-hardware-and-wireless.squid.reverse-proxy-accelerator
name: reverse-proxy-accelerator
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, reverse-proxy, accelerator, originserver, defaultsite]
level: practitioner
status: docs-checked
description: "Set up Squid as a basic website accelerator with http_port accel, an originserver cache_peer and access rules."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Reverse/BasicAccelerator
  - https://www.squid-cache.org/Doc/config/http_port/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic reverse proxy
Put the accelerator config at the top of squid.conf, above forward-proxy rules.
```
http_port 80 accel defaultsite=your.main.website.name no-vhost
cache_peer backend.webserver.ip.or.dnsname parent 80 0 no-query originserver name=myAccel
acl our_sites dstdomain your.main.website.name
http_access allow our_sites
cache_peer_access myAccel allow our_sites
cache_peer_access myAccel deny all
```
Steps: listen with `accel`, point `cache_peer` at the real server as `originserver`, allow your domain, and deny other requests to the peer. Test by editing a test machine's hosts file to the Squid IP before updating public DNS.

## Checked

2026-11-04. Read the ConfigExamples/Reverse/BasicAccelerator wiki page and confirmed the config block, the top-of-file placement, the option meanings and the hosts-file testing advice. Nothing was removed.

Method: documentation only; no commands were run.
