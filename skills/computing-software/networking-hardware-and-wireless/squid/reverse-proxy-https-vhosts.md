---
id: computing-software.networking-hardware-and-wireless.squid.reverse-proxy-https-vhosts
name: reverse-proxy-https-vhosts
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, reverse-proxy, https-port, tls-cert, virtual-hosts]
level: advanced
status: docs-checked
description: "Serve several HTTPS domains from one accelerator with https_port accel and one tls-cert per domain."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Reverse/HttpsVirtualHosting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTPS virtual hosting
Needs Squid 4 or newer built with GnuTLS; OpenSSL builds cannot do this.
```
https_port 443 accel defaultsite=example.net \
  tls-cert=/path/to/example.net.pem \
  tls-cert=/path/to/example.com.pem
cache_peer backend.webserver.ip.or.dnsname parent 80 0 no-query originserver name=myAccel
acl our_sites dstdomain your.main.website.name
http_access allow our_sites
cache_peer_access myAccel allow our_sites
cache_peer_access myAccel deny all
```
`defaultsite` serves clients that omit the Host header; without it they get an Invalid request error. Each `tls-cert` file holds one domain's certificate, key and intermediate CAs; only the first domain in a file is used.

## Checked

2026-11-04. Read the ConfigExamples/Reverse/HttpsVirtualHosting wiki page and confirmed the Squid 4 and GnuTLS requirement, the defaultsite behaviour, the tls-cert file contents and the first-domain-only rule. Nothing was removed.

Method: documentation only; no commands were run.
