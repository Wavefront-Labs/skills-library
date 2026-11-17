---
id: computing-software.cryptography-implementation.applied-cryptography.encoding-the-key-agreement-shared-secret
name: encoding-the-key-agreement-shared-secret
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, shared-secret-encoding, ecdh, x25519, ffdh, leading-zeros, raccoon-attack, sp-800-56a, interop, key-agreement]
level: advanced
status: docs-checked
description: "Encode the raw shared secret Z for ECDH and finite-field DH without stripping leading zero bytes: SP 800-56A conversions, TLS 1.3 padding, Raccoon timing, OpenSSL DH padding."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/a/r3/final", "https://raccoon-attack.com/", "https://www.rfc-editor.org/rfc/rfc8446#section-7.4", "https://www.rfc-editor.org/rfc/rfc5246", "https://docs.openssl.org/3.0/man3/EVP_PKEY_CTX_ctrl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encoding the key-agreement shared secret

## Rules (SP 800-56A Rev. 3, section 5.7)
- **ECC CDH:** Z is the x-coordinate of the shared point, converted with the field-element-to-byte-string routine of
  Appendix C.2. Do not hand-roll a variable-length integer encoding; use a fixed-length one for the field.
- **Finite-field DH:** the shared value is converted with the integer-to-byte-string routine of Appendix C.1. Pad to
  the length of the prime p rather than stripping leading zero bytes.
- If the primitive fails (for example the point is the point at infinity), abort and destroy intermediates.

## Why padding matters
- Interop: if one library strips leading zero bytes and the other keeps them, the two sides derive different keys in
  the cases where Z starts with a zero byte, giving intermittent, hard-to-reproduce handshake failures.
- Timing: TLS 1.2 DHE stripped leading zero bytes of the premaster secret (RFC 5246, section 8.1.2), so key
  derivation ran over inputs of varying length; the Raccoon attack used that timing difference. TLS 1.3 encodes the
  shared secret big-endian and left-padded with zeros to the field size (RFC 8446, section 7.4.1). The Raccoon
  authors note ECDHE already preserved leading zeros, and that ephemeral keys should not be reused.

## Library behaviour to check
- OpenSSL: `EVP_PKEY_CTX_set_dh_pad(ctx, 1)` pads the DH shared secret with zeros up to the size of p; the default
  (0) performs no padding.
- For any other library, test it with a vector whose Z begins with a zero byte instead of assuming.

## Then
Feed Z into a key-derivation function with context (see SP 800-56C); never use Z directly as a key.

## Verify
- [ ] A unit test with a known vector where Z starts with 0x00 derives the same key on both implementations.
- [ ] Every code path that serialises Z uses the fixed-length conversion.

## Checked
2026-11-01. Confirmed: NIST SP 800-56A Rev. 3 (PDF) sections 5.7.1.1 and 5.7.1.2 use Appendix C.1 and C.2
conversions and the error handling above; RFC 8446 section 7.4.1 (left-padded with zeros); RFC 5246 section 8.1.2
(leading zero bytes stripped); raccoon-attack.com FAQ (stripping, timing, TLS 1.3 preserves, no key reuse); OpenSSL
`EVP_PKEY_CTX_set_dh_pad`. Removed: per-curve byte lengths, interop failure rates, X25519/X448 handling, handshake
counts, and the Java, pyca and Web Crypto rows (not in fetched sources).
Method: documentation only; no commands were run.
