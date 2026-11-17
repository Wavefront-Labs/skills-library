---
id: computing-software.cryptography-implementation.applied-cryptography.ephemeral-vs-static-key-agreement
name: ephemeral-vs-static-key-agreement
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-agreement, ecdh, ephemeral-static-dh, forward-secrecy, sp-800-56a, c2e-2s, c1e-1s, ecies, authenticated-key-exchange]
level: advanced
status: docs-checked
description: "Choose a DH scheme by SP 800-56A class (2e/2s, 2e/0s, 1e/2s, 1e/1s, 0e/2s): freshness, identity assurance and key-compromise impersonation trade-offs."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/a/r3/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral versus static key agreement

SP 800-56A Rev. 3 classifies pair-wise discrete-log key-establishment schemes as C(ne, ms): each
party contributes ephemeral and static key pairs. Party U is the initiator; V the responder. Section 7
("Rationale for Choosing...") states the assurances of each class.

| Scheme | Keys | What the rationale says |
|---|---|---|
| C(2e, 2s) | each party: static + ephemeral | Each party gets assurance Z varies per transaction; later compromise of only their static private key does not completely reveal Z (but the static component Zs is exposed under Full Unified model or dhHybrid1). Static-key compromise lets the adversary masquerade as that entity; under Full Unified or dhHybrid1 it may let the adversary impersonate any other entity to the key holder. MQV variants limit the adversary to masquerading as the key owner. |
| C(2e, 0s) | each party: ephemeral only | Ephemeral keys destroyed after use protect Z against compromise of other transactions. No identity assurance by itself: the protocol must bind identifiers to ephemeral keys externally. No key confirmation specified. |
| C(1e, 2s) | U: static + ephemeral; V: static | Static keys give some identity assurance. U's secret varies per transaction; V's does not unless V contributes a nonce to key derivation. Compromise of V's static private key may expose secrets of past, current and future transactions in which that entity acts as V, and lets an adversary impersonate others to it. |
| C(1e, 1s) | U: ephemeral; V: static | U can identify V (as owner of the static key); V has no such assurance about U unless the protocol binds U's identifier to its ephemeral key. No assurance against private-key compromise: a compromised V static key may expose past, current and future shared secrets where it acts as V. Only V-to-U key confirmation is specified. |
| C(0e, 2s) | each party: static; U sends a nonce | Z is the same across transactions between the same static keys; the nonce used in key derivation provides freshness for U (V gets it only if V also contributes a nonce). Compromise of the static Z or static private keys can compromise keying material from past, current and future transactions. |

## Decision rules (derived from the rationale above)
- If you need protection against later static-key compromise, use a scheme with ephemeral keys on
  both sides (2e); pair it with an external identity mechanism if you use C(2e, 0s).
- One-pass schemes (1e) fit a recipient that cannot interact, but the recipient's static key is a
  long-lived liability: rotate it and keep its lifetime short.
- With static components, mix a nonce into key derivation for freshness.
- Generate ephemeral key pairs as close to the time of use as possible and destroy the private
  keys after use (the SP says this reduces compromise risk).
- Key confirmation is specified as an add-on for C(2e, 2s), C(1e, 2s), C(1e, 1s) (V to U only) and
  C(0e, 2s); not for C(2e, 0s).

## Verify
- [ ] The 56A class of your scheme is written down with its compromise properties.
- [ ] Ephemeral keys are generated per transaction and destroyed after use.
- [ ] Static-key lifetimes and rotation match the exposure window the chosen class leaves.

## Checked
Method: docs-checked 2026-11-09 against SP 800-56A Rev. 3 sections 7.1 to 7.5 (downloaded PDF, pages 113 to 119). Removed the Noise, HPKE, TLS 1.3 and Signal examples and the cached-ECDHE anecdote, which are not supported by pages read, and the forward-secrecy column, which the SP states per scheme instead.
