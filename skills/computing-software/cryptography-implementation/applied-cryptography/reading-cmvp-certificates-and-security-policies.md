---
id: computing-software.cryptography-implementation.applied-cryptography.reading-cmvp-certificates-and-security-policies
name: reading-cmvp-certificates-and-security-policies
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, fips-140, fips-140-3, cmvp-certificate, security-policy, cavp, compliance-evidence]
level: practitioner
status: draft
description: "Read a CMVP certificate and its Security Policy: status, sunset date, tested environments, CAVP algorithm certs and approved-mode rules, to prove FIPS claims."
sources: ["https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search", "https://csrc.nist.gov/projects/cryptographic-module-validation-program/modules-in-process/modules-in-process-list", "https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading CMVP certificates and Security Policies

Auditors ask "which certificate?" Answer from the CMVP database, not from a vendor web page.

## Find the certificate
- Search: csrc.nist.gov, CMVP "Validated Modules Search" by vendor, module name or cert number.
- Status values: **Active** (usable for new systems), **Historical** (past sunset or revoked
  for new procurement; existing systems need a risk acceptance), **Revoked**.
- FIPS 140-3 certificates sunset five years after validation; some carry a shorter **interim**
  validation. FIPS 140-2 validations moved to the Historical list on 21 September 2026, so any
  remaining 140-2 dependency now needs a migration plan.
- **Modules In Process (MIP)** and **Implementation Under Test (IUT)** lists show modules in
  the queue. Being listed there is not validation; some agencies accept MIP for procurement,
  check the specific policy.

## Read the certificate page
- Standard (FIPS 140-3), overall level, embodiment (software/hardware/hybrid), validation date,
  sunset date.
- **Tested configuration(s)**: OS, processor, with or without PAA (processor algorithm
  acceleration, e.g. AES-NI). Your deployment should match one of these.
- **Approved algorithms** with CAVP certificate numbers (e.g. `A1234`). A CAVP algorithm cert
  alone means "this implementation passed the test vectors", not a validated module.
- Caveats, e.g. "when operated in approved mode", "entropy: no assurance of the minimum strength
  of generated SSPs" (meaning you must supply entropy as described).

## Read the Security Policy PDF (the binding document)
1. **Module boundary** and the exact version/hash of the files.
2. **Approved services table**: algorithm, mode, key sizes, standard. Anything you call must be
   in it.
3. **Non-approved services**: allowed to exist, but using them makes that output non-FIPS.
4. **Approved mode / indicator**: how the module signals approved service use.
5. **Initialisation and installation rules**: config file, `fipsinstall` steps, CPU feature
   requirements, things you must not do (e.g. don't load other providers in the same context).
6. **SSP (keys/CSPs) table**: how keys are generated, entered, stored, zeroised.
7. **Entropy**: whether the module includes an entropy source (ESV certificate number) or
   expects an external one.

## Evidence pack for an assessor
Record per deployment: module name + version, certificate number + status + sunset date, the
tested OE you match, the config proving approved mode, and the list of services you use mapped
to rows of the approved services table.

## Gotchas
- Version drift: the validated version is often older than the distro's current package; a
  security update can move you to an unvalidated build until the vendor re-validates.
- A vendor's "FIPS-compliant" or "FIPS-ready" means not validated.
- One product may contain several modules (kernel crypto API, OpenSSL, NSS, libgcrypt), each
  with its own certificate.

## Verify
- [ ] Every certificate you cite is Active today and its sunset date is tracked.
- [ ] Installed module version matches the Security Policy exactly.
- [ ] Every algorithm/key size you use appears in the approved services table.
