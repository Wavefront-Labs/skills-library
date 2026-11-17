---
id: computing-software.digital-forensics-incident-response.evidence-handling.evidence-retention-and-disposal
name: evidence-retention-and-disposal
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-retention, evidence-disposal, legal-hold, media-sanitization, nist-sp-800-88, dfir]
level: practitioner
status: draft
description: "Set evidence retention periods and dispose of evidence properly: legal holds, statute periods, returning devices, and media sanitization per NIST SP 800-88."
sources: ["https://csrc.nist.gov/pubs/sp/800/88/r1/final", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Evidence retention and disposal

**Goal:** keep evidence as long as it may be needed, and no longer; dispose of it so it
cannot be recovered, with a record.

## Retention
- Driven by: active litigation or **legal hold** (overrides everything), regulatory
  requirements, statute of limitations for potential claims, contractual obligations,
  insurer requirements. Typical corporate IR default: 3-7 years after case closure,
  decided by legal and documented in the evidence policy.
- Personal data in evidence: GDPR storage limitation means you need a justified period.
- Review cases annually; legal confirms release before disposal.

## Disposal
- **Return** original devices to owners when allowed (custody form row: returned to, date,
  signature), after confirming forensic images are verified.
- **Digital evidence**: delete images and working copies from all locations (repository,
  analyst workstations, backups per backup policy).
- **Media sanitization** per NIST SP 800-88: Clear (overwrite) for reuse in-house, Purge
  (cryptographic erase, ATA Secure Erase, NVMe Sanitize, degaussing for HDD) for leaving
  control, Destroy (shred, disintegrate) for highest sensitivity. SSDs: overwrite is not
  reliable; use crypto erase/sanitize or destroy.
- Certificate of sanitization/destruction (SP 800-88 Appendix G sample) with item, method,
  date, operator, verifier.

## Gotchas
- Forgotten copies: exports in case platforms, email attachments, analyst laptops, cloud
  buckets used for transfer.
- Disposing while a related case or hold exists elsewhere in the company; check with legal.

## Verify
For each disposed item: legal release reference, sanitization certificate, evidence log
status updated to "destroyed/returned", and repository search confirms no copies remain.
