---
id: computing-software.systems-network-administration.active-directory.authentication-policy-silos-for-tier-0
name: authentication-policy-silos-for-tier-0
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, authentication-policy-silo, authentication-policies, new-adauthenticationpolicysilo, new-adauthenticationpolicy, tier-0-silo, tgt-lifetime, claims, kerberos-armoring, privileged-access, authentication-policy-audit-mode]
level: advanced
status: gated
description: "Pin Tier 0 admin sign-in to Tier 0 hosts with authentication policies and silos: KDC claims/armoring prereqs, audit mode, the access condition, and enforcement."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/authentication-policies-and-authentication-policy-silos
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-adauthenticationpolicy
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/protected-users-security-group
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Authentication policy silos for Tier 0

**Goal:** a Domain Admin's credentials only work when signing in **on** DCs and Tier 0
PAWs. Stolen credentials used elsewhere fail at the KDC.

## Prerequisites
- Authentication policy silos were introduced in Windows Server 2012 R2; confirm the domain functional level and DC requirements in the Microsoft article.
- Kerberos armoring for the Tier 0 hosts and KDC support for claims and armoring (Group Policy: *KDC support for claims, compound authentication and Kerberos armoring* on the DCs and *Kerberos client support for claims, compound authentication and Kerberos armoring* on clients) (gated: unconfirmed, source is paywalled or blocked).
- Admin accounts in **Protected Users** (members cannot authenticate with NTLM, Digest or CredSSP default credential delegation, and cannot be delegated).

## Build (audit first)
```powershell
New-ADAuthenticationPolicy -Name 'AP-Tier0' -UserTGTLifetimeMins 240 -Enforce:$false `
  -UserAllowedToAuthenticateFrom '<SDDL_CONDITION>' `
  -ProtectedFromAccidentalDeletion $true
New-ADAuthenticationPolicySilo -Name 'Silo-Tier0' -UserAuthenticationPolicy 'AP-Tier0' `
  -ComputerAuthenticationPolicy 'AP-Tier0' -ServiceAuthenticationPolicy 'AP-Tier0' -Enforce:$false
# members: admin accounts and the Tier 0 computers (DCs, PAWs)
$members = (Get-ADGroupMember GG-Tier0-Admins) + (Get-ADComputer -Filter * -SearchBase 'OU=Domain Controllers,DC=ad,DC=example,DC=com') + (Get-ADComputer PAW01)
foreach ($m in $members) {
  Grant-ADAuthenticationPolicySiloAccess -Identity 'Silo-Tier0' -Account $m
  Set-ADAccountAuthenticationPolicySilo -Identity $m -AuthenticationPolicySilo 'Silo-Tier0'
}
```
`<SDDL_CONDITION>` is the access control condition on the device identity (for example devices that are members of the silo); build it in the Active Directory Administrative Center Authentication node (gated: unconfirmed, source is paywalled or blocked), or see the cmdlet reference example for -UserAllowedToAuthenticateFrom.

## Watch audit events, then enforce
DC logs: `Applications and Services Logs > Microsoft > Windows > Authentication > AuthenticationPolicyFailures-DomainController`
(enable the log). While a policy is not enforced it is in audit mode: event 305 reports a potential Kerberos restriction failure, and event 105 reports an enforced denial. When clean:
```powershell
Set-ADAuthenticationPolicy 'AP-Tier0' -Enforce $true
Set-ADAuthenticationPolicySilo 'Silo-Tier0' -Enforce $true
```

## Gotchas
- Lockout risk: test with one admin account first; keep a break-glass account outside the
  silo, stored offline.
- The 240-minute non-renewable TGT lifetime in the example forces re-authentication; scripts running as admins break (use gMSAs).
- Computers must be silo members too if the condition tests silo membership (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Admin sign-in to a member server is denied and event 105 is logged on the DC once the policy is enforced.
- [ ] Admin sign-in to DCs and PAWs works.

## Checked
Checked 2026-10-27 against Microsoft Learn (Authentication policies and authentication policy silos; New-ADAuthenticationPolicy, New-ADAuthenticationPolicySilo, Grant-ADAuthenticationPolicySiloAccess, Set-ADAccountAuthenticationPolicySilo and Set-ADAuthenticationPolicy references, Windows Server 2025; Protected Users group).
- Confirmed: cmdlet names and parameters (-UserTGTLifetimeMins, -Enforce, -UserAllowedToAuthenticateFrom, -ProtectedFromAccidentalDeletion, silo policy parameters, -Account, -AuthenticationPolicySilo); non-enforced policies run in audit mode; the AuthenticationPolicyFailures-DomainController log with events 105 and 305; Protected Users effects; silos introduced in Windows Server 2012 R2; policy TGTs are non-renewable.
- Gated: the KDC and client armoring Group Policy names, the SDDL condition and ADAC wizard text, and the computer silo-membership rule.
- Removed: events 4820 and 4821 and the pinned SDDL string, which no readable page confirms.

Method: documentation only; no commands were run.
