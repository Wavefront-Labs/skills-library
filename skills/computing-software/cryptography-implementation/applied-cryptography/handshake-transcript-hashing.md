---
id: computing-software.cryptography-implementation.applied-cryptography.handshake-transcript-hashing
name: handshake-transcript-hashing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, transcript-hash, handshake, tls-1-3, ssh-exchange-hash, noise-protocol, channel-binding, protocol-design]
level: advanced
status: docs-checked
description: "Build handshake transcript hashes that bind every message: TLS 1.3 Transcript-Hash and HRR rules, SSH exchange hash, Noise h, and common binding bugs."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-4.4.1", "https://www.rfc-editor.org/rfc/rfc4253#section-8", "https://noiseprotocol.org/noise.html#the-symmetricstate-object", "https://terrapin-attack.com/", "https://www.rfc-editor.org/rfc/rfc8448"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handshake transcript hashing

A transcript hash commits to every handshake message so that keys, Finished MACs and signatures depend on exactly
what both sides saw.

## Reference designs
- **TLS 1.3:** `Transcript-Hash(M1, ..., Mn) = Hash(M1 || ... || Mn)` over handshake messages including the handshake
  message header (type and length) but not record layer headers. After HelloRetryRequest, ClientHello1 is replaced by
  a synthetic `message_hash` handshake message containing Hash(ClientHello1); this lets a server do a stateless
  HelloRetryRequest by keeping only that hash in the cookie.
- **SSH:** exchange hash `H = hash(V_C || V_S || I_C || I_S || K_S || e || f || K)` (identification strings, KEXINIT
  messages, server host key, ephemeral values, shared secret). The server signs H.
- **Noise:** running hash `h`, updated with `MixHash` over the prologue, pre-message public keys and every handshake
  payload; `h` is the associated data of `EncryptWithAd`, so tampering fails decryption.

## Rules
1. Hash exact bytes as sent on the wire, not a re-encoded structure.
2. Include identity data (certificates, host keys) and negotiation messages (offers and choices).
3. Length-prefix or use self-delimiting encodings so message boundaries are unambiguous.
4. Make sure sequence or state not in the transcript cannot be manipulated (Terrapin exploited sequence number
   manipulation in the SSH handshake).
5. Use the transcript in key derivation and in the final authentication (MAC or signature).

## Common bugs
- Hashing only the server's messages, or only the choices, not the offers (enables downgrade).
- Excluding the HRR or retry message.
- Using different encodings on each side (e.g. JSON re-serialisation).
- Computing the transcript after parsing and normalising a message.

## Verify
- [ ] Flipping any bit in any handshake message causes handshake failure.
- [ ] Known-answer traces from RFC 8448 (example handshake traces) match.

## Checked
2026-11-01. Confirmed in RFC 8446 section 4.4.1 (transcript definition, header inclusion, message_hash and the
stateless-HRR reason), RFC 4253 section 8 (H formula, server signs it), the Noise specification (MixHash,
prologue, pre-message keys, h as associated data), the Terrapin page (sequence number manipulation) and RFC 8448
(example traces). Removed: the numeric type code and the exact SSH string/mpint encoding detail.
Method: documentation only; no commands were run.
