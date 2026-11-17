---
id: computing-software.collaboration-platform-administration.matrix-synapse.turn-server-voip-setup-and-troubleshooting
name: turn-server-voip-setup-and-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, turn, voip, coturn, eturnal, webrtc, turn-uris, turn-shared-secret, nat]
level: advanced
status: docs-checked
description: "Connect Synapse to a TURN server for calls: turn_uris, turn_shared_secret, lifetime and guests, firewall and relay ports, IPv6 and NAT traps, and test tools."
sources:
  - https://element-hq.github.io/synapse/latest/turn-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse integrates with a TURN server through the TURN REST API: the homeserver generates credentials valid on the TURN server using a secret shared between them. The docs give coturn and eturnal setup pages. The TURN service needs a public IP; behind NAT it needs port forwarding and a public IP on the gateway, and even then NAT often causes problems.

Add four keys to `homeserver.yaml`: `turn_uris`, `turn_shared_secret`, `turn_user_lifetime` and `turn_allow_guests`. The matrix.org example uses `turn_uris: [ "turn:turn.matrix.org?transport=udp", "turn:turn.matrix.org?transport=tcp" ]` for default ports with no TLS, `turn_user_lifetime: 86400000` and `turn_allow_guests: true`. Use your own secret, not a sample. Restart Synapse (`synctl restart` or `systemctl restart matrix-synapse.service`), then reload clients or wait up to an hour for them to refresh.

**Symptom of a bad setup:** calls between devices on different networks ring but stick at "call connecting". Checks from the docs:

- Open the firewall for TCP and UDP on the TURN ports (normally 3478 and 5349) and UDP on the relay ports (49152-65535 by default).
- Temporarily disable TLS/DTLS listeners and use only plain TCP/UDP; only signalling becomes unencrypted, since WebRTC media is always encrypted.
- Chrome can be confused by TURN servers reachable over IPv6; try removing AAAA records so the server is IPv4 only.
- Behind NAT, forward all TURN and relay ports to the internal address, make the TURN server use the NAT gateway as its default route, and when in doubt drop AAAA records and set only an IPv4 `external-ip`.
- Turn on verbose logging (`verbose` in coturn, `eturnalctl loglevel debug` in eturnal).
- Inspect negotiation with `chrome://webrtc-internals/` or Firefox `about:webrtc`.

Test tools: the voip tester at test.voip.librepush.net (not fully reliable) and the WebRTC trickle-ICE sample page, which needs a username and password. Get them from the `GET /_matrix/client/r0/voip/turnServer` response a client makes, or compute them for coturn with an HMAC-SHA1 of `<expiry>:test` using the shared secret, or run `eturnalctl credentials`. A working server shows at least one `relay` result.

## Checked

2026-11-04. Confirmed against the Synapse TURN howto page: requirements, four config keys and matrix.org example, restart steps, symptom, firewall ports, IPv6 and NAT advice, logging, webrtc-internals, test tools and credential methods. Removed the unit label on turn_user_lifetime (not stated on the page).
Method: documentation only; no commands were run.
