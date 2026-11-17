---
id: computing-software.cryptography-implementation.applied-cryptography.downgrade-resistant-negotiation
name: downgrade-resistant-negotiation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, downgrade-protection, downgrade-attack, tls-1-3, tls-fallback-scsv, rfc-7507, terrapin, cve-2023-48795, ssh-strict-kex, negotiation]
level: advanced
status: docs-checked
description: "Design and verify downgrade protection for version and algorithm negotiation: transcript MACs, TLS 1.3 sentinels, fallback SCSV and SSH strict KEX (Terrapin)."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-4.1.3", "https://www.rfc-editor.org/rfc/rfc7507", "https://terrapin-attack.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downgrade-resistant negotiation

Any protocol that negotiates versions or algorithms must stop an active attacker from steering both sides to the
weakest common option.

## Principles
1. **Authenticate the whole negotiation:** everything both parties sent and received goes into a transcript hash
   that is MACed or signed at the end of the handshake (TLS Finished, SSH exchange hash, Noise handshake hash).
2. **Signal the maximum version inside authenticated data,** so a downgraded session can detect it.
3. **No insecure fallback by retry:** never reconnect with a lower version after a failure unless the retry carries a
   fallback signal.
4. **Strict message ordering and sequence numbers covered by the transcript.**

## Real mechanisms
- **TLS 1.3 sentinels (RFC 8446 4.1.3):** a TLS 1.3 server negotiating TLS 1.2 must set the last 8 bytes of
  ServerHello.random to `44 4F 57 4E 47 52 44 01`; for TLS 1.1 or below the last byte is `00`. A TLS 1.3 client
  receiving a ServerHello that indicates TLS 1.2 or below must check for both values and, on a match, abort with an
  `illegal_parameter` alert.
- **TLS_FALLBACK_SCSV (RFC 7507):** value `{0x56, 0x00}` in ClientHello.cipher_suites, included by clients that retry
  with a lower version; a server that supports a higher version than the ClientHello offers must respond with a
  fatal `inappropriate_fallback` alert.
- **SSH strict KEX:** Terrapin (CVE-2023-48795) is a prefix truncation attack: by adjusting sequence numbers during
  the handshake an attacker can delete messages at the start of the secure channel unnoticed. The countermeasure is
  strict key exchange, which resets sequence numbers and removes the ability to inject packets during the initial
  handshake. It only takes effect when both client and server support it.

## Designing your own
- Put the full list of offered versions/algorithms in the first message and echo it into the transcript.
- The final MAC/signature covers the transcript; mismatches abort.
- Remove weak options entirely rather than relying only on downgrade detection.

## Verify
- [ ] A test MITM that strips a high version or strong algorithm causes handshake failure.
- [ ] Both ends of each SSH link support strict key exchange (the Terrapin scanner checks this).
- [ ] Clients have no "retry with older protocol" path.

## Checked
2026-11-01. Confirmed in RFC 8446 section 4.1.3 (sentinel bytes, client check, illegal_parameter), RFC 7507
(SCSV value, inappropriate_fallback) and the Terrapin site (CVE number, sequence-number mechanism, strict key
exchange needs both sides, scanner). Removed: the OpenSSH extension names and version number, and the
`ssh -vv` check, which those pages do not state.
Method: documentation only; no commands were run.
