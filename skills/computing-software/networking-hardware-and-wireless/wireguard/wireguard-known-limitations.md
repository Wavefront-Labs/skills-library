---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-known-limitations
name: wireguard-known-limitations
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wireguard-limitations, tcp-mode, obfuscation, udp2raw, udptunnel, identity-hiding, system-time, roaming]
level: advanced
status: docs-checked
description: "Know what WireGuard deliberately does not do: no TCP, no obfuscation, time-sensitive counters, roaming caveats."
sources: ["https://www.wireguard.com/known-limitations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard known limitations

Documented trade-offs, with the mitigations the project names:
- **Deep packet inspection**: no built-in obfuscation; do it in a layer above.
- **TCP**: tunnelling over TCP is explicitly unsupported because TCP-over-TCP performs badly. A wrapper such as udptunnel or udp2raw can turn the UDP packets into TCP at a higher layer.
- **Hardware crypto**: ChaCha20Poly1305 is fast in software; vector instructions are comparable to AES-NI.
- **Roaming**: updates happen with no extra round trip, so an active man in the middle can replace source IPs. Packets stay indecipherable; lock the socket to a known address with ordinary firewalling if this matters.
- **Identity hiding forward secrecy**: the sender public key is encrypted to the responder's static key, so a compromised responder key plus handshake logs reveals who sent handshakes (not the data). Rotate keys.
- **Post-quantum**: not default; use the preshared key slot (see wireguard-preshared-keys-and-post-quantum).
- **Denial of service**: mac1/mac2 protect, though ECDH before mac2 may cost CPU.
- **System time**: used as a monotonic counter. A forward jump can lock your own keys out; a backward jump breaks handshakes; an adversary controlling the clock can replay a stored initiation. The page says the system time should not be under the control of a hostile adversary.
- **Routing loops**: detection is imperfect; avoid routing the endpoint through the tunnel (see wireguard-full-tunnel-routing-fwmark-method).

Verify: for TCP-only networks, test your chosen wrapper end to end, since WireGuard itself will not do it.

## Checked

2026-11-03. Confirmed: Every listed limitation (DPI, TCP mode with udptunnel/udp2raw, hardware crypto, roaming, identity-hiding forward secrecy, post-quantum, DoS, system-time counter, routing loops) against the known-limitations page. Removed: the NTP advice.

Method: documentation only; no commands were run.
