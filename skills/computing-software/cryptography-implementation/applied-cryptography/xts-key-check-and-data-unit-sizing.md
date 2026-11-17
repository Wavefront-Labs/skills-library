---
id: computing-software.cryptography-implementation.applied-cryptography.xts-key-check-and-data-unit-sizing
name: xts-key-check-and-data-unit-sizing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, xts-aes, ieee-1619, sp-800-38e, data-unit, ciphertext-stealing]
level: advanced
status: docs-checked
description: "Size XTS-AES data units within the SP 800-38E 2^20-block limit, know what ciphertext stealing and key sizes mean, and when XTS is the wrong mode."
sources: ["https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38e.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XTS data unit sizing

## What SP 800-38E approves
NIST SP 800-38E approves XTS-AES as specified in IEEE Std 1619-2007, subject to one extra requirement on data unit
length. XTS-AES is for protecting data on storage devices that use fixed-length data units; it was not designed for
other purposes such as encrypting data in transit.

## Data unit length
- An XTS-AES instance is defined by a secret key, a single fixed data unit length for that key, and the Enc or Dec
  procedure.
- The data unit length must not exceed 2^20 AES blocks (16 MiB at 16 bytes per block). IEEE 1619 recommends this limit; NIST
  requires it for conformance.
- An implementation may restrict data units further, for example to whole blocks only, which makes ciphertext stealing
  unnecessary.
- Ciphertext stealing is what lets the data unit end in a single non-empty partial block; XEX alone handles only whole
  128-bit blocks.
- An implementation may also restrict support to the 256-bit key (XTS-AES-128) or the 512-bit key (XTS-AES-256).
  Restricting key or data unit lengths can affect interoperability.

## What XTS does not give you
XTS provides confidentiality only. It has no authentication tag, because it was designed to encrypt without data
expansion. Without authentication or access control, NIST says it still gives more protection against manipulation of
the ciphertext than the other approved confidentiality-only modes. IEEE 1619 Annex D discusses the design choices, and
implementers should check that XTS fits their threat model.

## Checked
Date: 2026-11-09. Read in full (via pdftotext): NIST SP 800-38E. Removed as not confirmed: the FIPS 140-3 IG source (not
read) and the claim that key1 must differ from key2, the OpenSSL 3 behaviour and C snippet, the tweak and little-endian
claims, the 512/4096-byte sector sizes, the 16-byte minimum data unit, and the narrow-block leakage and "use an AEAD
for files" advice.
Method: docs-checked 2026-11-09 against NIST SP 800-38E.
