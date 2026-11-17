---
id: computing-software.networking-hardware-and-wireless.squid.intercept-linux-redirect
name: intercept-linux-redirect
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, intercept, iptables, redirect, nat]
level: advanced
status: docs-checked
description: "Intercept port 80 traffic on the Squid machine itself with an intercept http_port and iptables REDIRECT rules."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Intercept/LinuxRedirect
  - https://www.squid-cache.org/Doc/config/http_port/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interception with REDIRECT
```
http_port 3129 intercept
```
```
iptables -t nat -A PREROUTING -s $SQUIDIP -p tcp --dport 80 -j ACCEPT
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port $SQUIDPORT
iptables -t nat -A POSTROUTING -j MASQUERADE
iptables -t mangle -A PREROUTING -p tcp --dport $SQUIDPORT -j DROP
```
Caveats from the page:
- NAT works only when run on the Squid machine; for a separate gateway use policy routing.
- The first NAT rule (exempting Squid itself) must come first to avoid forwarding loops.
- Block outside access to the intercept port in the mangle table, before NAT.
- Squid 3.1 and later use `intercept`, not `transparent`.
- Authentication is disabled on intercept ports.

## Checked

2026-11-04. Read the Intercept/LinuxRedirect wiki page and confirmed the configuration steps. Nothing was removed.

Method: documentation only; no commands were run.
