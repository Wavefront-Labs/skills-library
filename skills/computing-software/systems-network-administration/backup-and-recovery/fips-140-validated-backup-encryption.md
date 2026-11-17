---
id: computing-software.systems-network-administration.backup-and-recovery.fips-140-validated-backup-encryption
name: fips-140-validated-backup-encryption
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [fips-140, fips-140-3, cmvp, validated-cryptography, backup-encryption, compliance]
level: advanced
status: docs-checked
description: "Meet FIPS 140 needs for backup encryption: CMVP validation vs compliance claims, the 140-2 sunset, Windows FIPS policy and Veeam strict FIPS mode."
sources:
  - https://csrc.nist.gov/projects/cryptographic-module-validation-program
  - https://helpcenter.veeam.com/docs/backup/vsphere/fips_compliance.html
  - https://learn.microsoft.com/en-us/windows/security/security-foundations/certification/fips-140-validation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIPS 140 validated encryption for backups

## Validated vs compliant
- NIST says that for US federal agencies, if cryptography is required it must be validated: non-validated cryptography is viewed as providing no protection, in effect plaintext. FIPS 140-2 or 140-3 applies when the agency specifies that data be cryptographically protected.
- Validation means the module has a CMVP certificate, issued after an independent NVLAP-accredited lab (CSTL) tests it. Ask vendors for the certificate number and confirm your build uses that module; a marketing claim such as "uses AES-256" is not validation.
- If a module is revoked, its use is no longer permitted.

## FIPS 140-2 vs 140-3 (CMVP schedule)
- CMVP began validating to FIPS 140-3 on 22 September 2020. It stopped accepting 140-2 submissions for new certificates on 22 September 2021, with only limited exceptions from 1 April 2022.
- 140-2 active modules could be used for new systems until 21 September 2026; after that date their certificates move to the Historical List. As of this review that date has passed, so target 140-3 modules for new work.
- A 140-3 validation stays on the Active list for 5 years (2 years for Interim Validations).

## Enabling FIPS mode
- **Windows**: the Windows cryptographic modules have FIPS 140 validation, and to use them in an approved mode you must follow the rules in each module's Security Policy. Administrators can enable the legacy FIPS policy with Group Policy ("System cryptography: Use FIPS-compliant algorithms for encryption, hashing, and signing" under Security Options) or MDM (`AllowFipsAlgorithmPolicy` set to 1).
- **Veeam Backup & Replication**: Options > Security tab > FIPS compliance section > "Force strict FIPS compliance mode". In this mode NTLM is disabled (Kerberos only), persistent agent components must be used for guest processing, connections to non-FIPS-compliant components cannot be established, the Veeam Cryptographic Module is used, and self-tests run. After toggling it, edit each Linux server with a persistent Data Mover and finish the wizard, or those servers become unavailable.

## Evidence for auditors
List each crypto point (in transit, at rest on the repository, tape, cloud), the module, its certificate number, and configuration evidence showing FIPS mode enabled.

## Verify
Evidence collected for every crypto point; a restore in the FIPS-enabled environment succeeds.

## Checked

2026-11-09. Confirmed against the NIST CMVP page (validation requirement, CSTLs, 140-3 and 140-2 dates, Active list periods, revocation), the Veeam FIPS Compliance page (strict mode steps and effects, Linux Data Mover note) and the Microsoft "FIPS 140 validation" page (Security Policy requirement, Group Policy and MDM settings). Partial reads of the NIST and Microsoft pages; the Veeam page was read in full. Removed: registry path, RHEL `fips-mode-setup`, tape drive and appliance certificate claims, AWS FIPS endpoint, FedRAMP/CMMC statements, and the claims about restores into non-FIPS environments and vendor updates changing module versions (not on cited pages).

Method: documentation only; no commands were run.
