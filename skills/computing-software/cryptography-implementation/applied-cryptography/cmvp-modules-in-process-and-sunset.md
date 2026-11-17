---
id: computing-software.cryptography-implementation.applied-cryptography.cmvp-modules-in-process-and-sunset
name: cmvp-modules-in-process-and-sunset
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, cmvp-modules-in-process, fips-140-3, fips-140-2-sunset, cmvp, procurement]
level: practitioner
status: docs-checked
description: "Read the CMVP Modules In Process and Historical lists: what MIP status means for procurement, the FIPS 140-2 move to Historical in September 2026, and revoked certificates."
sources: ["https://csrc.nist.gov/projects/cryptographic-module-validation-program/modules-in-process/modules-in-process-list", "https://csrc.nist.gov/projects/fips-140-3-transition-effort", "https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMVP Modules In Process and sunset dates

## Lists
- **Validated modules**: the searchable database of issued FIPS 140-1, 140-2 and 140-3 certificates, with a
  certificate detail page per module. A certificate can be marked Historical or Revoked.
- **Modules In Process (MIP)**: modules the CMVP is actively working on. Each row shows a status and the date it
  entered that state (for example Pending Review, Review, Comment Resolution - Lab, Comment Resolution - CMVP,
  Pending Resubmission). The action to respond can sit with the CMVP, the lab or the vendor. Hold is also a state.
- **Implementation Under Test (IUT)** is a separate list on the same program site.

## What MIP means
- A module on MIP is not validated. NIST's validated-modules page says only modules tested and validated to FIPS 140-2
  or 140-3 meet the requirements for protecting sensitive information. Treat MIP as "not yet", not as equivalence.
- Contact the vendor for a specific module's schedule; NIST's MIP page directs you there.

## Sunset and Historical
- Per the FIPS 140-3 transition page, FIPS 140-2 modules stay active for 5 years after validation or until
  September 21, 2026 (its schedule table says September 22, 2026), when all FIPS 140-2 certificates move to the
  Historical list.
- Historical: Federal agencies should not include these modules in new systems but can procure them for legacy
  systems. Reasons are certificates more than 5 years old or programmatic transitions. Agencies may make a risk
  determination about continuing to use them.
- Revoked: the validation is no longer valid and may not be cited to demonstrate compliance.

## Procurement checklist
1. Get the certificate number from the vendor and look it up yourself on the validated modules search.
2. NIST advises asking the vendor for a signed letter naming the validated module and certificate number, and
   comparing it with the CMVP entry; if they disagree, the vendor is not offering a validated solution.
3. Check the entry's validated version and operational environment match what you deploy.
4. Confirm the algorithms you use are covered and you use the module in its approved mode.

## Verify
- [ ] Certificate link, status and Historical/sunset information recorded in the system security plan.

## Checked
2026-11-01. Confirmed against the CMVP Modules In Process List page, the FIPS 140-3 Transition Effort page and the
Validated Modules page: MIP purpose and status wording, Historical and Revoked meaning, 5-year rule, the September
2026 FIPS 140-2 move (21 September in the prose, 22 September in the table), the vendor letter advice. Removed:
the MIP state names Review Pending/In Review/Coordination/Finalization, the 12-24 month queue figure, the
IUT definition, the "Active" status and the FIPS 140-3 5-year sunset claim, none of which the pages state.
Method: documentation only; no commands were run.
