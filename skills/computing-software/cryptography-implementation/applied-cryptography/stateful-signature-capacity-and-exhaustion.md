---
id: computing-software.cryptography-implementation.applied-cryptography.stateful-signature-capacity-and-exhaustion
name: stateful-signature-capacity-and-exhaustion
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, signature-capacity, lms, xmss, stateful-signatures, sp-800-208, key-exhaustion, monitoring, firmware-signing]
level: advanced
status: docs-checked
description: "Plan and monitor LMS/XMSS signature capacity: state reuse risk, HSS levels, distributed multi-tree keys, and provisioning the next key before exhaustion."
sources: ["https://csrc.nist.gov/pubs/sp/800/208/final", "https://www.rfc-editor.org/rfc/rfc8554", "https://www.rfc-editor.org/rfc/rfc8391"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stateful signature capacity and exhaustion

RFC 8554 defines an N-time private key as exhausted when it has generated N signatures, after which it can no longer
sign. The deeper risk is reuse: if a secret key state is used twice, no cryptographic security guarantees remain and
forging a signature on a new message becomes feasible, so the schemes should only be used in systems that prevent
reuse of secret key states.

## Planning
1. Estimate signing events over the key's lifetime: releases, nightly builds, per-device images, test signatures.
2. Add a margin you can justify for growth and for indices consumed by failures; write the figure down.
3. Choose the tree height and HSS level count accordingly (HSS allows between one and eight levels per RFC 8554) and
   plan the replacement key's public key to reach devices well before exhaustion. SP 800-208 notes stateful hash-based
   signatures suit applications such as firmware-update authentication for constrained devices that cannot practically
   change their verification code after deployment.

## Monitoring
- Track the remaining-signatures count from the signing module after every signature, and alert early enough to ship
  the successor key. Pick thresholds from your own signing rate.
- Log every index used with the artifact hash; a repeated index indicates a state bug.

## Failures and copies
- Never roll the state back: a signing request that fails after the state advanced should still be treated as having
  consumed the index.
- SP 800-208 warns that simply copying a stateful private key to a backup module creates a risk of one-time key
  reuse, and it prohibits exporting private keying material from conforming modules.

## Redundancy and replacement
- SP 800-208 section 7 describes two options for module failure: several independent stateful keys on different
  modules with clients accepting any of them (public keys may be distributed using the Hash Of Root Key certificate
  extension), or one key whose one-time keys are spread over modules using a two-level HSS or XMSS^MT tree.
- In the two-level design, the top-level key only signs the roots of bottom-level trees. The module holding it is a
  single point of failure, so SP 800-208 recommends generating all bottom-level keys up front in the initial key
  generation ceremony.
- In HSS, lower-level LMS keys are replaced as they are exhausted (RFC 8554), while the level-0 root is part of the
  HSS public key, so the top tree's capacity bounds the whole key.
- Ship the successor public key in a signed update while the old key still has capacity.

## Verify
- [ ] Dashboard shows remaining capacity and projected exhaustion date.
- [ ] Signing log has no repeated index.
- [ ] Successor public key is already present in the device trust store.

## Checked

Confirmed from RFC 8554 (state reuse warning, exhaustion definition, HSS levels one to eight, level-0 root in the public key, replacement of lower-level keys) and the SP 800-208 PDF (firmware-update use case, state management warning, section 7 distributed multi-tree guidance, export prohibition). RFC 8391 (XMSS) was fetched but not read in full. Removed: the 2-4x margin and 50/75/90% alert thresholds, the HSM index-block reservation claim, and the 90-day forecast advice, which none of the pages state.

Method: docs-checked 2026-11-09 against SP 800-208 PDF and RFC 8554 text.
