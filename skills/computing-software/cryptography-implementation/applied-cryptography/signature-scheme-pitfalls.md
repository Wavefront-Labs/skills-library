---
id: computing-software.cryptography-implementation.applied-cryptography.signature-scheme-pitfalls
name: signature-scheme-pitfalls
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, signatures, ecdsa, eddsa, ed25519, nonce-reuse, k-leakage, signature-malleability, low-s, strict-verification, batch-verification, rfc6979, der-encoding, replay-attacks]
level: advanced
status: docs-checked
description: "ECDSA/EdDSA implementation pitfalls: per-signature nonce k reuse and bias leaking the private key, deterministic nonces, Ed25519 malleability checks."
sources: ["https://www.rfc-editor.org/rfc/rfc6979", "https://www.rfc-editor.org/rfc/rfc8032", "https://github.com/C2SP/wycheproof", "https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Digital signature implementation pitfalls

Signing is easy to get working and easy to get catastrophically wrong. This is the failure-mode list a reviewer
checks beyond "call the sign function."

## ECDSA: the nonce (k) is as sensitive as the private key

Each ECDSA (and DSA) signature needs a fresh value k. RFC 6979 says k must be chosen randomly and uniformly using a
cryptographically secure process, and that even slight biases may be turned into attacks.

- **Reuse:** per the Trail of Bits write-up, if a signer repeats a nonce, even for different messages, the two
  signatures share the same r (so it is easy to detect) and the secret key can be recovered immediately.
- **Leakage and bias:** the same write-up covers lattice and Fourier-analysis attacks that recover keys from partial
  nonce leakage, including Minerva (timing leaks of the nonce size) and LadderLeak (less than one bit of the nonce).
- **Do not roll your own nonce generation.** RFC 6979 describes a deterministic procedure that keeps signatures
  compatible with plain ECDSA, so verifiers need not change, and removes the need for randomness at signing time.
  Randomised ECDSA is also harder to test: RFC 6979 notes automatic tests cannot reliably detect weak randomness.
- **Hedged variant:** RFC 6979 section 3.6 describes adding non-repeating additional data (for example a signature
  counter or monotonic clock) to the HMAC input as a variant, for systems with no high-quality random source. It
  calls such variants NOT "deterministic (EC)DSA", so state which one you implement.
- **Embedded and early-boot signers** are the case the RFC singles out: secure random generation is hard on smartcards
  and similar systems.

## EdDSA

RFC 8032 notes EdDSA signatures are deterministic, which protects against attacks arising from signing with bad
randomness. Key generation still needs randomness.

## Signature malleability

RFC 8032 section 8.4: Ed25519 and Ed448 signatures are not malleable because verification checks that the decoded S is
smaller than l; without that check one can add a multiple of l to the scalar part and still pass verification. Confirm
your library does this check, and do not use signature bytes as a unique identifier unless you know the scheme's
signatures are non-malleable. Check your ECDSA library's documentation for how it treats the second valid form of a
signature; it is not covered by the sources read here.

## Test with Wycheproof

The C2SP Wycheproof project provides test vectors for ECDSA and EdDSA (including Ed25519 small- and mixed-order public
keys) and for biased nonces in signature schemes. Run them against the library and parser you ship.

## Verify

- [ ] ECDSA nonces come from a library that implements RFC 6979, or a hedged variant you can name, not custom code.
- [ ] Ed25519 verification rejects S not smaller than l.
- [ ] Signature bytes are not used as a unique identifier unless malleability is excluded.
- [ ] Wycheproof vectors for your algorithm pass in CI.

## Checked

Confirmed from RFC 6979 (introduction on randomness, bias and testing; compatibility with plain ECDSA; section 3.6 variants), RFC 8032 (section 8.x text on deterministic signatures and section 8.4 malleability), the Trail of Bits "ECDSA: Handle with care" article (nonce reuse key recovery, partial-nonce attacks, Minerva, LadderLeak) and the Wycheproof README (ECDSA, EdDSA, biased nonce coverage). Removed: Sony PS3 and cryptocurrency wallet anecdotes, the claims about specific library defaults, low-S rules, DER parsing bugs and CVE references, algorithm-downgrade and domain-separation advice, and the batch-verification advice, none of which were confirmed in the pages read.

Method: docs-checked 2026-11-09 against RFC 6979 and RFC 8032 text, the Trail of Bits article and the Wycheproof README.
