---
id: computing-software.cryptography-implementation.applied-cryptography.testing-large-clienthello-middlebox-breakage
name: testing-large-clienthello-middlebox-breakage
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, large-clienthello, post-quantum, x25519mlkem768, middlebox, tls-1-3, tldr-fail, packet-capture, pq-tls]
level: practitioner
status: draft
description: "Test for middleboxes and servers that break on PQ-sized TLS ClientHellos split across packets: reproduction, packet captures, vendor fixes and fallbacks."
sources: ["https://tldr.fail/", "https://blog.chromium.org/2024/05/advancing-our-amazing-bet-on-asymmetric.html", "https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing large ClientHello middlebox breakage

An X25519MLKEM768 key share adds about 1.2 KB, pushing the ClientHello above about 1,500 bytes so it spans two TCP
segments (or multiple QUIC Initial packets). Some firewalls, load balancers and servers assumed one packet and drop
or reset the connection ("tldr.fail" bugs).

## Reproduce
```
# Classical only (control)
openssl s_client -connect host:443 -groups X25519 </dev/null
# PQ hybrid, large ClientHello (OpenSSL 3.5+)
openssl s_client -connect host:443 -groups X25519MLKEM768 </dev/null
curl -v --curves X25519MLKEM768 https://host/      # curl built against OpenSSL 3.5 / BoringSSL
```
A timeout, reset or "unexpected eof" only with the hybrid group indicates the bug.

## Capture
```
tcpdump -i any -w ch.pcap host <ip> and port 443
```
In Wireshark, filter `tls.handshake.type == 1` and check whether the ClientHello is reassembled from two segments and
what the peer sends next (RST, nothing, or a ServerHello).

## Fixes
- Update the middlebox or server firmware (most major vendors shipped fixes after 2024).
- As a temporary workaround, servers can be configured to prefer classical groups for affected paths, or clients can
  rely on HelloRetryRequest by sending only X25519 initially and listing the hybrid in supported_groups (costs a
  round trip).
- Chrome's enterprise policy `PostQuantumKeyAgreementEnabled` can disable hybrid KEX for managed fleets while
  vendors fix devices; set a removal date.

## Verify
- [ ] Hybrid handshake succeeds through every network path (office, VPN, partner links).
- [ ] Monitoring compares handshake failure rates for hybrid vs classical clients.
