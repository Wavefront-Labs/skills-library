---
id: computing-software.cryptography-implementation.applied-cryptography.tokenization-versus-format-preserving-encryption
name: tokenization-versus-format-preserving-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, tokenization-vs-fpe, tokenization, format-preserving-encryption, ff1, pci-dss, pan, sp-800-38g, data-masking]
level: advanced
status: draft
description: "Decide between vault tokenization, vaultless tokenization and FF1 format-preserving encryption for PANs and IDs, with PCI DSS scope and domain-size limits."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/g/r1/ipd", "https://docs-prv.pcisecuritystandards.org/Guidance%20Document/Tokenization/Tokenization_Guidelines_Info_Supplement.pdf", "https://www.pcisecuritystandards.org/document_library/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tokenization versus format-preserving encryption

## The options
| Approach | How | Reversible by | PCI scope impact |
|---|---|---|---|
| Vault tokenization | Random token, mapping stored in a hardened vault | Vault lookup only | Systems holding only tokens can leave scope |
| Vaultless (deterministic) tokenization | Keyed function, often FF1 or a PRF over the value | Anyone with the key | Key holders stay in scope |
| FF1 FPE | Encrypt digits into digits with a key and tweak | Anyone with the key | Ciphertext is still cardholder data while the key is reachable |
| Truncation / hashing | Irreversible | Nobody | Keyed hashes of PANs need care: the PAN space is small |

## Decision rules
- If downstream systems never need the real value, use random vault tokens; they carry no mathematical link to the
  data.
- Use FF1 when you must keep length/charset (legacy schemas, test data) and cannot add a vault round trip.
- Keep the BIN (first 6-8) and last 4 in clear only if business processes need them; it shrinks the domain further.

## FF1 domain-size caution
Small domains are weak for FPE: SP 800-38G requires radix^minlen >= 100 and the 2025 Rev 1 draft raises the
minimum domain to one million and drops FF3-1 entirely; check the current revision before relying on FF3-1. A
4-digit field encrypted with FPE can be brute-forced with a codebook by anyone who sees enough pairs. Use the tweak
(e.g. the BIN, or a field identifier) so identical values in different contexts encrypt differently.

## Unsalted hashes of PANs
A SHA-256 of a 16-digit PAN with known BIN and Luhn check digit is brute-forced in minutes. If you need a lookup
key, use HMAC with a key held in an HSM or KMS, and treat that key like an encryption key.

## Gotchas
- "Format-preserving" ciphertext can be mistaken for real PANs by other systems; flag it or use an invalid Luhn.
- Detokenisation APIs are the new crown jewels: authenticate, rate-limit and audit them.

## Verify
- [ ] Data-flow diagram shows which systems hold tokens, FPE ciphertext, or keys.
- [ ] FPE domains meet the current minimum size.
- [ ] PAN lookup keys use keyed HMAC, not plain hashes.
