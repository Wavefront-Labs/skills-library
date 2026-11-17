---
id: computing-software.cryptography-implementation.applied-cryptography.unambiguous-encoding-of-hashed-tuples
name: unambiguous-encoding-of-hashed-tuples
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-functions, hash-input-encoding, domain-separation, tuplehash, canonicalization, length-prefix, signature-malleability]
level: advanced
status: docs-checked
description: "Hash or sign multiple fields without ambiguity: length-prefixing, TupleHash, domain tags, and the concatenation bugs that let attackers shift boundaries."
sources: ["https://csrc.nist.gov/pubs/sp/800/185/final", "https://docs.aws.amazon.com/IAM/latest/UserGuide/create-signed-request.html", "https://www.rfc-editor.org/rfc/rfc9180#section-4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unambiguous encoding of hashed tuples

`H(a || b)` cannot tell `("ab", "c")` from `("a", "bc")`. When the hash
feeds a MAC, signature or KDF, an attacker who controls part of the input
can move bytes between fields and keep the same digest: `user=ad`,
`role=min...` vs `user=admin`, `role=...`.

## Encodings that work

1. **Length-prefix every field** with a fixed-width length:
   ```python
   def enc(*fields: bytes) -> bytes:
       return b"".join(len(f).to_bytes(8, "big") + f for f in fields)
   digest = sha256(b"myapp/v1/receipt\x00" + enc(user, amount, nonce)).digest()
   ```
2. **TupleHash** (SP 800-185) does the encoding inside the hash
   for you.
3. **A canonical serialisation** with typed, delimited fields where both sides
   produce identical bytes.
4. **Fixed-width fields only** (e.g. 32-byte keys) need no prefix, but
   document that every field is fixed width.

Delimiters (`|`, `\n`, `&`) only work if every field is escaped or proven
not to contain them; AWS Signature Version 4 signs a canonical request
built from the request parts.

## Domain separation

Prefix each distinct use with a constant tag (`"myapp/v1/receipt"`), so a
digest computed for one purpose is never valid for another. HPKE (RFC 9180)
prefixes `HPKE-v1` and a suite id to its extract and expand inputs.

## Where it bites

- HMAC over concatenated query parameters.
- Signing `header + payload` without separators.
- KDF `info` built by string concatenation of user-supplied ids.

## Verify

- [ ] Test: shifting a byte between two adjacent fields changes the digest.
- [ ] Each hash/MAC/KDF call site has a unique domain tag.

## Checked

- 2026-11-01. Confirmed: SP 800-185 defines TupleHash (NIST publication page); AWS Signature Version 4 creates a canonical request (AWS IAM signing page); HPKE `LabeledExtract` prefixes `HPKE-v1` and the suite id (RFC 9180).
- Removed as unconfirmed: library names for TupleHash, DER/CBOR/protobuf examples, TLS 1.3 and Noise labelling, Merkle tree note.
- The length-prefix code is an illustrative design, not a cited standard.

Method: documentation only; no commands were run.
