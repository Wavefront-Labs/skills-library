---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.health-monitors
name: health-monitors
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, monitors, http-monitor, send-receive, https-monitor]
level: practitioner
status: draft
description: "Create HTTP/HTTPS/TCP/external BIG-IP monitors with correct send/receive strings, intervals and timeouts, and read monitor failures."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Health monitors

```
tmsh create ltm monitor http mon_app defaults-from http send "GET /healthz HTTP/1.1\r\nHost: app.example.com\r\nConnection: close\r\n\r\n" recv "200 OK" interval 5 timeout 16
tmsh modify ltm pool pool_web monitor mon_app
tmsh create ltm monitor tcp mon_tcp interval 5 timeout 16
tmsh create ltm monitor https mon_tls cipherlist DEFAULT:+SHA:+3DES:+kEDH ssl-profile serverssl
tmsh show ltm monitor http mon_app
```
- Rule of thumb: `timeout = 3 x interval + 1`. The monitor must see 3 consecutive timeouts of the interval to mark down.
- `recv` is a regex matched against the response; add `recv-disable` to mark the member `disabled` (not down) for a "maintenance" reply.
- `reverse` flips the logic (mark down on match); `transparent` sends probes through the member to a destination elsewhere (firewall monitoring).
- Self IP source: probes originate from the self IP on the member's VLAN (or the mgmt route if none). Backend ACLs must permit that address. Floating self IPs are not used for probes.
- A passing TCP monitor does not mean the application works; use HTTP monitors with a real URI and `Host:` header.
- Gotcha: `HTTP/1.1` without a `Host:` header often gets a 400 from the backend, and the pool shows red. Use `\r\n\r\n` terminators exactly.

Verify: `tmsh show ltm pool pool_web members` shows Mon status; `tail -f /var/log/ltm` prints "Pool member ... monitor status down. [ /Common/mon_app: down; last error: /Common/mon_app: Response Code: 503 ...]".
