---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-krbtgt-reset-and-credential-rotation
name: ransomware-krbtgt-reset-and-credential-rotation
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [krbtgt-reset, credential-rotation, ransomware-recovery, active-directory-restore, forest-recovery, golden-ticket]
level: sme
status: draft
description: "Rotate credentials after ransomware: double krbtgt reset, privileged and service accounts, machine and trust passwords, cloud tokens, and timing relative to restore."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# krbtgt reset and credential rotation after ransomware

Assume every credential that touched compromised systems is known to the attacker.
Restoring servers without rotating credentials invites immediate re-entry (golden tickets,
stolen service account passwords).

## Order of operations
1. Contain (isolate networks, block attacker C2, disable known compromised accounts).
2. Recover/verify a clean AD (restore DCs from a clean point in an isolated environment, or
   validate surviving DCs).
3. **Rotate credentials in the clean environment before reconnecting** other systems.
4. Restore/rebuild workloads, then reconnect in stages with monitoring.

## krbtgt (invalidates forged Kerberos tickets)
Reset **twice**, because the account keeps the current and previous password:
```powershell
# Microsoft's New-KrbtgtKeys.ps1 script automates and checks replication; manual equivalent:
Set-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString (New-Guid).Guid -AsPlainText -Force)
repadmin /syncall /AdeP          # ensure replication to all DCs
# wait > max ticket lifetime (default 10 h) for normal ops, or reset again immediately in a forest
# recovery where breaking existing tickets is acceptable
Set-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString (New-Guid).Guid -AsPlainText -Force)
```
RODCs have their own `krbtgt_NNNNN` accounts: reset them too. Resetting twice quickly forces
all users/services to re-authenticate (expect disruption; in incident recovery that's intended).

## Other credentials
- All **privileged accounts** (Domain/Enterprise Admins, Tier 0 admins), break-glass accounts.
- **Service accounts** (prefer converting to gMSA); update services/apps after reset.
- **Built-in Administrator** on DCs (DSRM password: `ntdsutil "set dsrm password"`).
- **Local admin** on servers/workstations (LAPS rotation: `Reset-LapsPassword` / expire).
- **Computer account** passwords of DCs and critical servers (`Reset-ComputerMachinePassword`),
  **trust** passwords (`netdom trust /resetOneSide`).
- Azure/Entra: Entra Connect sync account (`MSOL_`/AD DS connector), Entra admin accounts,
  revoke sessions/refresh tokens (`Revoke-MgUserSignInSession`), app secrets/certificates of
  sensitive app registrations.
- Infrastructure: vCenter/ESXi root and SSO admin, backup system accounts, network devices,
  hypervisor OOB (iDRAC/iLO), firewall admins, cloud root/IAM keys, secrets vault master keys.
- Third-party remote access tools and VPN shared secrets.

## Track it
Credential rotation register: account, owner, rotated (date/time), validated. Unrotated
privileged accounts block the "reconnect" milestone.

## Verify
Replication healthy after resets (`repadmin /replsummary`), old tickets fail (`klist purge`
then access works only with new TGT), register 100% complete for Tier 0 before reconnection.
