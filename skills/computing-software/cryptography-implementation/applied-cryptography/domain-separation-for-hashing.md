---
id: computing-software.cryptography-implementation.applied-cryptography.domain-separation-for-hashing
name: domain-separation-for-hashing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, hash-domain-separation, domain-separation, context-strings, cshake, blake2-personalization, cross-protocol-attack, hkdf-info]
level: advanced
status: docs-checked
description: "Prevent cross-protocol collisions by domain-separating hashes, MACs, KDFs and signatures with context strings, prefixes, cSHAKE or BLAKE2 personalisation."
sources: ["https://csrc.nist.gov/pubs/sp/800/185/final", "https://www.rfc-editor.org/rfc/rfc9380#section-3.1", "https://www.rfc-editor.org/rfc/rfc8032", "https://docs.python.org/3/library/hashlib.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain separation for hashing

**Problem:** the same key or hash is used for two purposes, and a value valid in one context becomes valid in
another (a signed login challenge accepted as a signed payment, a MAC on a cookie reused as an API token).

## Techniques by primitive
| Primitive | Separation mechanism |
|---|---|
| SHA-2 / SHA-3 | Prefix a fixed, unique, length-prefixed tag: `H(len(tag) || tag || encode(data))` |
| cSHAKE (SP 800-185) | cSHAKE is the customizable SHAKE variant: use its customisation string |
| BLAKE2 | `person` (up to 16 bytes for BLAKE2b, 8 for BLAKE2s) and `salt` parameters |
| Signatures | Ed25519ctx context string (RFC 8032), or a tag inside the signed structure |

## Choosing tags
- Make tags globally unique and versioned: `"com.example.payments.receipt.v1"`. RFC 9380 calls these DSTs and says
  they should begin with a fixed application-unique string, include a version number, and (with several ciphersuites)
  a ciphersuite identifier; it recommends at least 16 bytes.
- Length-prefix or fix-length the tag so `tag || data` is unambiguous.
- Keep a registry (one file) of every tag in the codebase; review new ones.

## Example
```python
import hashlib
def h(tag: str, *parts: bytes) -> bytes:
    m = hashlib.sha256()
    t = tag.encode()
    m.update(len(t).to_bytes(2, "big") + t)
    for p in parts:
        m.update(len(p).to_bytes(8, "big") + p)
    return m.digest()
leaf = h("example.log.leaf.v1", record)
```
With BLAKE2b: `hashlib.blake2b(data, person=b"exmpl-receipt-v1")` (person is at most 16 bytes).

## Gotchas
- Domain separation does not replace key separation; still derive separate keys per purpose.
- Changing a tag is a breaking change; version it rather than editing it.
- Pure Ed25519 takes no context string (Ed25519ctx and Ed25519ph do); put the context inside the message.

## Checked
2026-11-01. Confirmed: RFC 9380 section 3.1 (DST requirements, 16-byte minimum recommendation); RFC 8032
(Ed25519ctx, Ed25519ph); Python hashlib docs (blake2 `person`, `salt`, 16 bytes for BLAKE2b, 8 for BLAKE2s);
SP 800-185 abstract (cSHAKE is customizable). Removed: ML-DSA context, HKDF `info` and HMAC key-derivation rows
(no source fetched). The Python example is illustrative design code, not a sourced claim.
Method: documentation only; no commands were run.

## Verify
- [ ] grep finds no raw `sha256(data)` used for security decisions without a tag.
- [ ] Tag registry has no duplicates.
- [ ] Cross-context test: a value produced for context A fails verification in context B.
