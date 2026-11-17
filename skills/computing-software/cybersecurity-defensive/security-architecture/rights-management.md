---
id: computing-software.cybersecurity-defensive.security-architecture.rights-management
name: rights-management
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [rights-management, microsoft-purview-information-protection, azure-rms, sensitivity-labels, irm, persistent-encryption, usage-rights]
level: practitioner
status: draft
description: "Apply rights management encryption with Purview sensitivity labels: usage rights, co-authoring, external sharing, super user recovery, and the scanning/search trade-offs."
sources: ["https://learn.microsoft.com/en-us/purview/encryption-sensitivity-labels", "https://learn.microsoft.com/en-us/azure/information-protection/configure-super-users", "https://learn.microsoft.com/en-us/purview/sensitivity-labels-coauthoring"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rights management encryption

Rights management (Azure RMS, behind Purview sensitivity labels) encrypts the file itself and binds
usage rights (view, edit, print, copy, forward) to identities, so protection travels with the file.

## Label design
- Encryption on only the top labels (e.g. Confidential\Restricted, Highly Confidential). Encrypting everything breaks search, eDiscovery tools, DLP and third-party integrations.
- Assign permissions now (fixed groups, e.g. "All employees - Co-Author") for most labels; let users assign permissions (Do Not Forward / Encrypt-Only) for ad hoc email.
- Set content expiration and offline access days (default allows offline access indefinitely; set e.g. 7 days for the highest label).
- Enable co-authoring for encrypted files (tenant setting) before rolling out to Office web users.

## Operations
- **Super user** feature for recovery and eDiscovery: `Enable-AipServiceSuperUserFeature`, `Add-AipServiceSuperUser -EmailAddress svc-ediscovery@...`; keep disabled except during use, audit.
- External sharing: recipients need an Entra account or one-time passcode; B2B guest settings and cross-tenant access settings must allow it.
- Unified labeling scanner / DLP read encrypted content only if they have super user or label rights.

## Gotchas
- Removing a user from the group revokes future opens, not copies already decrypted and saved elsewhere.
- Usage restrictions do not stop screenshots or a phone camera.
- Third-party apps (PDF readers, mobile mail apps) may not support RMS; test the actual client mix.
- Double Key Encryption breaks most cloud services by design; use only for a tiny set of data.

## Verify
- [ ] Labelled file opened by an outside account is denied.
- [ ] Print/copy restrictions enforced in desktop Office.
- [ ] Super user recovery tested and then disabled.
