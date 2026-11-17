---
id: computing-software.cryptography-implementation.key-management.tr31-key-blocks-for-key-transport
name: tr31-key-blocks-for-key-transport
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, tr-31, x9-143, key-block, key-transport, payment-hsm, pci-pin, key-wrapping, kek, keyblock-header]
level: advanced
status: draft
description: "Exchange symmetric keys in ANSI X9.143/TR-31 key blocks: header fields (usage, algorithm, mode, exportability), version D, and PCI PIN key-block mandates."
sources: ["https://x9.org/standards/x9-143/", "https://docs.aws.amazon.com/payment-cryptography/latest/userguide/terminology.html", "https://listings.pcisecuritystandards.org/documents/PCI_PIN_Security_Requirements_v3.1.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TR-31 key blocks for key transport

A key block wraps a key **together with its attributes** under a KEK and MACs the whole thing, so a recipient cannot
be tricked into using a PIN key as a data key (the classic "key variant" attacks).

## Structure (ASC X9 TR-31 / ANSI X9.143)
`Header (16 chars + optional blocks) || encrypted key (with length and padding) || MAC`

Header fields:
| Field | Values (examples) |
|---|---|
| Version ID | `D` = AES key-derivation binding (use this), `B` = TDES derivation, `A`/`C` = legacy variant binding |
| Block length | total length in ASCII digits |
| Key usage | `P0` PIN encryption, `K0` key encryption/wrapping, `B0` BDK, `D0` data encryption, `M3`/`M6` MAC keys, `V2` PIN verification |
| Algorithm | `A` AES, `T` TDES, `H` HMAC |
| Mode of use | `E` encrypt only, `D` decrypt only, `B` both, `G`/`C`/`V` generate/verify MAC, `N` no restriction |
| Key version | two characters |
| Exportability | `E` exportable under a trusted KEK, `N` non-exportable, `S` sensitive |

## Operations
- Establish a KBPK (key block protection key) with the partner, usually via a key ceremony from components with
  KCVs, or via TR-34 (RSA-based remote key loading).
- Export from your HSM as a TR-31 block under the KBPK; the partner imports and the HSM enforces header attributes.
- AWS Payment Cryptography, Thales payShield, Futurex and Utimaco all import/export TR-31; specify version D and
  the exact usage/mode pair.

## Compliance
PCI PIN Security Requirement 18-3 requires keys to be conveyed and stored in key blocks, with phased deadlines for
internal storage, sharing with partners, and devices. Check the current PCI PIN version for dates.

## Gotchas
- Mismatched usage/mode combos are rejected by HSMs; agree header values in the key exchange form.
- Version A/C blocks are deprecated; do not create new ones.
- TR-31 protects key attributes, not who may request an export; HSM authorisation still matters.

## Verify
- [ ] Imported key KCV matches the sender's.
- [ ] HSM refuses to use the imported key for a usage not in its header.
