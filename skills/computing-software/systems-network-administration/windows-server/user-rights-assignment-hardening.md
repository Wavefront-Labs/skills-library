---
id: computing-software.systems-network-administration.windows-server.user-rights-assignment-hardening
name: user-rights-assignment-hardening
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-policy-settings, gpo-security-settings, user-rights-assignment, seinteractivelogonright, seremoteinteractivelogonright, sedenynetworklogonright, seservicelogonright, sedebugprivilege, group-policy, tiering]
level: practitioner
status: docs-checked
description: "Set user rights assignments by GPO: who may log on locally, via RDP, as a service or batch job, the deny rights for tiering, and privileges to keep tight."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/user-rights-assignment
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-f--securing-domain-admins-groups-in-active-directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User rights assignment hardening

GPO path: *Computer Configuration > Policies > Windows Settings > Security Settings > Local
Policies > User Rights Assignment*. Inventory the current holders of a right before defining
it in a GPO, and include every principal that needs it.

## Logon rights
| Setting | Constant |
|---|---|
| Allow log on locally | `SeInteractiveLogonRight` |
| Allow log on through Remote Desktop Services | `SeRemoteInteractiveLogonRight` |
| Access this computer from the network | `SeNetworkLogonRight` |
| Log on as a service | `SeServiceLogonRight` |
| Log on as a batch job | `SeBatchLogonRight` |
| Deny log on locally | `SeDenyInteractiveLogonRight` |
| Deny log on through Remote Desktop Services | `SeDenyRemoteInteractiveLogonRight` |
| Deny access to this computer from the network | `SeDenyNetworkLogonRight` |
| Deny log on as a batch job | `SeDenyBatchLogonRight` |
| Deny log on as a service | `SeDenyServiceLogonRight` |

Tiering: Microsoft's guidance for securing Domain Admins groups defines these five deny
settings (network, batch, service, locally, Remote Desktop Services) for the admin groups
on computers that are not domain controllers, so credentials of Tier 0 accounts are not
exposed on lower tiers.

## Privileges to keep tight
These are held only by the accounts that need them: `SeDebugPrivilege` (Debug programs),
`SeTcbPrivilege` (Act as part of the operating system), `SeBackupPrivilege` and
`SeRestorePrivilege` (Back up / Restore files and directories),
`SeTakeOwnershipPrivilege`, `SeLoadDriverPrivilege` (Load and unload device drivers),
`SeImpersonatePrivilege` (Impersonate a client after authentication) and
`SeAssignPrimaryTokenPrivilege` (Replace a process level token). Look up each setting's
default and recommended members on the Learn user rights assignment page before changing it.

## Check what applies
```cmd
whoami /priv          (current token)
gpresult /scope computer /h <report>.html
```

## Gotchas
- A GPO that defines *Log on as a service* with only your list can drop accounts that
  applications added locally, so services may fail to start after a reboot: inventory first.
- Do not deny network logon to broad groups such as Authenticated Users on DCs or file servers.

## Verify
- [ ] A Tier 0 admin is denied logon to a Tier 1 server; the server admin group works.
- [ ] Services still start after a reboot with the GPO applied.

## Checked
2026-10-28. Confirmed against "User rights assignment" (all ten logon-right and the privilege constants) and "Appendix F: Securing Domain Admins groups" (the five deny settings for non-DC computers). Removed as unconfirmed: "replaces the local list" wording, the Local account SIDs S-1-5-113 and S-1-5-114, the per-right member recommendations, `secedit /export` and `IIS APPPOOL` details.
Method: documentation only; no commands were run.
