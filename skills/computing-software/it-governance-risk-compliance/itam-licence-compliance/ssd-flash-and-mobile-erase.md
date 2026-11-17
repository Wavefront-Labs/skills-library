---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.ssd-flash-and-mobile-erase
name: ssd-flash-and-mobile-erase
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [ssd-flash-and-mobile-erase, media-sanitisation-nist-800-88, crypto erase, nvme sanitize, ata secure erase, ssd erasure, mobile wipe, blkdiscard, itam-licence-compliance]
level: advanced
status: draft
description: "Erase SSDs, NVMe and phones using cryptographic erase, ATA/NVMe sanitise commands and factory reset plus verification."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSD, flash and mobile device erasure

Goal: reliable erasure on flash media where overwrite fails.

Method:
- Preferred: cryptographic erase of a self-encrypting drive or of a BitLocker/FileVault/LUKS key combined with removing key protectors, then drive-level sanitise.
- NVMe: nvme sanitize with block erase or crypto erase option, or format with secure erase setting (nvme-cli; confirm options per drive).
- SATA: ATA Sanitize or Enhanced Secure Erase via hdparm or vendor tool.
- Phones/tablets: remove from MDM and accounts (Activation Lock, FRP), use erase-all-content, confirm encryption was on beforehand so erase destroys keys.
- Keep an erase log with date, operator, tool and result.

Gotchas:
- Some USB bridges block sanitise commands.
- Unremoved Apple ID or Google account blocks resale.

Verify: read-back sampling shows no recoverable data.
