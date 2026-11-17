---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.tls-client-hello-sni-and-alpn-analysis
name: tls-client-hello-sni-and-alpn-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [tls-client-hello, sni, alpn, tls-handshake, ja4, network-forensics, dfir]
level: practitioner
status: verified
description: "Investigate encrypted traffic from the TLS handshake: SNI, ALPN, versions and cipher offers in ClientHello, ServerHello choices, certificates in TLS 1.2, ECH limits and fingerprinting."
sources: ["https://www.rfc-editor.org/rfc/rfc8446", "https://www.rfc-editor.org/rfc/rfc6066", "https://www.rfc-editor.org/rfc/rfc7301", "https://wiki.wireshark.org/TLS", "https://github.com/FoxIO-LLC/ja4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS ClientHello, SNI and ALPN analysis

Without keys you still get the handshake. The ClientHello is sent in clear (unless Encrypted Client Hello is used) and says which host the client wants, which application protocol, and what the client software supports.

## Fields and filters
```text
tls.handshake.type == 1                               # ClientHello
tls.handshake.extensions_server_name                  # SNI
tls.handshake.extensions_alpn_str                     # ALPN, e.g. h2, http/1.1
tls.handshake.extensions.supported_version            # offered versions (TLS 1.3 = 0x0304)
tls.handshake.ciphersuite                             # offered (ClientHello) / chosen (ServerHello)
tls.handshake.type == 2                               # ServerHello
tls.handshake.ja4                                     # JA4 (present in 4.4.1; 4.2.x release notes already fix JA4 bugs); ja3 / ja3s fields also available
```
Quick inventory:
```bash
tshark -r cap.pcapng -Y "tls.handshake.type==1" -T fields -e frame.time_utc -e ip.src -e ip.dst -e tls.handshake.extensions_server_name -e tls.handshake.extensions_alpn_str -e tls.handshake.ja4
```

## What to look for
- **No SNI** to an internet IP: common for malware connecting to raw IPs; browsers almost always send SNI.
- **SNI vs destination mismatch**: SNI for a big brand but the IP belongs to an unrelated hosting ASN (or domain fronting where HTTP Host differs; you only see that with decryption).
- **ALPN absent** where browsers would send `h2`: non-browser client claiming to be a browser in its User-Agent (if visible elsewhere).
- **Old versions / weak ciphers** offered: legacy or custom TLS stacks typical of malware or embedded devices.
- **Fingerprints** (JA3/JA4) matching known C2 frameworks or tools; cluster hosts by fingerprint to find others infected.
- **TLS 1.2 certificates** (in clear): self-signed, default framework certificates, short validity, odd issuer. In TLS 1.3 certificates are encrypted.

## Limits
- TLS 1.3 encrypts everything after ServerHello; QUIC carries TLS inside UDP (Wireshark decodes QUIC Initial packets to show the ClientHello).
- **ECH** (Encrypted Client Hello) hides the real SNI behind an outer SNI (the `public_name` of the client-facing server, e.g. a CDN's name; RFC 9849); expect it increasingly from browsers using DoH. Then the outer SNI is all you see.
- Fingerprints change with library versions; use them to cluster, not to convict.

## Gotchas
- Packets split across segments: Wireshark reassembles; tshark single-pass handles ClientHello reassembly too, but very large post-quantum key shares in modern ClientHellos span multiple segments, so check reassembly is enabled (with `tcp.desegment_tcp_streams` off the ClientHello is not decoded; with it on, the SNI appears on the frame that completes the message).

## Verify
Each suspicious connection is described by SNI, ALPN, offered versions, fingerprint and destination ASN, and fingerprints are compared to a baseline of normal clients in the same capture.

## Checked
Run on Wireshark 4.4.1: a hand-built ClientHello (SNI, ALPN h2 and http/1.1, supported_versions 0x0304 and 0x0303) showed
every field and JA4/JA3 values in the quoted tshark command; a ClientHello split over three TCP segments was decoded on
the last segment and not at all with TCP reassembly off; the RFC 9001 appendix A.2 client Initial packet decoded as QUIC with
SNI example.com, an ALPN and a JA4 beginning `q13`. ECH wording checked against RFC 9849. The version string for JA4
cannot be pinned from the release notes, so it is stated as observed.
