---
id: computing-software.cryptography-implementation.applied-cryptography.ff1-format-preserving-encryption
name: ff1-format-preserving-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, storage-encryption-modes, format-preserving-encryption, ff1, ff3-1, sp-800-38g, tokenization, pan-encryption, radix, tweak]
level: sme
status: docs-checked
description: "Apply NIST FF1 format-preserving encryption to card numbers and IDs: domain-size minimums, radix and tweak choice, determinism leakage, and when tokenization is better."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/g/r1/ipd", "https://csrc.nist.gov/pubs/sp/800/38/g/final", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38G.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FF1 format-preserving encryption

FPE encrypts a string over an alphabet (radix) into another string of the same
length and alphabet: a 16-digit PAN becomes another 16-digit number, so legacy
schemas, validators and fixed-width files keep working. SP 800-38G (2016) specifies
FF1 and FF3; Draft Revision 1 updates FF1 and FF3-1 (smaller FF3-1 tweak) and
makes the minimum domain size mandatory. FF1 supports a greater range of data
lengths and a variable-length tweak, so prefer it.

## Parameters

- **Key**: an approved block cipher key (AES).
- **Radix** r: 10 for digits, larger for letters; map characters yourself to
  numerals 0..r-1 and keep fixed parts (separators, BIN prefix) outside the
  encrypted portion.
- **Length** n: the 2016 text requires radix^minlen >= 100 and recommends at
  least one million; Draft Rev 1 makes a domain size of one million the minimum
  for FF1 and FF3-1. For digits that is six digits. Small domains (4-digit PINs,
  3-digit CVVs) are not safe with FPE at all.
- **Tweak**: not necessarily secret, variable length in FF1. Put context in it
  (tenant id, column name, the unencrypted BIN and last-4 when you keep those
  clear) so identical values in different contexts map differently.

## The leakage you accept

FF1 is deterministic for a given key and tweak: equal plaintexts give equal
ciphertexts. That is often the point (joins, dedup), but frequency analysis
works on low-entropy fields (gender codes, countries, small enums) - never FPE
those. There is no integrity; any same-format string decrypts to something.

## Practical layout for a PAN

Keep the BIN and last 4 digits in clear, encrypt the middle digits with the
clear parts as tweak. If you also need a valid Luhn check digit, encrypt the
digits before it and recompute the check digit, rather than encrypting all 16
and hoping.

## FPE or tokenization?

Tokenization (random token, vault lookup) leaks nothing about the value, and
de-tokenization is an access-controlled service call. FPE needs no vault but
anyone with the key can decrypt everything offline. Choose FPE when a vault is
impractical and key custody is strong (HSM).

## Verify

- [ ] Implementation passes the NIST sample vectors for FF1.
- [ ] Every encrypted domain meets the one-million minimum.
- [ ] Tweak includes context; key is in an HSM/KMS.
- [ ] Low-cardinality fields are excluded from FPE.

## Checked
2026-11-01. Confirmed in SP 800-38G (FF1 and FF3 defined; radix^minlen >= 100; tweak not necessarily secret; FF1
wider length range and flexible tweak length) and the NIST Draft Rev 1 notice (FF1 and FF3-1; one million minimum
domain size; smaller FF3-1 tweak). Removed: the claim that Rev 1 withdraws FF3-1, library and cloud-product names,
PCI scope statements and the AES key-size list.
Method: documentation only; no commands were run.
