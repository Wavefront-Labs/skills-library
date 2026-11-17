---
id: computing-software.cryptography-implementation.secure-implementation.fault-injection-defenses
name: fault-injection-defenses
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, fault-injection, differential-fault-analysis, dfa, rsa-crt-attack, bellcore-attack, glitch-attack, redundant-computation, result-verification, smart-card-security, bootloader-security]
level: sme
status: draft
description: "Defending crypto implementations against fault injection: the RSA-CRT (Bellcore) signature attack, why faulted outputs must never be released, redundant computation and verify-before-output."
sources: ["https://www.researchgate.net/publication/2409434_On_the_Importance_of_Checking_Cryptographic_Protocols_for_Faults", "https://eprint.iacr.org/2004/100", "https://wiki.newae.com/Fault_Attacks"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fault injection and differential fault analysis defenses

Fault injection is a **physical-access attack class**: an adversary
deliberately induces a hardware glitch (voltage spike, clock glitch,
laser/EM pulse on a chip, a bit-flip in RAM) during a cryptographic
computation, then uses the *faulty* output to extract the secret key. This
is firmly in the same physical-proximity threat model as the power/EM
analysis covered in
`computing-software.cryptography-implementation.secure-implementation.side-channel-defenses-beyond-timing`
— relevant to smart cards, hardware tokens, secure elements, and HSMs, not
to typical server/cloud software.

## The canonical example: RSA-CRT signature fault attack (Bellcore attack)

RSA implementations commonly use the **Chinese Remainder Theorem (CRT)** to
speed up the private-key operation, computing two partial results (mod `p`
and mod `q`) and combining them. The 1997 Bellcore attack showed that if an
attacker can induce a fault during computation of **just one** of the two
CRT partial results (e.g., a glitch that corrupts the mod-`q` computation
but leaves mod-`p` correct), the resulting faulty signature, combined with
the correct public key and a single correct signature of the same message,
lets the attacker compute `gcd(faulty_signature^e - message, N)` and
recover one of the prime factors of the RSA modulus directly — a **complete
private key break from a single faulted signature.** This is still the
textbook motivating example for why fault resistance is treated as a hard
requirement in any hardware security module or smart card doing RSA-CRT,
not an edge case.

## The general defense: never release an unverified result

The core, implementation-agnostic countermeasure for essentially all fault
attacks: **verify the result of a sensitive computation before releasing
it**, and if verification fails, output nothing (not even an error
revealing *which* check failed, ideally) rather than the faulty result.
- **For RSA-CRT specifically:** after computing a signature via the fast
  CRT path, verify it by re-encrypting with the public key and checking it
  reproduces the original message/hash, before releasing the signature.
  This single check closes the Bellcore attack, because a faulted
  signature will fail this verification and never leave the device.
- **Redundant computation:** compute the sensitive operation twice
  (ideally via two different code paths or at two different times) and
  compare results before releasing either — a transient fault affecting
  only one computation is caught by the mismatch. This is more expensive
  than a single verify-before-output check but is the standard defense
  for operations (like certain symmetric operations) where a
  "verify by re-deriving the input" check isn't naturally available the
  way RSA's public-key re-encryption check is.
- **Infective computation / error diffusion** (more advanced): design the
  computation so that a fault at any point corrupts the *entire* output
  unpredictably rather than leaving most of the result correct and only a
  localized piece wrong — this removes the attacker's ability to isolate
  which specific sub-computation was faulted, which is what differential
  fault analysis generally needs. Implementing this correctly is
  specialist cryptographic engineering, not a general application-layer
  technique.

## Glitch detection and environmental monitoring (hardware-level, context)

Dedicated secure hardware (smart cards, secure elements, HSMs) typically
includes on-chip sensors for voltage, clock, and temperature anomalies that
trigger a defensive reset or key-wipe if an out-of-spec condition
(consistent with a glitch attack) is detected — this is a hardware design
concern, not something application/firmware code implements from scratch,
but it's worth knowing it exists when evaluating whether a given secure
element/HSM is actually fault-resistant (look for Common Criteria or
similar certification that specifically tests fault-injection resistance,
not just "FIPS validated," since FIPS 140 historically weighted fault
resistance differently than Common Criteria smart-card profiles do).

## Scope — when this matters

Like power/EM side channels, this is a **physical-access attack class.**
Typical server/cloud application software has no realistic fault-injection
exposure (an attacker can't glitch a cloud VM's voltage rails). This matters
for: smart cards, payment terminals, hardware security tokens, IoT secure
elements, and HSMs where an adversary can gain physical possession of the
device. Don't invest engineering effort here for a pure server-side crypto
stack; do invest here (and bring in specialists) for any embedded/physically-
exposed secure hardware project.

## Verify

- [ ] Any RSA-CRT signing implementation verifies the signature against
      the public key before releasing it — the single highest-value check
      against the Bellcore-class attack.
- [ ] Sensitive computations in physically-exposed devices use redundant
      computation or an equivalent verify-before-output check, not a
      single unverified computation path.
- [ ] Error output on a verification failure does not leak which specific
      sub-check failed (information that could help an attacker refine the
      fault).
- [ ] If evaluating hardware (secure element/HSM) for a physically-exposed
      deployment, fault-injection resistance certification (not just FIPS)
      was explicitly checked.
- [ ] Fault-injection defense engineering effort is scoped to actually
      physically-exposed hardware, not applied as unnecessary complexity to
      server-side-only software.

Draft: this is an orientation-level map of a specialist hardware-security
field; actual fault-resistant implementation requires lab-equipment
validation (fault injection test benches) and domain experts, out of scope
for depth here.
