---
id: computing-software.networking-hardware-and-wireless.bind9.cookies-and-edns
name: cookies-and-edns
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dns-cookies, edns-udp-size, send-cookie]
level: advanced
status: docs-checked
description: "BIND 9 DNS cookie and EDNS settings: cookie-algorithm, require-server-cookie, answer-cookie, send-cookie, edns-udp-size."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cookies and edns
Server cookie options in `options`:

- `cookie-algorithm`: `siphash24` is the only supported value.
- `require-server-cookie`: if `yes`, a cookie-aware client without a valid server cookie gets BADCOOKIE rather than a full response over UDP. Default `no`.
- `answer-cookie`: default `yes`; `no` is a temporary measure when a shared IP address serves other servers without cookie support. Global only, not per view.
- `send-cookie`: whether a COOKIE option is sent along with queries; can be turned off per remote server in a `server` block.

`edns-udp-size` is the maximum advertised EDNS UDP buffer, 512 to 4096, default 1232. Lower it only to get answers through firewalls that drop fragments.

## Checked

2026-11-04. Read the cookie-algorithm, require-server-cookie, answer-cookie, send-cookie and edns-udp-size entries in the Administrator Reference Manual; defaults and range confirmed. Nothing was removed.

Method: documentation only; no commands were run.
