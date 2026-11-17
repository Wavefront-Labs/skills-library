---
id: computing-software.it-support-helpdesk.device-provisioning.certificates-of-destruction-and-itad-vendors
name: certificates-of-destruction-and-itad-vendors
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, data-sanitization, disposal, certificate-of-destruction, itad, r2v3, e-stewards, naid-aaa, chain-of-custody, asset-retirement, disposal-chain-of-custody, physical-destruction]
level: practitioner
status: draft
description: "Retire devices through an ITAD vendor safely: certifications to require (NAID AAA, R2v3, e-Stewards), chain of custody, serial-level certificates of destruction, and audits."
sources:
  - "https://csrc.nist.gov/pubs/sp/800/88/r1/final"
  - "https://sustainableelectronics.org/r2-standard/"
  - "https://e-stewards.org/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# certificates-of-destruction-and-itad-vendors

Goal: every retired device is provably sanitised or destroyed, and the
paperwork would satisfy an auditor or a regulator after a breach claim.

## Choose the vendor
- **Data destruction**: i-SIGMA **NAID AAA** certification (audited,
  unannounced inspections; on-site vs plant-based).
- **Environmental/reuse**: **R2v3** (SERI) or **e-Stewards** (no export of
  hazardous e-waste to developing countries).
- Contract terms: NIST 800-88 methods per media type, serial-level reporting,
  timeframes, liability/insurance, right to audit, sub-processor disclosure,
  data protection agreement (GDPR Article 28 where applicable), remarketing
  revenue share if devices are resold.

## Chain of custody
1. Internal: device marked "retired" in asset register; drives removed or
   wiped per policy; stored in a locked cage.
2. Collection manifest listing asset tag + device serial + drive serials,
   signed by your staff and the vendor's driver; sealed containers with
   seal numbers recorded; GPS-tracked vehicles for high-sensitivity loads.
3. Vendor receiving report reconciles counts — investigate any mismatch
   immediately.
4. Processing: sanitisation (for resale) or shredding (for destroy).
5. **Certificate of Destruction / Sanitisation** — serial-level, method,
   date, standard, signature. Bulk "we destroyed 300 laptops" certificates
   are not enough.

## Close the loop
- Attach certificates to the asset records; mark assets disposed with date.
- Spot-audit: witness a shred session or request video; sample resold
  devices in vendor reports.
- Retain records per your retention policy (often 6–7 years).

## Gotchas
- Leased devices: lessor's process and contract decide — sanitise before
  return anyway.
- Phones and tablets: remove from MDM/ABM, clear Activation Lock/FRP, or
  vendor can't resell (and you get them back).
- Printers/MFPs and network gear have storage too (job retention disks,
  configs with credentials).

## Verify
For any disposed asset tag you can produce: retirement date, collection
manifest, receiving reconciliation and a serial-level certificate.
