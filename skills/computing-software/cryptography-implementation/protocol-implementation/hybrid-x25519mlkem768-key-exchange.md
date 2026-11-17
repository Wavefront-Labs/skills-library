---
id: computing-software.cryptography-implementation.protocol-implementation.hybrid-x25519mlkem768-key-exchange
name: hybrid-x25519mlkem768-key-exchange
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, ml-kem, hybrid-kem, x25519mlkem768, post-quantum, tls-1-3, key-share, x-wing]
level: advanced
status: docs-checked
description: "Deploy hybrid X25519MLKEM768 key exchange in TLS 1.3 (RFC 10024): codepoints, key_share sizes, secret concatenation order, and caution outside TLS."
sources: ["https://datatracker.ietf.org/doc/rfc10024/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid X25519MLKEM768 key exchange

A hybrid KEM combines a classical and a post-quantum key exchange so the
session stays secure if either one holds. RFC 10024 (Proposed Standard,
August 2026) defines X25519MLKEM768, SecP256r1MLKEM768 and SecP384r1MLKEM1024
for TLS 1.3.

## TLS 1.3 layout (RFC 10024)

| Item | Value |
|---|---|
| NamedGroup | X25519MLKEM768 = 0x11EC (4588) |
| Client key_share | ML-KEM-768 encaps key (1184 B) then X25519 public (32 B) = 1216 B |
| Server key_share | ML-KEM-768 ciphertext (1088 B) then X25519 public (32 B) = 1120 B |
| Shared secret | ML-KEM secret (32 B) then X25519 secret (32 B) = 64 B, fed to the TLS key schedule |

The X25519MLKEM768 name does not follow the usual naming convention: the order of
shares in the concatenation is reversed from the name, for historical reasons.
Other groups: SecP256r1MLKEM768 (4587, 0x11EB) and SecP384r1MLKEM1024 (4589, 0x11ED);
for those the ECDHE part comes first.

## Deployment

Keep a classical group in the server list so old clients still connect.

## Outside TLS

The RFC's concatenation relies on the TLS 1.3 HKDF-based key schedule. In your own
protocol, use a vetted hybrid KEM or key combiner rather than an ad hoc one.

## Verify

- [ ] Handshake shows group X25519MLKEM768 from a modern client.
- [ ] Old clients without the group still negotiate a classical group.

## Checked

2026-10-31. Confirmed in RFC 10024: codepoint 4588 (0x11EC), 4587 (0x11EB), 4589 (0x11ED);
client share 1216 B (1184 + 32); server share 1120 B (1088 + 32); shared-secret order and
64-byte size; the reversed-order naming note. Removed: product and version adoption claims,
the openssl, nginx and Go configuration lines, the X25519Kyber768Draft00 codepoint, the
X-Wing and XOR claims, and the unfetched draft sources.

Method: documentation only; no commands were run.
