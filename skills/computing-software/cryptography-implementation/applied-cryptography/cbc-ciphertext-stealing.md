---
id: computing-software.cryptography-implementation.applied-cryptography.cbc-ciphertext-stealing
name: cbc-ciphertext-stealing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, block-cipher-modes, sp-800-38a, ciphertext-stealing, cbc-cs1, cbc-cs3, kerberos, length-preserving-encryption]
level: advanced
status: verified
description: "Use CBC ciphertext stealing (CBC-CS1/2/3) when ciphertext must equal plaintext length: choosing the variant, Kerberos CS3 interop, and minimum-length limits."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/a/addendum/final", "https://datatracker.ietf.org/doc/html/rfc3962", "https://datatracker.ietf.org/doc/html/rfc8009"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CBC ciphertext stealing

Ciphertext stealing (CTS) lets CBC handle any length >= one block without
padding, so ciphertext length equals plaintext length. The SP 800-38A addendum
defines three variants that differ only in the order of the last two blocks.

| Variant | Last two ciphertext blocks | Used by |
|---|---|---|
| CBC-CS1 | partial block last, natural order | NIST reference |
| CBC-CS2 | swap only if the last block is partial | cited in the addendum as specified elsewhere (its Ref. [3]) |
| CBC-CS3 | always swapped (Kerberos style) | Kerberos AES (RFC 3962, RFC 8009) |

Pick the variant your peer uses; they are not interoperable. The SP 800-38A addendum
says CBC-CS3 is the Kerberos 5 variant and CBC-CS1 was a suggestion on the NIST CSRC site.
For input that is a whole number of blocks: CS1 and CS2 equal plain CBC (run), CS3 swaps the last two blocks.

## When to use it

- Length-preserving fields (fixed-size records, sector-like layouts) where a
  padding block does not fit.
- Interop with Kerberos enctypes `aes256-cts-hmac-sha1-96` and
  `aes256-cts-hmac-sha384-192`.

For new storage designs prefer XTS (sectors) or an AEAD with an explicit
length field. CTS still needs a MAC: Kerberos pairs it with HMAC.

## Constraints and gotchas

- Plaintext must be at least 16 bytes. RFC 3962 section 5: exactly one block is
  just AES-ECB of that block, and shorter input is padded to a block (padding
  bits unspecified; the protocol must not rely on them).
- Exactly-one-block-multiple inputs: CS1 is plain CBC; CS3 still swaps the last
  two blocks. Test both partial and full final blocks.
- IV rules are those of CBC: unpredictable per message (Kerberos uses a zero IV
  with a random confounder block prepended instead).
- Few high-level libraries expose CTS. OpenSSL 3 has `AES-128-CBC-CTS`, `AES-192-CBC-CTS`
  and `AES-256-CBC-CTS` with a `cts_mode` parameter (`CS1`, `CS2`, `CS3`; set it via
  `EVP_CIPHER_CTX_set_params` with the UTF-8 string, per the EVP_EncryptInit man page). The default is CS1:
  `openssl enc -aes-128-cbc-cts` (3.2.3) output matched a CS1 reimplementation for
  17, 31, 47 and 100 byte inputs (and CS1/CS2 for 32, 48, 64). pyca exposes no CTS mode.
  Do not hand-roll it if a vetted implementation exists; to test one, use the vectors below.
  The C `cts_mode` call itself was not compiled here (no C compiler).

## Verify

- [ ] Variant matches the peer and is written in the format spec.
- [ ] Vectors pass: RFC 3962 Appendix B for CS3 (all five CBC-CTS vectors, 17 to 48 bytes, matched by a CS3 reimplementation here), SP 800-38A addendum examples for CS1.
- [ ] Inputs of length 16, 17, 31, 32 and 33 all round-trip.
- [ ] A MAC covers the ciphertext.
