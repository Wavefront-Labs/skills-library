---
id: computing-software.digital-forensics-incident-response.evidence-handling.secure-evidence-storage-and-access-control
name: secure-evidence-storage-and-access-control
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-storage, chain-of-custody, evidence-locker, access-control, encryption-at-rest, dfir]
level: practitioner
status: draft
description: "Store physical and digital evidence securely: evidence lockers, access logs, encrypted evidence repositories, backups of images, and environmental controls."
sources: ["https://www.iso.org/standard/44381.html", "https://www.swgde.org/documents/published-complete-listing/", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure evidence storage and access control

**Goal:** evidence cannot be altered, lost or accessed by unauthorised people while it is
held, and you can prove it.

## Physical evidence
- Locked evidence room or safe with restricted keys/badges; access log (who, when, why),
  ideally camera-covered.
- Shelving by case, items in sealed bags; temporary lockers for after-hours intake.
- Environmental: cool, dry, away from magnetic fields; fire suppression suitable for
  electronics.

## Digital evidence repository
- Dedicated storage (NAS/SAN or encrypted drives) on an isolated network; not on general
  file shares or cloud sync folders.
- Encryption at rest (BitLocker/LUKS, or encrypted E01 containers); keys held by the
  evidence custodian.
- Per-case folders with ACLs; analysts work on **copies**; master images read-only.
- Access logging (file audit, SIEM) on the repository.
- **Two copies** of master images on separate media/sites, hashes verified periodically.
- Retain a hash manifest per case (`sha256sum -c manifest.sha256` monthly or before use).

## Malware and dangerous content
Store samples in password-protected archives (convention `infected`), clearly labelled, in a
separate repository; never on analyst desktops.

## Gotchas
- Drives degrade: verify hashes of long-held images and migrate media every few years.
- Personal data in evidence is subject to privacy law; restrict and record access accordingly.

## Verify
Annual audit: sample items from the evidence log, physically locate them, check seals, and
re-hash digital masters against acquisition hashes.
