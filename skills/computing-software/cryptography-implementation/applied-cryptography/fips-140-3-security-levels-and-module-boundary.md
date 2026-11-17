---
id: computing-software.cryptography-implementation.applied-cryptography.fips-140-3-security-levels-and-module-boundary
name: fips-140-3-security-levels-and-module-boundary
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, fips-140, fips-140-3, fips-security-levels, cryptographic-boundary, iso-19790, compliance]
level: advanced
status: draft
description: "Read and choose FIPS 140-3 security levels 1-4 and define a module's cryptographic boundary so what you claim as validated matches what the certificate covers."
sources: ["https://csrc.nist.gov/pubs/fips/140-3/final", "https://csrc.nist.gov/projects/cryptographic-module-validation-program/fips-140-3-standards", "https://csrc.nist.gov/projects/cryptographic-module-validation-program/fips-140-3-ig-announcements"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FIPS 140-3 security levels and module boundary

FIPS 140-3 points at ISO/IEC 19790:2012 (requirements) and ISO/IEC 24759 (test methods), with NIST
SP 800-140A..F and the CMVP Implementation Guidance (IG) layered on top. Before you claim "we use
FIPS 140-3 crypto", pin down two things: the **level** and the **boundary**.

## The four levels (what changes as you go up)
| Level | Physical security | Authentication | Typical module |
|---|---|---|---|
| 1 | Production-grade parts, nothing more | None required | Software libraries (OpenSSL FIPS provider, BoringCrypto, AWS-LC, Go native) |
| 2 | Tamper **evidence** (seals, coatings) | Role-based | Hardened appliances, some software modules on a validated OS |
| 3 | Tamper **resistance** with detection/response (zeroise on open) | Identity-based; plaintext CSPs entered via trusted path or split | Network HSMs, cloud HSMs (CloudHSM, Azure Managed HSM) |
| 4 | Full envelope protection, environmental failure protection/testing (voltage, temperature) | Multi-factor identity-based | Highest-assurance HSMs |

The **overall** level is the lowest level achieved across the 11 areas (module specification,
interfaces, roles/services/authentication, software/firmware security, operational environment,
physical security, non-invasive security, SSP management, self-tests, life-cycle assurance,
mitigation of other attacks). A certificate reads like "Overall Level 3" with per-area
levels in the security policy table; one area at Level 2 makes the whole module Level 2.

## Module types and the boundary
- Module embodiment: software, firmware, hardware, hybrid-software, hybrid-firmware.
- The **cryptographic boundary** is drawn in the Security Policy: a list of files (e.g. `fips.so`
  plus its integrity MAC), or a chip, or a whole chassis. Only code inside it is validated.
- For a software module the boundary is the binary; the **Tested Operational Environment (OE)**
  (OS + CPU, with/without AES-NI/ARMv8 crypto extensions) is listed on the certificate. Running on
  a different OE may be allowed as vendor-affirmed under the IG; check the current IG text before
  relying on that for an audit.
- Anything outside the boundary (your TLS stack, your KDF wrapper, the language binding) is not
  validated even if it only calls validated primitives. Say "uses a FIPS 140-3 validated module
  (cert #NNNN)", not "is FIPS validated".

## Choosing a level for a requirement
1. Read the actual requirement: FedRAMP / CMMC / CJIS usually require "FIPS-validated
   cryptography" for data protection, which a Level 1 software module meets.
2. Key custody requirements (CA root keys, payment HSMs, "keys never in software") push you to
   Level 3 hardware. Payment uses PCI PTS HSM in addition.
3. Map each key to where it lives: application keys in a Level 1 library, KEKs/root keys in a
   Level 3 HSM, envelope encryption between them.

## Gotchas
- A cloud KMS's certificate covers its HSM fleet, not the client SDK on your host.
- "FIPS mode" toggles are not validation. The certificate number and the Security Policy are.
- Physical security levels say nothing about side channels on shared hosts; non-invasive security
  is a separate area and is often "N/A" for software.

## Verify
- [ ] You can name the certificate number, overall level and the boundary files for every module.
- [ ] Your OS/CPU appears in the certificate's tested OE list (or the vendor-affirmation rule is documented).
- [ ] Code outside the boundary only calls approved services of the module.
