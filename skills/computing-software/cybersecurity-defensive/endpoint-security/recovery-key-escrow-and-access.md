---
id: computing-software.cybersecurity-defensive.endpoint-security.recovery-key-escrow-and-access
name: recovery-key-escrow-and-access
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [full-disk-encryption, recovery-key-escrow, bitlocker-recovery, filevault-recovery-key, key-retrieval-audit, helpdesk-verification, key-rotation]
level: practitioner
status: draft
description: "Govern disk encryption recovery keys: escrow coverage, who may retrieve keys, identity verification, audit of retrievals, and rotation after use."
sources: ["Microsoft Learn - BitLocker recovery (Entra ID and AD DS key storage, key rotation)", "Apple Platform Deployment - FileVault recovery key escrow", "NIST SP 800-111 Guide to Storage Encryption Technologies for End User Devices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recovery key escrow and access

**Goal:** every encrypted device has a recoverable key, only authorised people can retrieve
keys after verifying the requester, and every retrieval is logged and followed by rotation.

## Escrow coverage
- Windows: BitLocker recovery passwords in Entra ID (device object) or AD DS (`msFVE-RecoveryInformation`); MBAM is retired.
- macOS: FileVault PRK in MDM.
- Linux: LUKS recovery passphrases or header backups in a secrets vault (indexed by hostname/serial).
- Reconcile: encrypted devices vs devices with an escrowed key; fix gaps by re-escrowing (`BackupToAAD-BitLockerKeyProtector`, new FileVault PRK).

## Access control
- Entra: role "Cloud Device Administrator" or custom role with `microsoft.directory/bitlockerKeys/key/read`; owners can self-service via the My Account portal.
- AD: delegate read on recovery objects to a helpdesk group only.
- Limit to helpdesk tier and security; not all IT admins.

## Retrieval procedure (helpdesk)
1. Verify identity (callback to registered number, manager confirmation, or verified ticket from the user's authenticated session) - attackers call helpdesks to get keys for stolen laptops.
2. Confirm the device belongs to the caller (serial, key ID shown on the recovery screen).
3. Provide the key; record ticket, key ID, verifier.
4. **Rotate** the key after use (Intune rotation, `manage-bde -protectors`, new FileVault PRK).

## Audit
Entra audit logs "Read BitLocker key" activity; AD object access auditing on recovery objects;
MDM logs for FileVault key views. Alert on bulk reads or reads by unexpected admins.

## Gotchas
- Keys of retired devices stay in directories; keep them per retention rules (needed for old drives) but restrict access.
- Users self-retrieving keys after phishing compromise of their account: require MFA and alert on self-service retrievals for stolen-device reports.

## Verify
- [ ] Escrow coverage at 100% of encrypted devices.
- [ ] Quarterly review of key retrieval logs against helpdesk tickets.
