---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-with-proxies
name: pjsip-with-proxies
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, proxy, outbound-proxy, kamailio, itsp, identify]
level: advanced
status: docs-checked
description: "Configure PJSIP when an outbound proxy sits between Asterisk and an ITSP: transport, endpoint, aor, registration and identify settings, and the lr parameter."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-with-Proxies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip with proxies
Scenario: Asterisk on the same private network as the phones, using an outbound proxy to reach an ITSP that requires registration.

- `transport`: do not set `external_signalling_address`, `external_media_address` or `local_net`; Asterisk should not know what is beyond the proxy.
- `endpoint`: configure the ITSP as usual and add `outbound_proxy = sip:192.168.0.1\;lr` (the proxy internal address). Do not enable NAT options such as `force_rport` or `ice_support`.
- `aor`: add the same `outbound_proxy` so OPTIONS qualify requests go via the proxy; keep `contact` as without a proxy.
- `registration`: keep `client_uri` and `server_uri` as without a proxy and add `outbound_proxy`.
- `identify`: most ITSPs do not authenticate calls to clients and may send the caller ID as the From user, so identify by IP: `match = 192.168.0.1` (the proxy), `endpoint = myitsp`.

Without the `lr` parameter you will probably get a 404 from the proxy, because most proxies follow RFC 3261 loose routing. The backslash before the semicolon keeps it from starting a comment in the config file.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP with Proxies page: transport, endpoint, aor, registration and identify settings and the lr parameter. Replaced the claim that the page covers lr in detail with what it states (404 without lr, backslash escape).
Method: documentation only; no commands were run.
