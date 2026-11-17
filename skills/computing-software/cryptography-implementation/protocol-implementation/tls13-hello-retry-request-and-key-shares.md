---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-hello-retry-request-and-key-shares
name: tls13-hello-retry-request-and-key-shares
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-1-3, hello-retry-request, key-share, supported-groups, rfc8446]
level: advanced
status: docs-checked
description: "Handle TLS 1.3 key_share negotiation and HelloRetryRequest: client share choice, server group preference, HRR checks, cookies, and transcript handling."
sources: ["https://www.rfc-editor.org/rfc/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HelloRetryRequest and key share negotiation

## How negotiation works
- ClientHello carries `supported_groups` (groups it accepts) and `key_share` (public keys for a subset of them,
  usually one or two).
- Server picks a group from the intersection. If the client already sent a share for it: no retry. If not, the server
  sends a **HelloRetryRequest** (HRR) naming the group, costing one extra round trip.
- HRR is a ServerHello carrying the special Random value
  `CF21AD74E59A6111BE1D8C021E65B891C2A211167ABB8C5E079E09E2C8A8339C` (RFC 8446 4.1.3).

## Client rules (RFC 8446 4.1.2, 4.1.4, 4.2.8)
- After HRR send a second ClientHello with the same content except: `key_share` replaced by only the requested group,
  `cookie` included if the HRR had one, `early_data` removed (early data is not permitted after an HRR), and PSK
  binders recomputed.
- Abort with `illegal_parameter` if the HRR selected_group is not in `supported_groups` or you already sent a share
  for it, or if the HRR would not change the ClientHello.
- A second HRR in the same connection: abort with `unexpected_message`.
- The cipher suite in the ServerHello must equal the one in the HRR, else abort with `illegal_parameter`; the
  selected_version in the HRR must be retained in the ServerHello.
- Transcript: ClientHello1 is replaced by a synthetic `message_hash` message containing Hash(ClientHello1).

## Server rules
- Choose by server preference among groups the client supports, but weigh the round-trip cost: a server that prefers
  a group the client did not pre-share forces an HRR on every handshake.
- Stateless HRR: put needed state (such as a hash of ClientHello1) in an integrity-protected `cookie` extension and
  verify it on the second ClientHello.
- Servers must negotiate the same cipher suite on the updated ClientHello.
- Validate received shares (for ECDHE, check the point; section 4.2.8.2 lists the steps).

## Verify
- [ ] Interop tests cover HRR with each supported group and with a cookie.
- [ ] Second HRR, mismatched suite and unoffered group are rejected with the right alert.
- [ ] HRR rate is monitored after group policy changes.

## Checked
2026-11-01: HRR random value, client abort conditions and alerts, early_data and cookie handling, cipher-suite and
selected_version consistency, message_hash transcript replacement confirmed against RFC 8446 sections 4.1.2, 4.1.3,
4.1.4, 4.2.8, 4.4.1. Removed: post-quantum share sizes, DNS key-share-prediction draft, DTLS/QUIC remark, OpenSSL and
Wireshark debugging lines (not confirmed).
Method: documentation only; no commands were run.
