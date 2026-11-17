---
id: computing-software.cryptography-implementation.protocol-implementation.dtls-13-datagram-channels
name: dtls-13-datagram-channels
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, dtls-1-3, dtls, rfc-9147, connection-id, udp, replay-window]
level: advanced
status: docs-checked
description: "Build datagram secure channels with DTLS 1.3 (RFC 9147): epochs and record numbers, replay window, cookies against amplification, connection IDs, PMTU and retransmission."
sources: ["https://www.rfc-editor.org/rfc/rfc9147", "https://www.rfc-editor.org/rfc/rfc9146"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DTLS 1.3 datagram channels

## How it differs from TLS 1.3
- Records carry an epoch and sequence number, and the sequence number can be encrypted (record number encryption,
  RFC 9147 4.2.3). Receivers keep a sliding replay window, and each epoch needs its own window because each epoch
  resets the sequence number space (4.5.1).
- Handshake messages carry message_seq and fragment fields; lost flights are retransmitted on a timer. Without
  deployment-specific RTT knowledge, use an initial timer of 1000 ms and double it on each retransmission (5.8.2).
  Explicit ACK messages exist in DTLS 1.3.
- A HelloRetryRequest carrying a cookie gives a return-routability check, so the server need not commit state or send
  large flights to a spoofed address (3, 5.1). A stateless cookie must let the server rebuild the first ClientHello
  hash for the transcript (5.1). Enable it on public endpoints.
- Connection IDs (the `connection_id` extension is defined in RFC 9146; RFC 9147 builds the CID into its record
  format) let a session survive address changes. A client that does not want a CID should still offer the extension
  so a server that wants one can negotiate it (5.1).

## Configuration
- DTLS leaves PMTU discovery to the application (4.4). Size records to fit the PMTU estimate to avoid IP
  fragmentation; handshake messages can exceed the PMTU, so fragment them, and if repeated retransmissions get no
  answer back off to smaller records (the RFC suggests 2-3 retransmits before backing off).
- Use AEAD ciphers only (DTLS 1.3 is a delta from TLS 1.3).

## Pitfalls
- DTLS 1.0 (a delta from TLS 1.1) is not recommended and is forbidden by the deprecation document RFC 9147 cites;
  disable it. There is no DTLS 1.1.
- Application-level retransmission duplicating DTLS's; let DTLS handle handshake loss, the application handles data
  loss.
- DTLS 1.3 gives no order protection / non-replayability beyond the replay window; the application must tolerate
  loss, reordering and duplication.

## Verify
- [ ] Packet capture shows a cookie exchange (HelloRetryRequest) on first contact and encrypted record numbers.
- [ ] Interop test against a second implementation with induced loss and reordering.

## Checked
2026-11-01. Confirmed against RFC 9147 (sections 3, 4.2.3, 4.4, 4.5.1, 5.1, 5.8.2, intro on DTLS 1.0 and 1.1) and
RFC 9146 (connection_id extension). Removed: per-library API names and support claims (wolfSSL, mbedTLS, OpenSSL,
GnuTLS), a fixed MTU range and the default replay window size, none of which the RFCs state.
Method: documentation only; no commands were run.
