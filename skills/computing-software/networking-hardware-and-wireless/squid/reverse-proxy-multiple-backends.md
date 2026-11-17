---
id: computing-software.networking-hardware-and-wireless.squid.reverse-proxy-multiple-backends
name: reverse-proxy-multiple-backends
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, reverse-proxy, multiple-backends, cache-peer-access, dstdomain]
level: practitioner
status: docs-checked
description: "Route requests for different domains to different origin servers using named cache_peer lines and cache_peer_access."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Reverse/MultipleWebservers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple backend web servers
```
cache_peer ip.of.server1 parent 80 0 no-query originserver name=server_1
acl sites_server_1 dstdomain www.example.com example.com
cache_peer_access server_1 allow sites_server_1

cache_peer ip.of.server2 parent 80 0 no-query originserver name=server_2
acl sites_server_2 dstdomain www.example.net download.example.com .example.net
cache_peer_access server_2 allow sites_server_2
```
`name=` gives each backend an identifier the access rules use. The older `cache_peer_domain` was deprecated in Squid 3.2 and removed in Squid 4.

## Checked

2026-11-04. Read the ConfigExamples/Reverse/MultipleWebservers wiki page and confirmed the example, name= use and the cache_peer_domain deprecation in 3.2 and removal in 4. Removed the claim about a leading dot matching subdomains, which the page does not state.

Method: documentation only; no commands were run.
