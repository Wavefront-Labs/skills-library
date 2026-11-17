---
id: computing-software.cryptography-implementation.applied-cryptography.finding-and-removing-ecb-mode
name: finding-and-removing-ecb-mode
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, block-cipher-modes, sp-800-38a, ecb-mode-detection, ecb, aes-ecb, code-audit, semgrep, migration, aes-gcm]
level: practitioner
status: docs-checked
description: "Find ECB mode in a codebase, prove it from ciphertext, and migrate stored data to an AEAD without a flag day."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/a/final", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/security/standard-names.html", "https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding and removing ECB mode

ECB encrypts each block independently, so identical plaintext blocks always give identical ciphertext blocks, which
can leave significant patterns in the output (pyca/cryptography). OWASP says ECB should not be used outside of very
specific circumstances, and the Java standard names page says it generally should not be used for multiple blocks of
data. SP 800-38A lists ECB as a confidentiality mode; it provides no integrity.

## Where ECB hides

| Source | Pattern |
|---|---|
| Java JCA | Transformation strings such as `AES/ECB/PKCS5Padding` or `AES/ECB/NoPadding`, and `DESede/ECB/...` |
| Python pyca | `modes.ECB()` |
| OpenSSL command line | `aes-128-ecb`, `aes-192-ecb`, `aes-256-ecb` in `openssl enc` |
| Hand-rolled | A raw block-cipher call inside a loop over block-sized chunks |

Search:

```bash
rg -n -i 'AES/ECB|MODE_ECB|modes\.ECB|_ecb\(|aes-(128|192|256)-ecb|DESede/ECB' .
```

Also check for a bare algorithm name where the library picks the mode for you: look up your provider's default
transformation in its documentation rather than assuming it. Calls of a raw block function inside a loop are ECB
written by hand, and a grep for mode names misses them.

## Proving ECB from data

If you only have ciphertext (for example a database column), split each value into block-sized pieces (16 bytes for
AES) and count duplicates. Repeated blocks inside long, structured plaintext are strong evidence of ECB.

```python
def ecb_score(ct: bytes) -> int:
    blocks = [ct[i:i+16] for i in range(0, len(ct) - len(ct) % 16, 16)]
    return len(blocks) - len(set(blocks))
```

Also look for equal plaintexts encrypting to equal ciphertexts across rows, and lengths always a multiple of the block
size with no IV prefix.

## Migration

1. Introduce a versioned format: new writes use an AEAD such as AES-GCM with a fresh key, prefixed with a version byte.
2. Read path: version byte present means AEAD; no prefix means legacy ECB.
3. Re-encrypt in the background (decrypt ECB, encrypt AEAD), lazily on read or in a batch job.
4. When the legacy count reaches zero, delete the ECB decrypt code and retire the old key.

Use a new key for the AEAD; do not reuse the ECB key across modes. If ECB was used to get deterministic ciphertext for
equality lookups, plan a separate design for that (for example a keyed-hash lookup column) rather than keeping ECB.

## Verify

- [ ] Grep and semgrep return no ECB usages.
- [ ] Duplicate-block score is zero for new ciphertexts of repetitive plaintext.
- [ ] Legacy-record counter is tracked and reaches zero before ECB code is removed.
- [ ] Equality-search needs moved to a different design, not left on ECB.

## Checked

Confirmed from the OWASP Cryptographic Storage Cheat Sheet ("ECB should not be used outside of very specific circumstances"), the Java 21 standard names page (ECB note, `AES/ECB/NoPadding`, `AES/ECB/PKCS5Padding`, `DESede/ECB/...`), the pyca/cryptography symmetric-encryption page (`modes.ECB`, identical blocks leave patterns) and the OpenSSL `enc` cipher list (`aes-[128|192|256]-ecb`); SP 800-38A PDF lists ECB among its confidentiality modes. Removed: the claim that `Cipher.getInstance("AES")` resolves to ECB, the .NET, Node, MySQL, PyCryptodome and EVP C rows, the SP 800-38F key-wrap remark, the 2^-128 repeat probability, XChaCha20-Poly1305 and AES-SIV suggestions, none of which were on the pages read.

Method: docs-checked 2026-11-09 against SP 800-38A PDF, OWASP Cryptographic Storage Cheat Sheet, Java 21 standard names, pyca/cryptography modes page and OpenSSL enc page.
