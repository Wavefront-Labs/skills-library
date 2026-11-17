---
id: computing-software.cryptography-implementation.secure-implementation.side-channel-defenses-beyond-timing
name: side-channel-defenses-beyond-timing
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, side-channel, cache-timing, power-analysis, dpa, electromagnetic-leakage, masking, blinding, spectre, meltdown, microarchitectural-attacks, smart-card-security]
level: sme
status: draft
description: "Side-channel defenses beyond CPU-instruction timing: cache-timing leaks (Flush+Reload, Prime+Probe), power/EM analysis for embedded/smart-card crypto, masking and blinding countermeasures."
sources: ["https://eprint.iacr.org/2005/271", "https://www.rambus.com/blogs/differential-power-analysis/", "https://www.chosenplaintext.ca/articles/beginners-guide-constant-time-cryptography.html", "https://meltdownattack.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Side-channel defenses beyond timing

This product's existing `constant-time-code-and-known-answer-tests` skill
covers instruction-level timing (branches, variable-time comparisons,
table lookups). This skill covers the side-channel classes that constant-time
*code* alone does not address, because they leak through the hardware, not
just the instruction sequence.

## Cache-timing attacks: constant-time code isn't enough on shared hardware

Even code with no secret-dependent branches or variable-time operations can
leak through **cache access patterns** if it indexes memory using secret
data (a classic example: a naive AES T-table implementation indexing a
lookup table by a secret key byte — the *table lookup itself* has data-
dependent timing because of CPU cache behavior, not because of a branch).
- **Flush+Reload / Prime+Probe:** an attacker (another process or VM on
  the same physical core/cache, e.g., a hostile co-tenant in a shared cloud
  environment) measures which cache lines get touched by observing their
  own access timing to shared memory or probing cache sets, recovering
  which table entries the victim process accessed — this is how early
  software AES implementations with table-based lookups were broken even
  though they had no secret-dependent branches.
- **Defense:** use CPU hardware AES instructions (AES-NI on x86, the ARMv8
  Crypto Extensions) wherever available — hardware AES implementations are
  constant-time by construction at the microarchitectural level because
  they don't use data-dependent table lookups at all. If software AES is
  unavoidable (no hardware support), use a **bitsliced** implementation
  (operates on bits in constant-time-by-construction fashion, no lookup
  tables indexed by secret data) rather than table-based.
- This is also why `computing-software.cryptography-implementation.secure-implementation.constant-time-code-and-known-answer-tests`'s
  guidance to avoid secret-dependent table indexing (not just secret-
  dependent branches) matters — table lookups are the specific pattern that
  survives "no branches on secrets" review but still leaks via cache.

## Power analysis and electromagnetic leakage (embedded/smart-card/HSM context)

For devices where an attacker has **physical proximity** (a smart card, a
hardware token, an embedded secure element, sometimes even a nearby
workstation), power consumption and electromagnetic emission during a
cryptographic operation can correlate with the secret key being processed:
- **Simple Power Analysis (SPA):** visually distinguishable power-trace
  differences correlate directly with operations performed (e.g., which
  branch of a conditional ran) — same root cause as a timing side channel,
  observed via power instead of elapsed time.
- **Differential Power Analysis (DPA):** a statistical attack correlating
  many power traces against hypothesized key bits, extracting keys even
  when no single trace is individually informative — this is the technique
  behind most smart-card key-extraction attacks historically, and it
  defeats naive "no secret branches" constant-time code, because the power
  draw of *executing the same instruction* still varies with the data
  values involved (e.g., the Hamming weight of a register).
- **Defense — masking:** split every sensitive intermediate value into
  multiple shares (e.g., `x = x1 XOR x2`) such that operating on the shares
  separately and combining at the end produces the same result but no
  single intermediate value correlates with the secret — this is the
  standard DPA countermeasure in hardened embedded crypto implementations,
  and it is a materially different (and harder to get right) technique than
  ordinary constant-time coding; implementing masking correctly is a
  specialist skill, not a drop-in library call in most cases.
- **Defense — blinding:** for asymmetric operations (RSA, ECC), randomize
  the exponent/scalar or the input before the operation and un-randomize
  the output, so the actual value processed differs every time even for
  the same logical operation — many production libraries (OpenSSL's RSA
  blinding, for instance) apply this by default specifically as a DPA/timing
  countermeasure; confirm it's enabled rather than assuming, if you're
  evaluating a library for a physically-exposed deployment.

## When this actually matters — and when it doesn't

- **Cloud/server/application software without physical attacker access:**
  cache-timing attacks (co-tenant VM/process) are the realistic concern;
  power/EM analysis generally isn't, because it requires physical
  proximity to the hardware. Prioritize hardware-accelerated primitives and
  cache-safe implementations; don't over-invest in masking schemes meant
  for physically-exposed devices.
- **Embedded devices, smart cards, hardware wallets, secure elements, HSMs
  physically accessible to an adversary:** power/EM side channels are a
  real, well-documented attack class and masking/blinding is standard
  practice in that industry — if you're building for this threat model,
  this is specialist territory; use certified hardware (HSMs/secure
  elements with side-channel-resistance certifications, e.g., Common
  Criteria evaluations that specifically test DPA resistance) rather than
  attempting to roll your own masked implementation without deep expertise
  and lab-equipment validation.

## Verify

- [ ] Any software crypto implementation uses hardware acceleration
      (AES-NI/ARM Crypto Extensions) where available, rather than
      table-based software lookups, specifically to avoid cache-timing
      leakage.
- [ ] If software AES is unavoidable, the implementation is bitsliced, not
      table-based.
- [ ] For asymmetric operations, confirmed the library applies blinding by
      default (don't assume — check the library's documentation/source).
- [ ] If the deployment target has physical-proximity attacker exposure
      (embedded/smart-card/HSM), side-channel resistance is being evaluated
      by specialists with lab equipment, not assumed from software-only
      constant-time review.
- [ ] The threat model explicitly states whether physical-proximity side
      channels (power/EM) are in scope — most server/cloud deployments can
      correctly scope them out, but that should be a stated decision, not
      a silent omission.

Draft: this is an orientation-level map of a specialist field (hardware
side-channel countermeasures); actual masking/blinding implementation and
Common Criteria/FIPS side-channel evaluation require domain experts and are
out of scope for depth here.
