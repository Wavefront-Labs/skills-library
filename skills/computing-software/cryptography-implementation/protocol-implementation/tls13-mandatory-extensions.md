---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-mandatory-extensions
name: tls13-mandatory-extensions
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, tls13-extensions, tls-1-3, rfc-8446, supported-versions, key-share, signature-algorithms]
level: advanced
status: docs-checked
description: "Implement and debug TLS 1.3 mandatory extensions (RFC 8446 9.2): supported_versions, key_share, signature_algorithms, supported_groups, server_name, and their errors."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-4.2", "https://www.rfc-editor.org/rfc/rfc8446#section-9.2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 mandatory extensions

## Required by RFC 8446 9.2 (unless the application profile says otherwise)
| Extension | Role |
|---|---|
| `supported_versions` (43) | Real version negotiation; legacy_version stays 0x0303. Required in ClientHello and ServerHello for TLS 1.3 |
| `key_share` (51) | ECDHE/KEM shares; server returns one share or sends HelloRetryRequest |
| `supported_groups` (10) | Groups the client can do (for example x25519, secp256r1) |
| `signature_algorithms` (13) | Schemes for CertificateVerify; `signature_algorithms_cert` (50) optionally for certificate chains |
| `server_name` (0) | SNI; all implementations must support it, servers may require it (then `missing_extension`) |
| `pre_shared_key` (41) + `psk_key_exchange_modes` (45) | Resumption; pre_shared_key must be the last extension in ClientHello |
| `cookie` (44) | In HRR to make the server stateless |

## Placement rules
- ServerHello carries only `supported_versions`, `key_share`, `pre_shared_key`. Everything else goes in
  EncryptedExtensions (ALPN, server_name ack, early_data) or Certificate (OCSP status, SCTs per certificate).
- Unknown extensions in ClientHello must be ignored by servers; unsolicited extensions in server messages must
  cause `unsupported_extension` alerts at clients.

## Alerts you will see
- `missing_extension` (109): e.g. TLS 1.3 ClientHello without supported_groups when key_share present.
- `illegal_parameter`: server key_share for a group the client did not offer.
- `handshake_failure`: no common signature algorithm or group.

## Verify
- [ ] A packet capture shows extension placement as in the RFC 8446 extension table.

## Checked

2026-10-31. Confirmed in RFC 8446 (4.2 extension table and numbers 0, 10, 13, 41, 43,
44, 45, 50, 51; 9.2 required extensions and `missing_extension`; `unsupported_extension`
for unsolicited responses; `pre_shared_key` last; `illegal_parameter` and
`handshake_failure` cases). Removed: X25519MLKEM768 example, the claim that clients must
send server_name, the s_client and tlsfuzzer mentions, the IANA source.

Method: documentation only; no commands were run.
