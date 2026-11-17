---
id: computing-software.cryptography-implementation.applied-cryptography.lms-xmss-stateful-signatures
name: lms-xmss-stateful-signatures
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-based-signatures, lms-xmss, lms, hss, xmss, sp-800-208, rfc8554, rfc8391]
level: sme
status: docs-checked
description: "LMS/HSS and XMSS stateful hash-based signatures: the state-reuse rule, LMS tree heights and Winternitz w trade-off, HSS levels, and what the RFCs require."
sources: ["https://csrc.nist.gov/pubs/sp/800/208/final", "https://datatracker.ietf.org/doc/html/rfc8554", "https://datatracker.ietf.org/doc/html/rfc8391"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LMS and XMSS stateful signatures

LMS (RFC 8554) and XMSS (RFC 8391) are stateful hash-based signature schemes; NIST SP 800-208 specifies LMS and XMSS and
their multi-tree variants HSS and XMSS^MT.

## The state rule
Both RFCs state that the secret key changes over time and that if a secret key state is used twice, no cryptographic security
guarantees remain, and it becomes feasible to forge a signature on a new message. RFC 8554 says developers should not use
these schemes except in systems that prevent the reuse of secret key states. Because of the state, classical signature
APIs cannot be used unmodified: the API must let signature generation update the secret key state.

In XMSS the private key holds an index that is updated with every signature generation and points to the next unused WOTS+
key pair, starting at index 0 at the leftmost leaf.

## LMS parameters (RFC 8554)
- Tree height h in `LMS_SHA256_M32_H5`, `H10`, `H15`, `H20`, `H25` (SHA-256, 32-byte hashes). A tree of height h holds 2^h
  one-time key pairs.
- LM-OTS Winternitz parameter w in `LMOTS_SHA256_N32_W1`, `W2`, `W4`, `W8`. Increasing w shrinks the signature but increases
  the time to generate the public key and to sign and verify.

| LM-OTS set | w | p | OTS signature length (bytes) |
|---|---|---|---|
| LMOTS_SHA256_N32_W1 | 1 | 265 | 8516 |
| LMOTS_SHA256_N32_W2 | 2 | 133 | 4292 |
| LMOTS_SHA256_N32_W4 | 4 | 67 | 2180 |
| LMOTS_SHA256_N32_W8 | 8 | 34 | 1124 |

An LM-OTS signature is 4+n*(p+1) bytes; public key generation takes p*(2^w - 1) + 1 hash computations, and signing and
verifying take roughly half that on average.

## HSS levels (RFC 8554)
- The number of levels L is between one and eight. Each tree has its own key pair and identifier, generated independently of
  all others; the top tree signs the public keys of the next level.
- HSS with L=1 is essentially LMS with a fixed field prepended, and all implementations MUST support HSS for
  interoperability.
- Levels may use different parameter sets (for example H15 at the root and H10 below), but the signer MUST NOT change the
  parameter set used for a specific level over time.
- An N-time private key is exhausted after N signatures.

## Verify
- [ ] The signing API can persist updated key state; no copy of a key can sign independently.
- [ ] Verification code passes the test cases in RFC 8554 Appendix F.

## Checked
Date: 2026-11-09. Read: RFC 8554 (security considerations, section 4 table, section 6 HSS, parameter registry) and the
relevant stateful-scheme passages of RFC 8391; the SP 800-208 page is only an abstract. The CNSA 2.0 PDF returned 403 and
was dropped. Removed as not confirmable from those pages: the hardware module (FIPS 140 level 3) requirement, the 192-bit
and SHAKE parameter sets, signature budget advice, example signature sizes, library support list, counter-persist ordering,
backup and snapshot guidance, and the CNSA 2.0 claim.
Method: docs-checked 2026-11-09 against RFC 8554, RFC 8391 and the SP 800-208 abstract page.
