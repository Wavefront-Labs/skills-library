---
id: computing-software.systems-network-administration.backup-and-recovery.backup-media-sanitization-and-destruction
name: backup-media-sanitization-and-destruction
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [media-sanitization, nist-800-88, tape-destruction, degaussing, crypto-erase, disposal]
level: practitioner
status: docs-checked
description: "Sanitise retired backup media per NIST SP 800-88 Rev. 1: clear, purge and destroy for tape, HDD and SSD, crypto erase caveats, certificates."
sources:
  - https://csrc.nist.gov/pubs/sp/800/88/r1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup media sanitisation and destruction

**Goal:** retired tapes and disks leave the organisation with no recoverable data, with evidence to prove it.

## NIST SP 800-88 Rev. 1 levels
- **Clear**: logical techniques on all user-addressable locations, protecting against simple non-invasive recovery.
- **Purge**: physical or logical techniques that make recovery infeasible with state-of-the-art laboratory techniques.
- **Destroy**: recovery infeasible with laboratory techniques and the media can no longer store data.
Pick the level by categorising the information, assessing the medium and the risk to confidentiality, and the future plans for the media; also weigh cost and environmental impact.

## Appendix A minimums by media
| Media | Clear | Purge | Destroy |
|---|---|---|---|
| Magnetic tape (reel and cassette) | re-record all data once with a non-sensitive pattern; the guide notes this is impractical for most uses since it occupies the transport for long | degauss with an approved degausser rated for the media | incinerate in a licensed incinerator, or shred |
| ATA HDD | at least one overwrite pass with a fixed value such as zeros | ATA Sanitize Device (overwrite EXT, or Cryptographic Erase if supported), or SECURITY ERASE UNIT in Enhanced Erase mode, or crypto erase via TCG Opal/Enterprise | shred, disintegrate, pulverise or incinerate |
| ATA SSD | overwrite pass, or SECURITY ERASE UNIT; overwrite may miss unmapped flash and wears the media | ATA Sanitize block erase or Cryptographic Erase, or TCG crypto erase | shred, disintegrate, pulverise or incinerate |
| NVMe SSD | overwrite pass | NVM Express Format (User Data Erase or Cryptographic Erase), or TCG crypto erase | shred, disintegrate, pulverise or incinerate |
The guide prefers the ATA Sanitize commands over SECURITY ERASE UNIT when supported, and says ATA Secure Erase is only Clear for flash. It says degaussing must not be solely relied on for flash or hybrid devices, and that degaussing renders many devices unusable (then it is also a destruction technique). Verification is required for each Clear and Purge technique.

## Crypto erase (section 2.6)
Cryptographic Erase sanitises the encryption key, leaving only ciphertext. Do not use it if encryption was enabled after sensitive data was already stored unsanitised, or if that is unknown. Consider it when all data is encrypted before storage, you know where every copy of the key (and any wrapping key) lives and can sanitise them all, and the keys are protected. If keys exist outside the device through backup or escrow, they could be used to recover the data later. For backup tapes this means key destruction must cover the key manager and key backups (applying the guide's key-copy rule to backup software is practice).

## Process (practice, informed by section 4.8)
1. Inventory media due for disposal and check no legal hold applies.
2. Keep secure storage and chain of custody until sanitisation.
3. Sanitise or destroy in house or via a vendor; verify per technique.
4. Complete a certificate of media disposition per item where confidentiality warrants. The guide's list: manufacturer, model, serial number, organisation media number, media type and source, sanitisation description (Clear, Purge, Destroy), method and tool (with version), verification method, destination, and for sanitisation and verification the person's name, title, date, location, contact and signature. For very low confidentiality in bulk the guide allows skipping it.
5. Update the media inventory and backup catalogue.

## Gotchas
- Failed drives returned under warranty leave with your data unless sanitised first (destruction is the guide's option when Clear or Purge cannot be applied or verification fails).
- Encrypted backups still need key destruction recorded for crypto erase to count.

## Verify
Every disposed barcode or serial in the inventory has a matching certificate entry, where certificates are required by your policy.

## Checked

2026-11-09. Checked against NIST SP 800-88 Rev. 1 (full PDF, 65 pages, read sections 2.5-2.6, 4.8, Table 5-1 and the Appendix A tape, ATA HDD, ATA SSD and NVMe rows). A Rev. 2 PDF exists but was not read; check which revision your organisation follows. Removed: the NSA and LTO sources (not read), LTO servo-track and "WORM tapes can only be destroyed" claims, "long erase takes hours", NAID AAA, "annual audit sample" and the "keep your drive" product advice. The process steps are practice except where tied to section 4.8.

Method: documentation only; no commands were run.
