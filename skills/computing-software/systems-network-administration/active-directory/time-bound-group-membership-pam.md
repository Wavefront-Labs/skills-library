---
id: computing-software.systems-network-administration.active-directory.time-bound-group-membership-pam
name: time-bound-group-membership-pam
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, privileged-access, privileged-access-management-feature, ttl-group-membership, just-in-time, jit-admin, add-adgroupmember-membertimetolive, enable-adoptionalfeature, kerberos-ticket-lifetime]
level: advanced
status: gated
description: "Use the AD Privileged Access Management optional feature for expiring group membership (-MemberTimeToLive) as just-in-time admin, and its caveats."
sources:
  - https://learn.microsoft.com/en-us/microsoft-identity-manager/pam/privileged-identity-management-for-active-directory-domain-services
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/add-adgroupmember
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/enable-adoptionalfeature
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time-bound group membership (AD PAM feature)

**Goal:** admins are members of privileged groups only for a limited window; membership
disappears automatically, and Kerberos tickets expire with it.

## Enable
The feature needs forest functional level 2016 and cannot be undone once enabled (gated: unconfirmed, source is paywalled or blocked).
```powershell
Get-ADOptionalFeature 'Privileged Access Management Feature'    # feature name (gated: unconfirmed, source is paywalled or blocked)
Enable-ADOptionalFeature 'Privileged Access Management Feature' -Scope ForestOrConfigurationSet -Target ad.example.com
```

## Grant expiring membership
```powershell
Add-ADGroupMember -Identity 'GG-Tier1-ServerAdmins' -Members 'adm1-jsmith' -MemberTimeToLive (New-TimeSpan -Hours 4)
Get-ADGroup 'GG-Tier1-ServerAdmins' -Property member -ShowMemberTimeToLive | Select -Expand member
```
- With Windows Server 2016 or later, the membership carries a time limit in Active Directory. An expired link is evaluated in real time by the Security Accounts Manager on any DC, while an added member must replicate before it takes effect.
- Time-limited group memberships produce time-limited TGTs, so access does not outlive the membership.

## Operating it
- Wrap it in a request workflow: a small script or portal that records the ticket number, approver and duration, then calls `Add-ADGroupMember -MemberTimeToLive`.
- Pair with Protected Users and authentication policy silos so elevated accounts are still constrained.
- Microsoft states that MIM PAM, which builds on this capability with a bastion forest, is not recommended for new deployments in Internet-connected environments, and that it is distinct from Microsoft Entra Privileged Identity Management.

## Caveats
- Permanent memberships are still possible, so audit for members of privileged groups that have no TTL regularly.
- Replication latency affects how quickly a new membership works.

## Verify
- [ ] After the TTL, the user is no longer in the group and tickets obtained during the window expire.
- [ ] Audit report lists no permanent members in Tier 0 groups except break-glass.

## Checked
Checked 2026-10-27 against Microsoft Learn (Privileged Access Management for Active Directory Domain Services, MIM documentation; Add-ADGroupMember, Get-ADGroup, Enable-ADOptionalFeature and Get-ADOptionalFeature references, Windows Server 2025).
- Confirmed: Add-ADGroupMember -MemberTimeToLive takes a TimeSpan; Get-ADGroup -ShowMemberTimeToLive; Enable-ADOptionalFeature -Scope ForestOrConfigurationSet -Target; Windows Server 2016 or later stores a time limit on the membership; expired links are evaluated in real time by the SAM; time-limited memberships produce time-limited TGTs; the MIM PAM recommendation note.
- Gated: the optional feature name, and the forest functional level 2016 and irreversibility statements. Reason: the cmdlet pages do not state them.
- Removed: the TTL output example, nested-group and application-caching claims, and the PIM for Groups remarks.

Method: documentation only; no commands were run.
