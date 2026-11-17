---
id: computing-software.cryptography-implementation.applied-cryptography.detecting-ecdsa-nonce-reuse-and-bias
name: detecting-ecdsa-nonce-reuse-and-bias
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ecdsa-nonce-reuse, ecdsa, dsa, nonce-reuse, biased-nonce, lattice-attack, rfc-6979, minerva, private-key-recovery]
level: advanced
status: docs-checked
description: "Detect ECDSA/DSA nonce reuse in signature corpora, understand why bias is dangerous, and prevent both with RFC 6979 deterministic nonces."
sources: ["https://www.rfc-editor.org/rfc/rfc6979", "https://eprint.iacr.org/2019/023", "https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting ECDSA nonce reuse and bias

## Why it is fatal
RFC 6979: k must be chosen randomly and uniformly using a cryptographically secure process, and even slight biases may
be turned into attacks on the signature schemes.
- **Reuse:** two signatures made with the same k have the same r. Trail of Bits shows that the nonce k can then be
  computed from the two signatures and messages, and that the secret key follows; this holds even for different
  messages.
- **Leaked or biased bits:** lattice attacks (Howgrave-Graham and Smart, Nguyen and Shparlinski) and Fourier-analysis
  attacks recover keys from partial nonce leakage. Per the same article, the Minerva timing attacks recovered keys
  even when only the size of the nonce leaked, and LadderLeak needs less than one bit of the nonce.

## Detection in a corpus
```python
from collections import defaultdict
seen = defaultdict(list)
for sig in signatures:            # (r, s, z, pubkey)
    seen[(sig.pubkey, sig.r)].append(sig)
dups = {k: v for k, v in seen.items() if len(v) > 1}
```
Any duplicate r for the same key means the same k was used. Bias is much harder to see in a corpus; lattice-style
recovery needs many signatures and is the job of dedicated tooling, so treat timing leaks and weak RNGs as the
indicators (see the Minerva project, which could not be fetched here).

## Prevention
- Use RFC 6979 deterministic nonces, which keep signatures compatible with plain ECDSA, or a hedged variant described
  in its section 3.6 (non-repeating additional data added to the HMAC input). Do not generate k yourself.
- Keep signing time independent of the nonce: Minerva exploited timing side channels in nonce handling.
- RFC 6979 stresses that automatic tests cannot reliably detect a low-quality random source, so deterministic
  derivation removes a failure mode that tests would miss.

## Response
Treat a key with detected reuse as compromised: revoke, rotate, and audit everything it signed.

## Verify
- [ ] Signing the same message twice yields identical (deterministic) or different-but-valid (hedged) signatures,
  never identical r across different messages.
- [ ] Corpus scan finds no duplicate r per key.

## Checked

Confirmed from RFC 6979 (introduction and section 3.6 variants), the Trail of Bits "ECDSA: Handle with care" article (reuse recovery, partial-nonce attacks, Minerva, LadderLeak) and the eprint 2019/023 abstract page. The Minerva site could not be fetched. Removed: the explicit formulas for k and d, PS3 and blockchain wallet examples, the TPM-Fail and PuTTY P-521 details (9 bits, 521+64 bits), the claim that hedged nonces are the default in modern libraries, the timing-versus-bit-length detection hint, and the Ed25519 derivation sentence.

Method: docs-checked 2026-11-09 against RFC 6979 text, the Trail of Bits article and the eprint 2019/023 page.
