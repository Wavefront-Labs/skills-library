---
id: computing-software.cryptography-implementation.protocol-implementation.cpace-balanced-pake
name: cpace-balanced-pake
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, cpace, pake, balanced-pake, ristretto255, password-authenticated-key-exchange]
level: sme
status: docs-checked
description: "Use CPace for balanced password-authenticated key exchange: generator from PRS, CI and sid, abort on identity, ISK derivation, recommended suites, and when to prefer OPAQUE."
sources: ["https://datatracker.ietf.org/doc/draft-irtf-cfrg-cpace/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPace balanced PAKE

CPace (an IRTF CFRG Internet-Draft) is a balanced password-authenticated key establishment: both parties start with
a shared password-related string (PRS), which can be low-entropy.

## Protocol outline
1. Both compute a generator `g = G.calculate_generator(H, PRS, CI, sid)`, where CI is channel identifier data and
   sid a session ID.
2. Each samples a scalar, sends `Y = scalar * g` plus optional associated data (AD).
3. Each computes `K = scalar_mult_vfy(own scalar, peer Y)` and MUST abort if K is the group identity. Otherwise
   `ISK = H.hash(lv_cat(G.DSI || "_ISK", sid, K) || transcript(Ya, ADa, Yb, ADb))`.
4. The ISK is identical on both sides if and only if PRS, CI and sid match and the transcript views match.

## Suites
Suites are named `CPACE-G-H`. The draft recommends `CPACE-X25519-SHA512` and the P-256 suite with RFC 9380
encode_to_curve and SHA-256; for higher security margins `CPACE-X448-SHAKE256`, the P-384 suite and the P-521
suite. `CPACE-RISTR255-SHA512` and `CPACE-DECAF448-SHAKE256` are also defined. Recommended sets can change between
draft versions, so check the current text.

## When to use
- Balanced settings where both sides hold the same PRS.
- Applications with servers that store account and password information are recommended by the draft to use an
  augmented PAKE such as OPAQUE (RFC 9807).

## Implementation notes
- The ISK matches only if the sid and CI inputs match on both sides, so agree them explicitly.
- Draft-stage: pin the draft version and its test vectors (appendix B).

## Verify
- [ ] Draft test vectors pass for the chosen suite.

## Checked

2026-11-01: draft-irtf-cfrg-cpace (April 2026 text) sections 4, 5 and 7.2 read. Confirmed: PRS, OPAQUE recommendation, suite names, generator and ISK computation, abort on identity. Removed: PAKE competition claim, explicit-MAC key confirmation step, SPAKE2 comparison, P-256 and Elligator2 suite names not in the draft.
Method: documentation only; no commands were run.
