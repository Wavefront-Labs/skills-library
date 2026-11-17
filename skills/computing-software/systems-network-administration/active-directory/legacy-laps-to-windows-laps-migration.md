---
id: computing-software.systems-network-administration.active-directory.legacy-laps-to-windows-laps-migration
name: legacy-laps-to-windows-laps-migration
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, windows-laps, laps, legacy-laps-migration, get-lapsadpassword, ms-mcs-admpwd, legacy-microsoft-laps, admpwd-ps, laps-emulation-mode]
level: practitioner
status: docs-checked
description: "Move from legacy Microsoft LAPS (AdmPwd) to Windows LAPS: side-by-side rules, emulation mode, cut over by OU, retire the CSE, and read passwords with Get-LapsADPassword."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-scenarios-migration
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-scenarios-legacy
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-technical-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy Microsoft LAPS to Windows LAPS

## Know the states
- **Legacy LAPS**: MSI-installed client-side extension (CSE), attributes `ms-Mcs-AdmPwd` and `ms-Mcs-AdmPwdExpirationTime`.
- **Windows LAPS**: in-box, `msLAPS-*` attributes, `LAPS` module, encryption, history, DSRM, Entra backup.
- **Legacy emulation mode**: Windows LAPS can honour legacy LAPS Group Policy settings. Requirements: the legacy CSE is not installed, no Windows LAPS policy is present on the machine (a Windows LAPS policy always wins), and the machine is not a domain controller. Passwords are stored in clear text in the legacy attributes, and Windows LAPS features such as encryption or Entra backup are unavailable. Windows LAPS does not add the legacy schema or ACLs.

## Rule: never manage the same account with both
A Windows LAPS policy and a legacy LAPS policy that target the same local account are not supported. A side-by-side setup works only when the two policies target different local accounts.

## Migration steps
1. Prepare AD for Windows LAPS (schema, self-permission, read permissions) per the schema skill.
2. Pilot OU: create the Windows LAPS policy (AD backup, encryption). Choose:
   - **Same account** (easiest): disable or remove the legacy LAPS policy, apply the Windows LAPS policy, then remove the legacy LAPS software.
   - **Different account**: create the new local account before applying the Windows LAPS policy, keep legacy LAPS on the old account during the transition, then remove the legacy policy and software and the old account if unneeded.
3. Confirm passwords appear in new attributes:
```powershell
Get-LapsADPassword -Identity WS0123 -AsPlainText
```
4. Roll out by OU and update helpdesk tooling to `Get-LapsADPassword`.
5. When done: remove the legacy LAPS policy and uninstall the legacy LAPS software from each device (Add/Remove Programs or the command in the migration article).

## Verify
- [ ] The legacy LAPS software is uninstalled from every migrated device.
- [ ] LAPS Operational log shows successful updates on all migrated machines.

## Checked
Checked 2026-10-27 against Microsoft Learn (Migrate to Windows LAPS from legacy LAPS; legacy emulation mode article; Windows LAPS technical reference; Get-LapsADPassword reference), Windows Server documentation current in 2026.
- Confirmed: side-by-side requires different accounts; same-account migration steps (disable legacy policy, apply Windows LAPS policy, remove legacy software); emulation-mode requirements and limits; legacy-to-Windows attribute mapping; Get-LapsADPassword and the msLAPS-PasswordExpirationTime check.
- Removed: AdmPwd.dll and AdmPwd.PS names, the claim that Windows LAPS refuses and logs an event on collision, the ADUC LAPS tab, legacy cmdlet names, clearing legacy attributes and the Get-Package check.

Method: documentation only; no commands were run.
