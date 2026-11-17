---
id: computing-software.cryptography-implementation.applied-cryptography.ml-dsa-rejection-sampling-side-channels
name: ml-dsa-rejection-sampling-side-channels
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ml-dsa-rejection-sampling, ml-dsa, fips-204, side-channel, fiat-shamir-with-aborts]
level: sme
status: draft
description: "Handle ML-DSA signing's rejection loop safely: variable iteration counts, what may leak, constant-time checks inside each attempt, and fault risks."
sources: ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf", "https://eprint.iacr.org/2023/050", "https://pq-crystals.org/dilithium/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML-DSA rejection sampling and side channels

## Why signing loops
ML-DSA (Fiat-Shamir with aborts) samples a mask `y`, computes `z = y + c*s1`, and restarts if `z` or the hint
would leak information about `s1`/`s2` (norm checks against `gamma1 - beta`, `gamma2 - beta`). Expected
iterations: about 4.3 (ML-DSA-44), 5.1 (65), 3.9 (87).

## What may leak
- The number of iterations is public by design; rejected attempts' contents must not leak. FIPS 204 notes
  rejected `z`/`c` values are sensitive.
- Leaking the rejection reason or partial values of rejected `z` (via timing of early-exit norm checks or
  error logs) has been shown to enable key recovery.

## Implementation rules
- Norm checks inside an attempt should be constant time over the coefficients, or at least not leak which
  coefficient failed.
- Do not log, return or reuse values from rejected iterations.
- Use hedged signing (fresh `rnd`) by default; deterministic mode increases fault-attack exposure.
- Fault defence: verify the signature before release on high-value signers, or recompute critical steps.
- Cap iterations with a high bound (FIPS 204 mentions implementations may cap at e.g. 814 for negligible failure)
  and fail closed.

## Verify
- [ ] Constant-time tooling over signing with secret key marked secret.
- [ ] Code review confirms rejected-iteration data is wiped and not exposed.
