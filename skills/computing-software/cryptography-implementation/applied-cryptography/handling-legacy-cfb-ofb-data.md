---
id: computing-software.cryptography-implementation.applied-cryptography.handling-legacy-cfb-ofb-data
name: handling-legacy-cfb-ofb-data
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, block-cipher-modes, sp-800-38a, cfb-ofb-legacy, cfb, cfb8, ofb, legacy-decryption, interop, migration]
level: advanced
status: docs-checked
description: "Decrypt and migrate data encrypted with CFB/CFB8/OFB: matching segment sizes across libraries, IV rules for each mode, and moving to AEAD."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/a/final", "https://docs.openssl.org/3.0/man1/openssl-enc/", "https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling legacy CFB and OFB data

You meet CFB and OFB in old file formats and embedded protocols. SP 800-38A defines them as confidentiality modes only;
they do not authenticate. The job is usually: decrypt correctly, then re-encrypt under an AEAD.

## Get the parameters exactly right

| Parameter | What varies |
|---|---|
| Segment size s | CFB has 1-bit, 8-bit and full-block (128-bit for AES) variants; SP 800-38A gives test vectors for CFB1, CFB8 and CFB128. OpenSSL `enc` lists ciphers such as `aes-128-cfb1`; pyca/cryptography has `modes.CFB` and `modes.CFB8` ("the CFB8 variant uses an 8-bit shift register"). |
| IV | Block size; where it is stored (prefix, header field, derived) |
| Padding | Check whether the legacy code padded anyway |
| Key derivation | For `openssl enc` files made from a passphrase, the key and IV come from the password via the `-md`, salt and iteration options; the first bytes of the data hold the salt when it was generated randomly |

If a decrypt produces garbage, vary one parameter at a time (segment size, IV placement, key derivation) and test each
candidate against a known plaintext header (magic bytes, JSON `{`, XML `<?xml`).

## IV rules differ

- **CFB**: SP 800-38A says the IV need not be secret but must be unpredictable (Appendix C gives two methods:
  encrypt a nonce with the forward cipher, or use a FIPS-approved random number generator).
- **OFB**: the IV must be a nonce, unique for each execution of the mode under the key; it need not be unpredictable.
  Legacy OFB data that reused an IV under one key breaks that requirement; treat it as exposed.
- Neither mode authenticates, so flipped ciphertext bits are not detected.

## Migration recipe

1. Write a decrypt-only adapter and test it with the SP 800-38A example vectors (F.3 for CFB, F.4 for OFB) for the
   exact segment size used.
2. Add an authenticity check you can still do: if the legacy format had a checksum or MAC, verify it; otherwise flag the
   records as unauthenticated.
3. Re-encrypt to an AEAD such as AES-GCM with a new key and a versioned format.
4. Remove encrypt support for CFB/OFB immediately; keep decrypt until the legacy count is zero.

## Verify

- [ ] Adapter passes SP 800-38A vectors for the exact segment size used.
- [ ] Known-header check decrypts a sample of real records correctly.
- [ ] No new data is written with CFB/OFB.
- [ ] OFB data with reused IVs is documented as exposed.

## Checked

Confirmed from the SP 800-38A PDF (CFB and OFB definitions, CFB1/CFB8/CFB128 and OFB example vector sections F.3 and F.4, CFB IV unpredictable, OFB IV a nonce, Appendix C IV generation), the OpenSSL 3.0 `openssl enc` page (cipher list with cfb1, -md, -salt, salt stored in the first bytes) and the pyca/cryptography modes page (CFB, CFB8, OFB). Removed: the OpenPGP and SNMPv3 examples, the Java and OpenSSL "default segment size" mappings, the claim that CFB8 and CFB128 agree on the first byte, the wrong-IV symptom, the XOR-of-first-segments remark, the EVP_BytesToKey/MD5 statement and the XChaCha20 suggestion, none of which were on the pages read.

Method: docs-checked 2026-11-09 against SP 800-38A PDF, the OpenSSL enc page and the pyca/cryptography modes page.
