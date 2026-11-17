---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-ipv6
name: pjsip-ipv6
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, ipv6, transport, bind, rtp]
level: intro
status: docs-checked
description: "Make res_pjsip speak IPv6 by binding transports to an IPv6 address or :: and understanding how RTP follows the signaling address family."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-res_pjsip-for-IPv6/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip ipv6
Configuration is in transport and endpoint sections of `pjsip.conf`.

- Bind to a specific address with brackets: `bind=[fe80::5e26:aff:fe4b:4399]` on a `type=transport` section (create one per protocol, e.g. `protocol=udp` and `protocol=tcp`).
- Bind to the first available IPv6 interface with `bind=::`.
- RTP needs no extra setting: IPv4 or IPv6 is chosen from the address family used for signaling.
- Point the endpoint at the IPv6 transport with `transport=<name>`.

Transport selection details are on the transport-selection page.

## Checked

2026-11-09. Confirmed against the Asterisk page on configuring res_pjsip for IPv6: bracketed bind, bind=:: for the first available IPv6 interface, RTP address family following signaling. Nothing changed.
Method: documentation only; no commands were run.
