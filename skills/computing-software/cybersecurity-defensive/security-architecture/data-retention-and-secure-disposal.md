---
id: computing-software.cybersecurity-defensive.security-architecture.data-retention-and-secure-disposal
name: data-retention-and-secure-disposal
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-protection, data-disposal, data-retention, media-sanitization, nist-800-88, crypto-erase, certificate-of-destruction, records-retention, legal-hold]
level: practitioner
status: docs-checked
description: "Enforce data retention schedules and sanitise media correctly (clear, purge, destroy per NIST 800-88), including cloud crypto-shredding and disposal records."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r1.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data retention and secure disposal

**Goal:** data is kept as long as required and no longer, and when media or data is retired
it cannot be recovered.

## Retention
- Retention schedule per record type: legal/regulatory minimum, business need, and a maximum; take
  the legal periods from your counsel and regulators, not from this skill.
- Implement in systems: mailbox and SharePoint retention policies, database purge jobs,
  object storage lifecycle rules, backup expiry. Policies on paper do nothing.
- **Legal hold** overrides deletion: a mechanism to suspend deletion for specific custodians/data when litigation is anticipated.

## Sanitisation (NIST SP 800-88)
| Method | What | When |
|---|---|---|
| Clear | Logical overwrite of user-addressable storage (on magnetic media a single pass with a fixed pattern typically hinders recovery) | Reuse inside the organisation, low sensitivity |
| Purge | Overwrite, block erase or cryptographic erase via dedicated sanitize commands; degaussing of magnetic media | Leaving organisational control, sensitive data |
| Destroy | Shred, disintegrate, pulverise, incinerate | Highest sensitivity, failed or unverifiable media (Clear/Purge cannot be applied) |

- **SSDs/flash**: overwriting through the normal read/write interface is unreliable (spare cells, wear
  levelling). Use the dedicated device sanitize commands (800-88 prefers the ATA Sanitize Device feature set
  over Secure Erase), cryptographic erase, or destroy.
- **Encrypted media**: cryptographic erase (sanitise the keys, not the data) is fast, but only if the data
  was encrypted from the start; verify it per 800-88 section 4.7.
- **Phones and office equipment**: a factory reset is only Clear-level; follow the 800-88 Appendix A entry
  for the device type to reach Purge. Copiers, printers and multifunction machines hold storage too.
- **Cloud**: you cannot sanitise provider media; rely on encryption with your own keys and sanitise the
  keys (cryptographic erase), plus provider attestations.

## Records
Keep a disposal record: asset ID, serial, method, tool, operator, date, verification, and a
certificate of destruction from any third-party vendor (with chain of custody to the vendor).

## Gotchas
- Backups and replicas keep "deleted" data until they expire.
- Drives that fail cannot be cleared or purged: treat them as Destroy candidates before they leave.

## Verify
- [ ] Verify each sanitised item where practical, plus representative sampling, per 800-88 section 4.7.
- [ ] Retention jobs report deleted volumes; legal hold tested.

## Checked
2026-11-01. Confirmed in NIST SP 800-88 Rev. 1: Clear/Purge/Destroy definitions and methods, single-pass
note for magnetic media, flash wear levelling limits, cryptographic erase, ATA Sanitize preference,
office equipment scope, verification and sampling, sanitization record fields (manufacturer, serial,
method). Removed: nvme command, CompTIA and CIS control citations, privacy-law claim, RMA clause advice.
Method: documentation only; no commands were run.
