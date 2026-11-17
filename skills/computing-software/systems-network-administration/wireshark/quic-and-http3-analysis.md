---
id: computing-software.systems-network-administration.wireshark.quic-and-http3-analysis
name: quic-and-http3-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, quic, http3, tls-1-3, sslkeylogfile, udp-443, qlog, connection-id]
level: practitioner
status: gated
description: "Analyse QUIC and HTTP/3 in Wireshark: recognising UDP 443 handshakes, decrypting with SSLKEYLOGFILE, connection IDs and migration, and forcing fallback to TCP."
sources:
  - https://www.rfc-editor.org/rfc/rfc9000
  - https://www.rfc-editor.org/rfc/rfc9114
  - https://wiki.wireshark.org/QUIC
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QUIC and HTTP/3 analysis

QUIC is UDP (usually 443) with TLS 1.3 built in; everything after the first Initial packets is
encrypted, including transport headers like packet numbers and ACKs. Without keys you see
little beyond the handshake.

## Filters
```
quic                                    # all QUIC
quic.long.packet_type == 0              # Initial packets (contain ClientHello)
tls.handshake.extensions_server_name    # SNI is readable in Initial (Initial keys are public)
http3
quic.connection.number == 3             # one connection (Wireshark's index)
```

## Decrypt
Set `SSLKEYLOGFILE` before launching a browser or other client that supports TLS key logging; point Edit > Preferences > Protocols > TLS > (Pre)-Master-Secret log
filename at it. QUIC uses the same keylog. Then HTTP/3 frames, headers (QPACK) and ACK
frames are visible (gated: unconfirmed, source is paywalled or blocked). No decrypted QUIC capture could be built here, so this decryption workflow was not run. Wireshark 4.4.1 decodes QUIC v1 (RFC 9000/9001): the RFC 9001 appendix A.2 sample Initial packet showed as `QUIC ... Initial ... CRYPTO` with its SNI.

## What to look for
- **Handshake RTT:** Initial -> Handshake -> 1-RTT; 0-RTT data on resumption.
- **Loss:** gaps in packet numbers (decrypted), ACK frames with ranges, PTO probes.
- **Connection migration:** same connection ID from a new client IP/port (Wi-Fi to cellular).
- **Version negotiation / Retry** packets: middlebox or server forcing address validation.

## When QUIC is the problem
To test whether QUIC is involved in a problem, block UDP 443 for one test client and compare the two captures
(the behaviour and any fallback delay differ by client, so measure rather than assume).
Server/application side: qlog files (qvis) are richer than pcaps for QUIC debugging.

## Verify
- [ ] Decrypted capture shows HTTP/3 requests; handshake timing and loss measured per connection.

## Checked
Run on Wireshark 4.4.1: the RFC 9001 appendix A.2 client Initial (fetched from the RFC and replayed in a pcap) decoded as
QUIC, `quic.long.packet_type == 0` matched it, `tls.handshake.extensions_server_name` showed example.com, and `quic`
matched while `http3` and `quic.connection.number == 3` parsed (no match, as expected). The `tls.keylog_file` preference exists.
Initial keys being derivable from the public connection ID (RFC 9001), connection migration, version negotiation and Retry
(RFC 9000) are from the RFCs, and qvis is live at qvis.quictools.info. No decrypted QUIC capture was available, so the
decryption section is documentation only and not exercised here.
