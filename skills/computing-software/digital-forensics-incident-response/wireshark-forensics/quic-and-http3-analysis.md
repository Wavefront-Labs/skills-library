---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.quic-and-http3-analysis
name: quic-and-http3-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [quic, http3, udp-443, tls-keylog, ja4, sni, wireshark, dfir]
level: advanced
status: draft
description: "Analyse QUIC and HTTP/3 traffic: identify it on UDP 443, read the Initial packet SNI, decrypt with SSLKEYLOGFILE, and handle QUIC as a visibility gap."
sources: ["https://datatracker.ietf.org/doc/html/rfc9000", "https://wiki.wireshark.org/QUIC", "https://github.com/FoxIO-LLC/ja4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QUIC and HTTP/3 analysis

**Goal:** understand and, where possible, decrypt QUIC traffic, which carries an increasing
share of web traffic (Google, Cloudflare, Meta) and is used by some malware and tunnelling
tools to bypass TLS inspection.

## Recognise it
- UDP 443 (sometimes 80/8443), filter `quic`. Long-header packets (Initial, 0-RTT, Handshake,
  Retry) at connection start, then short-header 1-RTT packets.
- `quic.version` (0x00000001 = v1, 0x6b3343cf = v2), `quic.dcid`/`quic.scid` connection IDs
  (connections can migrate across IPs/ports; track by connection ID, not 5-tuple).

## SNI and fingerprints
Initial packets are encrypted with keys derived from the destination connection ID, which
Wireshark derives automatically, so the TLS ClientHello inside is readable:
```
quic && tls.handshake.type == 1
tls.handshake.extensions_server_name
```
JA4 has a QUIC variant (`q` prefix, e.g. `q13d0310h3_...`) for client fingerprinting.
Encrypted Client Hello (ECH) hides the real SNI (outer SNI shows the provider's public name).

## Decrypt
Same as TLS: set `SSLKEYLOGFILE` on the client (Chrome, Firefox, curl, many Go/Rust tools),
then Preferences > Protocols > TLS > (Pre)-Master-Secret log filename. Wireshark then shows
`http3` frames (HEADERS, DATA), QPACK-decoded headers and streams (Follow > QUIC Stream).

## Investigation tips
- Corporate networks often block UDP 443 to force fallback to TCP TLS, which the proxy can
  inspect. QUIC flows to unusual destinations from servers (not browsers) are suspicious.
- Malware/tunnels over QUIC: Merlin C2, Sliver-capable configs, Chisel/quic-based tunnels,
  Hysteria/TUIC proxies. Look for long-lived QUIC to VPS ranges with periodic packets.
- Zeek has a QUIC analyser (`quic.log`, with SNI and versions in recent versions); Suricata
  parses QUIC for SNI and JA4.
- Firewall/flow logs show UDP 443 only; volume and duration are the main signals.

## Gotchas
- Without key logs, only the Initial handshake and metadata are visible; no server certificate
  (it is in encrypted Handshake packets in TLS 1.3).
- Older Wireshark versions dissect QUIC drafts poorly; use a current release.

## Self-check
You identified QUIC flows by connection ID, extracted SNI/JA4 for each, and stated whether
content could be decrypted.
