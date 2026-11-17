---
id: computing-software.cryptography-implementation.applied-cryptography.ecdh-public-key-validation-nist-curves
name: ecdh-public-key-validation-nist-curves
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-agreement, ecdh, ecdh-public-key-validation, p-256, p-384, invalid-curve-attack, point-validation, sp-800-56a, compressed-points]
level: sme
status: verified
description: "Validate peer public keys for ECDH on P-256/P-384/P-521 per SP 800-56A 5.6.2.3: on-curve, range and identity checks, and how to confirm your library does it."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/a/r3/final", "https://web-in-security.blogspot.com/2015/09/practical-invalid-curve-attacks.html", "https://github.com/C2SP/wycheproof"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ECDH public key validation on NIST curves

On short-Weierstrass curves (P-256, P-384, P-521), ECDH with an unvalidated
peer point lets an attacker send points on a weaker "invalid curve" and
recover your static private key a few bits at a time (Jager, Schwenk,
Somorovsky 2015: of eight libraries analysed, Bouncy Castle and Oracle's JCE were vulnerable). Validation is
mandatory whenever your key is static or reused.

## SP 800-56A Rev 3 ECC public-key validation (5.6.2.3.3 full, 5.6.2.3.4 partial)

For peer point Q = (x, y):

1. Q is not the point at infinity.
2. 0 <= x, y < p (coordinates in range).
3. y^2 = x^3 + a*x + b mod p (on the curve).
Full validation (5.6.2.3.3) adds step 4, compute n*Q and check it is the identity. Rev 3 says partial
validation (5.6.2.3.4, which omits subgroup membership) "shall only be used" for ephemeral keys, and full validation
shall be used when full validity is required for a static or ephemeral key. P-256, P-384 and P-521 have cofactor 1,
so every on-curve non-identity point already has order n and step 4 cannot fail; run the full routine anyway when an
auditor reads the standard literally.

Also check the encoding: uncompressed `04 || x || y` of the exact length;
compressed `02/03 || x` decompressed by the library (decompression implies the
on-curve check if done right). Reject hybrid `06/07` encodings.

## Does your library do it?

| Library | Validates on import? |
|---|---|
| OpenSSL 3.2.3 CLI | an off-curve public key DER fails to load (`openssl pkey -pubin`); `openssl pkey -pubin -check` prints `Key is valid` for a good key (run) |
| Go `crypto/ecdh` | Yes: `NewPublicKey` returned `P256 point not on curve` and rejected a `06` hybrid prefix (run, Go 1.26) |
| pyca 50 | Yes: `EllipticCurvePublicKey.from_encoded_point` rejected off-curve, hybrid `06`, infinity `00`, short and all-zero points (run) |
| Others (BoringSSL, Java, Web Crypto, embedded libraries) | Not checked here: read their docs and test with Wycheproof |

Do not accept affine coordinates as two separate integers from an API and
build a point yourself without the curve equation check.

In OpenSSL 3 the explicit check is `EVP_PKEY_public_check` (CLI equivalent: `openssl pkey -pubin -check`).

## Additional rules

- Prefer ephemeral keys (ECDHE): invalid-curve attacks then recover only a
  throwaway key, but still validate.
- Reject an identity/all-zero shared secret.
- Feed the shared x-coordinate into a KDF (SP 800-56C) with context.
- X25519/X448 do not need this check for private key safety; see
  `computing-software.cryptography-implementation.applied-cryptography.x25519-key-agreement`.

## Verify

- [ ] Wycheproof `ecdh_secp256r1_test.json` (in `testvectors_v1` of C2SP/wycheproof; including `InvalidPublic` cases) passes.
- [ ] Off-curve point and point-at-infinity encodings are rejected at import.
- [ ] Static ECDH keys exist only where validation is confirmed.
