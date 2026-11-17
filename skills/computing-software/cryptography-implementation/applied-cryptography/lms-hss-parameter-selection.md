---
id: computing-software.cryptography-implementation.applied-cryptography.lms-hss-parameter-selection
name: lms-hss-parameter-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, hss-parameters, lms, hss, rfc-8554, winternitz, stateful-signatures, firmware-signing]
level: advanced
status: docs-checked
description: "Select LMS/HSS tree heights, levels and Winternitz parameters (RFC 8554) for firmware signing: signature counts, signature sizes and why large capacity uses HSS."
sources: ["https://www.rfc-editor.org/rfc/rfc8554"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LMS/HSS parameter selection

## Parameters (RFC 8554, SHA-256 with n=32)
- **LMS tree height H**: 5, 10, 15, 20 or 25 (`LMS_SHA256_M32_H5` ... `H25`). One tree signs `2^H` messages.
- **LM-OTS Winternitz w**: 1, 2, 4 or 8 (`LMOTS_SHA256_N32_W1` ... `W8`). Larger w gives smaller signatures at the
  cost of more hashing per chain.
- **HSS levels L**: a tree of trees; total capacity is `2^(H1 + H2 + ... + HL)`. Only the root tree must be generated
  before the public key is distributed, which makes large capacity practical (RFC 8554 section 6). Levels may use
  different LMS parameter sets.
- The state (which one-time key is next) must never be reused or rolled back; see the stateful-signature skills.

## Sizes (RFC 8554, SHA-256, n=32)
LM-OTS signature sizes from the section 4 table: w=1 8516 bytes, w=2 4292, w=4 2180, w=8 1124. An LMS signature adds
the leaf number, the type fields and an authentication path of `H` 32-byte hashes, so LMS H=10, w=8 is
`1124 + 8 + 32*10` = 1452 bytes. An HSS signature with L levels carries L LMS signatures and L-1 signed public keys.

## Picking for firmware
| Need | Suggestion |
|---|---|
| Few hundred releases over product life | Single LMS H=10, w=8 (1024 signatures) |
| CI signing nightly builds for a decade | HSS L=2, H=10/10 (1,048,576 signatures) |
| Verifier on a tiny bootloader | w=4 (bigger signature than w=8, fewer hash steps per chain) |

Key generation cost grows with `2^H` of the tree(s) that must be built up front, so prefer HSS over a single very tall
tree for large capacity.

## Implementation
- Verification is simple and stateless; bootloaders often embed a small verifier.
- Check any implementation against the RFC 8554 Appendix F test cases.
- Where approved-use rules apply (for example NIST SP 800-208), read the current publication for module and
  parameter requirements rather than relying on this summary.

## Verify
- [ ] Capacity covers planned signatures with a margin.
- [ ] Bootloader verify time and signature size measured on target hardware.
- [ ] RFC 8554 Appendix F test vectors pass.

## Checked
2026-11-01. Confirmed against RFC 8554: parameter-set tables for LM-OTS (section 4, sizes 8516/4292/2180/1124) and
LMS (section 5, H5 to H25), HSS key structure and signature layout (section 6), Appendix F test cases. Removed:
SP 800-208 parameter and hardware-module claims, CNSA 2.0 remark, the 1 to 8 level range, key-generation timings, and
named vendor libraries and versions.
Method: documentation only; no commands were run.
