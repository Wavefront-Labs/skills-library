---
id: computing-software.cryptography-implementation.protocol-implementation.spake2-device-pairing
name: spake2-device-pairing
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, pake, spake2, spake2-plus, rfc9382, rfc9383, device-pairing, matter, short-code, magic-wormhole]
level: advanced
status: docs-checked
description: "Pair devices or users with a short code using SPAKE2 (RFC 9382) or SPAKE2+ (RFC 9383): when a balanced PAKE fits, the flow, identities, key confirmation and groups."
sources: ["https://datatracker.ietf.org/doc/html/rfc9382", "https://datatracker.ietf.org/doc/html/rfc9383"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPAKE2 device pairing

A balanced PAKE turns a short shared secret (a short code, a few words) into a
strong session key without exposing the code to an eavesdropper.

## SPAKE2 vs SPAKE2+

- **SPAKE2 (RFC 9382)**: both parties know the password. Good for
  user-to-user pairing (both type the same code).
- **SPAKE2+ (RFC 9383)**: augmented - only one party (the prover) knows the
  password; the verifier holds values derived from it, not the
  password itself. SPAKE2 itself does not support augmentation, so the server
  stores a password equivalent (RFC 9382 security considerations).

## Flow (SPAKE2)

1. Both derive `w` from the password, typically `w = MHF(pw) mod p` with a
   memory-hard function (parameter choice is out of scope of the RFC).
2. A picks x and sends `pA = w*M + x*P`; B picks y and sends `pB = w*N + y*P`
   (M, N fixed points specified for each group).
3. A computes `K = h*x*(pB - w*N)`, B computes `K = h*y*(pA - w*M)`. K must not
   be output as the shared secret; both derive keys from the transcript TT
   which includes K.
4. **Key confirmation**: the key schedule derives MAC keys KcA and KcB for
   confirmation messages (RFC 9382 section 4); abort if a MAC does not match.

## Rules

- Include identities of A and B in the transcript. An absent identity is
  encoded as a zero-length string and only for applications where identities
  are implicit; otherwise the protocol risks unknown key-share attacks (RFC
  9382 section 3.3).
- Limit attempts per code and expire codes; a short code is guessable by
  repeated online runs.
- Use the RFC's M and N constants for your group (the RFC lists P-256 and
  edwards25519 suites and the seed method); never generate M/N with known
  discrete logs.
- Check which RFC version and group a library implements before interop.

## Verify

- [ ] Wrong code fails at key confirmation, not later.
- [ ] Attempt counter and code expiry enforced on the device/server side.
- [ ] RFC 9382/9383 test vectors pass for the chosen group.

## Checked

2026-11-01: RFC 9382 (flow, K computation, identities, key confirmation, suites, augmentation note) and the RFC 9383 abstract/introduction read. Removed: Magic Wormhole, Matter and Chrome usage claims, attempt-count figures and library names (not in the RFCs), ristretto255 as an RFC 9382 group.
Method: documentation only; no commands were run.
