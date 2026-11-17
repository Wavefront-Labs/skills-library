---
id: computing-software.cryptography-implementation.applied-cryptography.composite-and-hybrid-signatures
name: composite-and-hybrid-signatures
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-dsa, composite-signatures, hybrid-signatures, post-quantum, ecdsa, lamps, stripping-attack]
level: advanced
status: docs-checked
description: "Design composite ML-DSA plus ECDSA/Ed25519 signatures using the LAMPS draft: labels, pre-hashing, fresh component keys, fixed pairings and stripping resistance."
sources: ["https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/", "https://datatracker.ietf.org/doc/rfc9955/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite and hybrid signatures

A composite signature pairs a post-quantum scheme (ML-DSA) with a classical one (ECDSA or Ed25519, per the LAMPS
draft) so one public key and one signature carry both components. The IETF draft is still a draft: pin the version
you implement.

## How the LAMPS composite works

- The two component signatures are combined by a signature combiner that pre-hashes the message and prepends label
  values before passing it to the component algorithms. The draft's message representative is
  `M' = Prefix || Label || len(ctx) || ctx || PH(M)`.
- Each composite algorithm has its own fixed Label that binds the signature to that composite algorithm. Label
  values are fully specified and runtime-variable labels are not allowed.
- Registered pairings include `id-MLDSA65-ECDSA-P256-SHA512` and `id-MLDSA65-Ed25519-SHA512`. Use the registered
  combinations; do not let the signer pick components dynamically.
- The draft says the combiner gives weak non-separability, and discusses stripping attacks in its Security
  Considerations. Do not invent your own format without equivalent binding.

## Key rules from the draft

- Key generation must run for both component algorithms so keys are fresh. Do not use, import or export component
  keys that are used in other contexts, combinations or standalone.
- Key reuse across composite and standalone use must be avoided; the draft notes it can open EUF-CMA
  vulnerabilities and complicates certificate revocation.

## Choosing an approach

Read the IETF hybrid signature spectrums document (now RFC 9955) for the design space of composite versus other
hybrid constructions, then check your regulator's current guidance directly; this skill does not restate national
policy.

## Verify

- [ ] Verification checks both components and rejects if either is invalid.
- [ ] A component signature extracted from a composite fails as a standalone signature.
- [ ] OIDs, labels and algorithm ids match the exact LAMPS draft version you implement.

## Checked

2026-11-01. Confirmed in draft-ietf-lamps-pq-composite-sigs (April 2026 text): ECDSA or Ed25519 components, the
combiner and `M'` formula, per-algorithm Label, the two named OIDs, weak non-separability, stripping and key-reuse
sections. The hybrid-signature-spectrums page now resolves to RFC 9955. Removed: statements about BSI, ANSSI and NSA
CNSA 2.0 policy, the dual-certificate and nested-signature rows, ML-DSA-65 pairings other than those named, and
the short-lived-signature advice, which the cited pages do not state (the BSI source could not be fetched).
Method: documentation only; no commands were run.
