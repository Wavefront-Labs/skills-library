---
id: computing-software.systems-network-administration.active-directory.ad-security-hardening
name: ad-security-hardening
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-security, hardening, privileged-groups, domain-admins, protected-users, adminsdholder, admincount, windows-laps, laps, gmsa, kerberoasting, asrep-roasting, aes, rc4, krbtgt, krbtgt-reset, golden-ticket, unconstrained-delegation, constrained-delegation, rbcd, ntlm-restriction, ntlmv1, ldap-signing, ldap-channel-binding, print-spooler, machineaccountquota, ad-cs, esc1, pingcastle, bloodhound, purple-knight, tier-0]
level: advanced
status: docs-checked
description: "Harden Active Directory: shrink privileged groups, Protected Users, Windows LAPS, gMSA, delegation, LDAP signing, krbtgt rotation and audit events."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/reducing-the-active-directory-attack-surface
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/how-to-configure-protected-accounts
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/protected-users-security-group
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-reset-the-krbtgt-password
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-signing-in-windows-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD security hardening — close the paths attackers actually walk

**Goal:** remove the well-known ways from "one compromised workstation" to "Domain
Admin", in an order that gives the most risk reduction per change. Administrative
tiering itself is outlined in
`computing-software.systems-network-administration.active-directory.ou-group-and-gpo-design`;
this skill is the control list around it. Defensive use only.

## 0. Measure first
Run an AD security assessment from a domain-joined admin host, using a tool you are authorised to run. Fix the
highest-risk findings, re-scan, repeat. Without a baseline you'll harden the wrong things.

## 1. Shrink and protect Tier 0
- Domain/Enterprise/Schema Admins, Administrators, Account/Server/Backup/Print
  Operators, DnsAdmins, Group Policy Creator Owners: **empty or near-empty**. Schema and
  Enterprise Admins empty except during change windows.
- Admin accounts are separate from daily accounts, never have mailboxes, and log on
  only to DCs/PAWs (enforce with *Deny log on* user rights on lower tiers).
- Add admin accounts to **Protected Users**: no NTLM, no DES/RC4, no delegation, no
  cached credentials, 4-hour TGT. Test first — it breaks NTLM-only apps — and **never**
  add service or computer accounts. The group needs the Windows Server 2012 R2 domain functional level.
- Mark admins *Account is sensitive and cannot be delegated*.
- Accounts once in privileged groups keep `adminCount=1` and broken inheritance
  (AdminSDHolder); clean them up after removal, and watch for unexpected ACEs on
  `CN=AdminSDHolder` — a persistence technique.

## 2. Local admin passwords: Windows LAPS
Use built-in **Windows LAPS** (shipped with the April 11, 2023 updates; the legacy Microsoft LAPS download is a
separate product): `Update-LapsADSchema` (one-time, forest-wide), `Set-LapsADComputerSelfPermission -Identity <OU>`,
`Set-LapsADReadPasswordPermission` for the readers, then set the `BackupDirectory` policy (2 = Active Directory,
1 = Entra ID; the default 0 is disabled). Enable password encryption (retrieving previously decrypted passwords is not
supported below the Windows Server 2016 domain functional level) and restrict who can read. A shared local admin
password across machines enables lateral movement.

## 3. Service accounts and Kerberoasting
Any user account with an SPN is a target for offline guessing of its service-ticket password.
- Replace with **gMSA** (`New-ADServiceAccount ... -PrincipalsAllowedToRetrieveManagedPassword <GROUP>`): AD
  manages and rotates the password.
- For remaining SPN accounts: long random passwords, `msDS-SupportedEncryptionTypes`
  AES-only, not in privileged groups.
- Find them: `Get-ADUser -Filter 'ServicePrincipalName -like "*"' -Properties ServicePrincipalName`.
- No accounts with *Do not require Kerberos preauthentication* (AS-REP roasting):
  `Get-ADUser -Filter 'DoesNotRequirePreAuth -eq $true'`.
- Plan RC4 removal: audit 4769 events (they record the ticket encryption type) first; Microsoft is
  phasing RC4 out of defaults, so check current guidance for your DC OS.

## 4. Delegation
**Unconstrained delegation** on anything but DCs = a host that harvests TGTs:
`Get-ADComputer -Filter 'TrustedForDelegation -eq $true'`. Move to constrained or
resource-based constrained delegation. Set `ms-DS-MachineAccountQuota` (default 10) to **0** so
ordinary users can't create computer accounts.

## 5. Protocol hardening on DCs
- **LDAP signing required** and **LDAP channel binding** (check event 2889 for
  unsigned binds before enforcing).
- **SMB signing**: keep it required on DCs and avoid signing-policy mismatches between DCs (a mismatch can break
  replication).
- **NTLM**: audit NTLM use first, then restrict it (see the restrict-ntlm skill). Removing NTLM entirely is a project.

## 6. krbtgt rotation
Reset the krbtgt password **twice**, waiting at least the maximum user and service ticket lifetime (10 hours by
default) between resets, and confirm replication in between. The krbtgt password history holds two passwords, so the
second reset clears the old one. Do this on a regular schedule and after any suspected Tier 0 compromise. The
procedure covers writable DCs, not RODCs (each RODC has its own `krbtgt_<number>` account).

## 7. Detect
Forward DC Security logs to a SIEM: 4728/4732/4756 (member added to a global, local or universal group), 4769
(Kerberos service ticket requested; check the encryption type), 4662 (operation performed on a directory object) and
5136 (directory object modified, for example AdminSDHolder or GPOs).

## Verify
- [ ] Assessment findings re-scanned and top findings closed.
- [ ] Privileged groups contain only named, documented admin accounts in Protected Users.
- [ ] Windows LAPS rotates passwords on all workstations and member servers.
- [ ] No Kerberoastable privileged accounts; gMSAs used where possible; no pre-auth-disabled users.
- [ ] No unconstrained delegation off DCs; MachineAccountQuota = 0; Spooler off on DCs.
- [ ] krbtgt reset on a documented schedule.

## Checked
2026-10-27, against Microsoft Learn (windowsserverdocs security best practices and Appendix pages, Protected Users, Windows LAPS pages, forest-recovery krbtgt reset, SupportArticles-docs, event 4769 page). Confirmed: Protected Users protections, 240-minute TGT limit, DFL 2012 R2 and the rule not to add service or computer accounts; AdminSDHolder, SDProp (hourly on the PDC emulator) and the adminCount behaviour; Windows LAPS April 11, 2023 release, Update-LapsADSchema, Set-LapsADComputerSelfPermission, Set-LapsADReadPasswordPermission, BackupDirectory values, encryption and the 2016 DFL note; krbtgt reset twice with a 10-hour default wait and password history of 2; LDAP signing and event 2889; Appendix L event names for 4728, 4732, 4756, 4769, 4662, 5136; ms-DS-MachineAccountQuota default 10. Removed as unconfirmed: third-party scanner names and their descriptions, the 120-character gMSA figure, 0x17, Print Spooler, PetitPotam/EPA and AD CS ESC1 bullets, the NTLM level setting, the Microsoft reset script remark, the "#1 lateral-movement" ranking and the OS-default uncertainty note.

Method: documentation only; no commands were run.
