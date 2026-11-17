---
id: computing-software.networking-hardware-and-wireless.squid.dns-and-hostname
name: dns-and-hostname
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, dns-nameservers, visible-hostname, resolver]
level: intro
status: docs-checked
description: "Point Squid at specific DNS servers with dns_nameservers and set the hostname it shows with visible_hostname."
sources:
  - https://www.squid-cache.org/Doc/config/dns_nameservers/
  - https://www.squid-cache.org/Doc/config/visible_hostname/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS servers and visible hostname
`dns_nameservers` lists DNS server IPs to use instead of the system resolver configuration. Default: use operating system definitions.
```
dns_nameservers 10.0.0.1 192.172.0.4
```
On Windows, if none are set here or in resolv.conf, Squid takes them from the registry.

`visible_hostname` sets the hostname shown in places such as error messages. Default: auto-detected system host name. Give each cache in a cluster its own name if you see forwarding-related errors.

## Checked

2026-11-04. Read the dns_nameservers and visible_hostname directive pages and confirmed the defaults, the example, the Windows registry note and the cluster naming advice. Nothing was removed.

Method: documentation only; no commands were run.
