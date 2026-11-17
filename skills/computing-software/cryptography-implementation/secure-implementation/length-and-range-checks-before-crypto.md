---
id: computing-software.cryptography-implementation.secure-implementation.length-and-range-checks-before-crypto
name: length-and-range-checks-before-crypto
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, point-validation, crypto-length-checks, input-validation, integer-overflow]
level: practitioner
status: docs-checked
description: "Validate lengths and ranges before calling crypto: key, nonce and tag sizes, minimum ciphertext length, RSA integer ranges and wire length fields."
sources: ["https://www.rfc-editor.org/rfc/rfc8017#section-5.1.2", "https://cwe.mitre.org/data/definitions/130.html", "https://doc.libsodium.org/secret-key_cryptography/secretbox"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Length and range checks before crypto

Crypto APIs often take a pointer and a length you supply. Wrong lengths give out-of-bounds
reads, truncated keys, or silently weaker operations.

## Check at the boundary

1. **Total length** against the format minimum before slicing. For libsodium
   `crypto_secretbox_easy`, the ciphertext holds the authentication tag followed by the
   encrypted message, so a valid `clen` is `crypto_secretbox_MACBYTES` plus the message
   length; anything shorter cannot be valid. Use the library constants
   (`crypto_secretbox_KEYBYTES`, `crypto_secretbox_NONCEBYTES`, `crypto_secretbox_MACBYTES`)
   for key, nonce and tag sizes rather than literals.
2. **Length fields read from the wire** (length-prefixed key ids, ASN.1 lengths): CWE-130
   covers parsers that mishandle a length field inconsistent with the actual data. Its
   mitigations include not letting the user control the buffer size and validating that the
   supplied length is consistent with the buffer size.
3. **Integer ranges**: RFC 8017 requires RSA primitives to reject out-of-range values.
   RSAEP requires the message representative m to be between 0 and n - 1 and otherwise
   stops with "message representative out of range". RSADP requires the same of the
   ciphertext representative c ("ciphertext representative out of range"). RSASP1 rejects
   an out-of-range message representative likewise.

## Practical rules

- Compare against the remaining buffer before reading, and guard additions of attacker-supplied
  lengths against overflow.
- Fixed-size array types make wrong-length keys a compile-time or conversion error where the
  language supports them.
- Fail decrypt-path length errors the same way as authentication failures so a distinct
  "too short" message does not become an oracle.

## Verify

- [ ] Test lengths 0, 1, boundary minus 1, boundary, boundary plus 1 and very large values.
- [ ] Every wire length field is checked against the remaining bytes.
- [ ] Key, nonce and tag sizes come from library constants.

## Checked

Method: docs-checked 2026-11-09 against doc.libsodium.org secretbox page, RFC 8017 (RSAEP, RSADP and RSASP1 range steps, section 5.1), CWE-130 (description and mitigations). Removed: the NIST SP 800-56A source (PDF not read), specific key/nonce/tag size figures for AES, GCM, ChaCha20, Ed25519 and X25519, ECDSA and DH range bounds, Node, bcrypt, PBKDF2, HKDF and OpenSSL trap examples, and language-specific slicing behaviour, none of which the read sources state.
