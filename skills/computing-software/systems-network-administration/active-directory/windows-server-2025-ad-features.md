---
id: computing-software.systems-network-administration.active-directory.windows-server-2025-ad-features
name: windows-server-2025-ad-features
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, functional-level, functional-level-2025, 32k-pages, database-32k-pages-feature, windows-server-2025, ldap-encryption, kerberos, dc-upgrade, optional-feature]
level: advanced
status: docs-checked
description: "Adopt Windows Server 2025 AD: the 2025 functional level, the irreversible 32k database page optional feature, and behaviour changes to test first."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/32k-pages-optional-feature
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/enable-32k-pages-optional-feature
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/ldap-signing
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windows Server 2025 AD: level 10 and 32k pages

## Functional level
Windows Server 2025 adds a new domain and forest functional level, mapping to `DomainLevel 10` and `ForestLevel 10` in
unattended installs; only Windows Server 2025 DCs can run at it. It is required for the 32k database page feature.
Windows Server 2019 and 2022 stay on the 2016 level (no plan to retrofit). New forests on 2025 must be at Windows Server
2016 level or later, and promoting a replica needs the existing domain at 2016 or later.

## The 32k database page optional feature
NTDS.dit has used 8k ESE pages since Windows 2000. The 32k page format allows approximately 3,200 values in a
multivalued attribute (2.6 times more).
- New 2025 installs get a 32k-page capable database but run in 8k-page simulation mode for compatibility. DCs that were
  in-place upgraded keep the 8k format. A DC also has a 32k-capable database if promoted over the wire or restored from
  a 32k-format backup.
- Enabling the feature is forest-wide and **cannot be reverted**. It needs every DC on Windows Server 2025 with a
  32k-capable database, domain and forest functional levels at 2025, replication free of errors, backups of the GC and
  FSMO DCs, and an Enterprise Admins (or equivalent) account. Test your backup software with 32k backups first.
- Check capability per DC: the `msDS-JetDBPageSize` attribute on the DC's NTDS Settings object is `32768`
  (32k-capable), `8192`, or absent (Windows Server 2022 or earlier).
```powershell
Get-ADObject -LDAPFilter "(ObjectClass=nTDSDSA)" -SearchBase "CN=Configuration,DC=fabrikam,DC=com" -Properties msDS-JetDBPageSize
$params = @{
    Identity = 'Database 32k pages feature'
    Scope    = 'ForestOrConfigurationSet'
    Server   = 'FABRIKAMDC01'
    Target   = 'fabrikam.com'
}
Enable-ADOptionalFeature @params
```
- After enabling, only 32k-format backup media can restore a 2025 DC; 8k backups made earlier are unusable unless you
  do a complete authoritative forest recovery. Larger pages can raise memory use. Monitor replication traffic after the
  change.

## Behaviour changes to test before introducing 2025 DCs
- LDAP: signing (sealing) is required by default for new AD deployments, and an upgrade with no server signing
  policy set also requires signing. Watch events 2887 and 2889 to find unsigned clients. LDAP over TLS supports TLS 1.3.
  Confidential attributes can only be added, searched or modified over encrypted LDAP connections. Channel binding
  audit events 3074 and 3075 can be enabled.
- Kerberos: the KDC no longer issues TGTs with RC4 encryption; the legacy `SupportedEncryptionTypes` registry value is
  no longer honoured (use Group Policy). Legacy devices that only do RC4 cannot authenticate with Kerberos to a
  2025 DC.
- Passwords: default machine-account passwords are blocked on 2025 DCs when the policy "Domain controller: Refuse
  setting default machine account password" is enabled, and legacy SAM RPC password-change methods are blocked by
  default when called remotely.
- NTLM and SMB: the SMB client can block NTLM (see the restrict-ntlm skill), SMB signing is required by default for
  outbound connections, and Remote Mailslot is disabled by default, including for DC Locator.
- Other: AD uses CPUs in all processor groups, and `fixupObjectState` lets Enterprise Admins repair objects missing
  `SamAccountType` or `ObjectCategory`.

## Verify
- [ ] Lab forest upgrade completed with your LOB apps before production.
- [ ] `Get-ADOptionalFeature` shows the 32k feature either intentionally enabled with fresh 32k backups, or
  deliberately left off.

## Checked

Date: 2026-10-27. Documentation: What's new in Windows Server 2025, AD DS functional levels (updated 2025-10-30),
Database 32k pages and Enable Database 32k pages articles (2024-10), LDAP signing for AD DS
(MicrosoftDocs/windowsserverdocs, main branch).
Confirmed: level numbers 10 and the 2016 floor, 32k page behaviour, requirements, irreversibility, backup effects,
`msDS-JetDBPageSize` values, the `Enable-ADOptionalFeature` identity and parameters, LDAP signing defaults and events
2887/2889, TLS 1.3, RC4 TGT change, SAM RPC and default-password changes, SMB and mailslot changes.
Removed unconfirmed claims: the `Windows2025Domain`/`Windows2025Forest` names, the DES/PKINIT "enforcement timelines",
the NTLM event IDs 8001-8004.

Method: documentation only; no commands were run.
