---
id: computing-software.cryptography-implementation.applied-cryptography.authenticating-diffie-hellman-exchanges
name: authenticating-diffie-hellman-exchanges
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, dh-authentication, authenticated-key-exchange, mitm, sigma, transcript-signature]
level: advanced
status: docs-checked
description: "Authenticate Diffie-Hellman exchanges against man-in-the-middle: sign transcripts, static-ephemeral keys, PSK or PAKE, and bind identities into key derivation."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-4.4.3", "https://noiseprotocol.org/noise.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticating Diffie-Hellman exchanges

Unauthenticated (anonymous) DH gives a secret shared with whoever answered, including an attacker who runs two
exchanges. Every DH handshake needs one of these:

## Options
1. **Signed transcript (TLS 1.3)**: CertificateVerify is a signature over the handshake with the party's
   long-term key, and Finished is a MAC over the handshake (RFC 8446). RFC 8446 cites the SIGMA paper for this
   design.
2. **Static-ephemeral DH (Noise patterns such as IK and XX)**: DH tokens such as `es`, `se` and `ss` mix
   long-term static keys into the handshake; only the holder of the static private key can derive the result.
3. **Pre-shared key**: mix a PSK into the key schedule (TLS 1.3 `psk_dhe_ke`, Noise `psk` token).
4. **PAKE** when only a password is shared (use a published PAKE, not a hand-built one).
5. **Out-of-band comparison** of a hash of the transcript for device pairing.

## Rules
- Sign or MAC the whole transcript, not just the peer's public key.
- Include both parties' identities in the derivation or the signed data.
- Verify peer certificates or pinned keys before trusting the derived key.
- Key confirmation (Finished messages in TLS 1.3) proves both derived the same key.

## Verify
- [ ] Threat model shows how an active attacker is detected.
- [ ] Protocol modelled or matches a published design (TLS 1.3, Noise pattern) rather than an ad hoc one.

## Checked
2026-11-01. Confirmed in RFC 8446 (CertificateVerify signature over the handshake, Finished MAC, key
confirmation, `psk_dhe_ke`, SIGMA reference) and the Noise specification (tokens, IK pattern, `psk` token).
Removed: Signal X3DH, WireGuard, OPAQUE, CPace, the unknown key-share attack name, and the "MACs its identity"
detail, which were not in the cited pages.
Method: documentation only; no commands were run.
