---
id: computing-software.cybersecurity-defensive.system-hardening.uefi-secure-boot
name: uefi-secure-boot
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [firmware-security, uefi-secure-boot, secure-boot, shim, mok, dbx-updates, bootkit-protection]
level: advanced
status: docs-checked
description: "Enable and manage UEFI Secure Boot across a fleet: verify state, understand the key hierarchy, and apply DB/DBX revocation and certificate updates safely."
sources: ["https://support.microsoft.com/en-us/topic/how-to-manage-the-windows-boot-manager-revocations-for-secure-boot-changes-associated-with-cve-2023-24932-41a975df-beb2-40c1-99a3-b3ff139f832d"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UEFI Secure Boot

**Goal:** every host boots only signed bootloaders, kernels and drivers, with revocation lists current.

## Check state
Use your platform's Secure Boot state report and your management console's device health data. Secure Boot requires UEFI mode (not legacy/CSM).

## Key hierarchy
PK (platform owner) -> KEK -> db (allowed signers) and dbx (revoked hashes/certs).

## Revocations and updates
- DBX updates revoke vulnerable boot managers (for example the BlackLotus CVE-2023-24932 mitigations). Confirm boot media are updated first - applying revocations can make old recovery media unbootable. See the blacklotus-mitigation skill.
- Microsoft's guidance covers adding the 2023 Secure Boot certificates to the DB and KEK and updating boot managers signed with them. Track device readiness through Windows Update and OEM firmware updates.

## Firmware settings
Supervisor/admin password on firmware setup, disable boot from external media unless needed, disable CSM.

## Verify
- [ ] Fleet report shows Secure Boot enabled on 100% of supported devices (exceptions listed).
- [ ] DB/DBX state matches the vendor's guidance (for the Windows mitigation, the KB's check returns True and event 1037 is logged).

## Checked
2026-10-28. Confirmed against official pages: DB and DBX roles, 2023 certificate additions to DB and KEK, boot-media breakage after revocation, BlackLotus CVE-2023-24932 (Microsoft KB5025885).
Removed or rewritten: Confirm-SecureBootUEFI, msinfo32, mokutil, bootctl, mbr2gpt, the Linux shim/MOK/module-signing section, kernel lockdown, BootHole CVE, fwupdmgr, the June 2026 expiry date and non-URL sources.
Method: documentation only; no commands were run.
