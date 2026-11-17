---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-nat-traversal
name: pjsip-nat-traversal
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, nat, local-net, external-media-address, rtp-symmetric, force-rport, direct-media]
level: practitioner
status: docs-checked
description: "Configure res_pjsip behind NAT: local_net, external_media_address, external_signaling_address, direct_media, and per-endpoint rtp_symmetric, force_rport, rewrite_contact."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Configuring-res_pjsip-to-work-through-NAT/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip nat traversal
Scenario in the page: Asterisk and phones on a private network behind a router doing NAT and firewalling, with the router port-forwarding SIP (5060) and the RTP range (UDP 10000-20000) to the Asterisk host.

Transport options:
- `local_net`: networks treated as local; no NAT rewriting applies to traffic to them (the page example lists a private network and 127.0.0.1/32 on separate lines).
- `external_media_address`: address written into SDP when the destination is outside `local_net` and the SDP address is inside it.
- `external_signaling_address`: the same idea for SIP signaling. Keep the two equal unless media and signaling use different addresses.

Endpoint options:
- `direct_media=no` keeps Asterisk in the media path so the far end sends RTP to the public address.
- For remote phones behind NAT: `media_address` (address used in SDP), `rtp_symmetric` (send RTP back to the address and port it came from), `force_rport` (reply to the source port as if `rport` were present), `rewrite_contact` (send requests to the source address and port instead of the Contact).

Reference the NAT transport from the registration, endpoint and phones with `transport=`. The page defers ICE, STUN and TURN to a separate section and gives no examples.

## Checked

2026-11-09. Confirmed against the Asterisk page on configuring res_pjsip through NAT: scenario, local_net, external_media_address, external_signaling_address, direct_media and the remote-phone endpoint options. Removed the proxy sentence, which the page does not state.
Method: documentation only; no commands were run.
