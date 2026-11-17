---
id: computing-software.cryptography-implementation.applied-cryptography.encrypt-then-mac-composition
name: encrypt-then-mac-composition
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, message-authentication-code, encrypt-then-mac, encrypt-then-mac-composition, aes-cbc-hmac, key-separation, rfc-7518]
level: advanced
status: docs-checked
description: "Build encrypt-then-MAC correctly when an AEAD is unavailable: separate keys, MAC over header, IV, ciphertext and AD length, verify before decrypt."
sources: ["https://www.rfc-editor.org/rfc/rfc7518#section-5.2", "https://www.rfc-editor.org/rfc/rfc7366", "https://datatracker.ietf.org/doc/html/draft-mcgrew-aead-aes-cbc-hmac-sha2-05"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composing encrypt-then-MAC correctly

Use an AEAD (AES-GCM, ChaCha20-Poly1305) when you can. EtM is for formats or
platforms that only offer CBC/CTR plus HMAC, or to interoperate with
JWE `A128CBC-HS256` / TLS `encrypt_then_mac` (RFC 7366).

## The construction (as in RFC 7518 5.2)

```
enc_key, mac_key = HKDF(master, info="v1 enc"), HKDF(master, info="v1 mac")   # RFC 7518 instead splits one key K
iv  = random(16)
ct  = AES-CBC(enc_key, iv, PKCS7(plaintext))
AL  = uint64_be(len(aad) * 8)                                  # AAD length in bits, 64-bit big-endian
tag = HMAC-SHA-256(mac_key, aad || iv || ct || AL)[:16]         # A128CBC-HS256: first T_LEN=16 octets
out = header || iv || ct || tag
```

RFC 7518 section 5.2 defines the MAC input as `A || IV || E || AL` with PKCS7 CBC, truncating the HMAC output to
T_LEN octets (16 for A128CBC-HS256, 24 for the SHA-384 variant). It splits a single key K into MAC_KEY (initial
octets) and ENC_KEY (final octets); the HKDF split above is a local alternative.

Decrypt:

1. Parse lengths, reject malformed sizes.
2. Recompute the tag over exactly `aad || iv || ct || AL`.
3. Compare in constant time. On mismatch, return one generic error.
4. Only then decrypt and unpad.

## Rules that break if skipped

- **Separate keys.** Use distinct MAC and encryption keys, as RFC 7518 does.
- **MAC the IV and header.** The RFC 7518 MAC covers the AAD, IV, ciphertext and AL.
- **Length-encode AD** (the AL field) so `aad || iv` boundaries are unambiguous.
- **Verify before decrypt/unpad.** Compare the tag in constant time and fail with
  one generic error.
- **Keep tags at 128 bits or more**, as in A128CBC-HS256.

## Pitfalls

- MAC-then-encrypt is the TLS/DTLS default that RFC 7366 replaces with the
  `encrypt_then_mac` extension; do not build new formats that way.
- Check that a library's "AES-CBC with HMAC" MACs the IV and AAD, not only the ciphertext.

## Verify

- [ ] RFC 7518 Appendix B test cases pass if implementing the AES_CBC_HMAC_SHA2 algorithms.
- [ ] Modifying IV, header, ciphertext or AD each causes rejection before decryption.
- [ ] Padding errors and MAC errors are indistinguishable to callers.

## Checked

2026-11-01. Confirmed in RFC 7518 section 5.2 (MAC_KEY/ENC_KEY split, `A || IV || E || AL`, AL in bits, T_LEN=16
for A128CBC-HS256, Appendix B test cases) and RFC 7366 (encrypt_then_mac extension replacing MAC-then-encrypt).
Fixed: the tag was truncated to 32 octets, the RFC value is 16 for HS256. Removed: Lucky 13/POODLE attribution,
the "same key is a known pitfall" and AES-CTR claims, unconfirmed by the cited pages.
Method: documentation only; no commands were run.
