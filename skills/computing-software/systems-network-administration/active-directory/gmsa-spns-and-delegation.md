---
id: computing-software.systems-network-administration.active-directory.gmsa-spns-and-delegation
name: gmsa-spns-and-delegation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, gmsa, gmsa-spn, setspn, resource-based-constrained-delegation, rbcd-services]
level: advanced
status: docs-checked
description: "Register SPNs on gMSAs, let services self-register, avoid duplicates and configure constrained or resource-based delegation for gMSA-run front ends."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/configure-kerberos-delegation-group-managed-service-accounts
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adserviceaccount
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SPNs and delegation for gMSAs

A service running as a gMSA needs its SPNs on the **gMSA**, not on the computer account, or Kerberos falls back to
NTLM (or fails where NTLM is blocked).

## Register
Either set the SPNs at creation (`New-ADServiceAccount ... -ServicePrincipalNames`) or afterwards:
```powershell
Set-ADServiceAccount gmsa-web -ServicePrincipalNames @{Add='HTTP/app.corp.example.com','HTTP/app'}
Get-ADServiceAccount gmsa-web -Properties ServicePrincipalNames
```
Microsoft's gMSA overview requires the SPNs to be correctly registered for each service that uses a gMSA, and DNS records
to be set up correctly for Kerberos.

## Moving an SPN from a user account to a gMSA
An SPN must be registered on one account only: remove it from the old account first, then add it to the gMSA.

## Delegation (front-end gMSA calling a back end as the user)
- **Resource-based constrained delegation** (configured on the back end): `Set-ADComputer`, `Set-ADServiceAccount`
  and others have a `-PrincipalsAllowedToDelegateToAccount` parameter. For a computer back end:
```powershell
Set-ADComputer FILE01 -PrincipalsAllowedToDelegateToAccount gmsa-web$
```
  If the back end is itself a gMSA: `Set-ADServiceAccount gmsa-api -PrincipalsAllowedToDelegateToAccount gmsa-web$`.
- **Kerberos constrained delegation on the front-end gMSA** (Microsoft's gMSA delegation page): the
  `userAccountControl` flags define the delegation type and `msDS-AllowedToDelegateTo` holds the back-end SPNs.
```powershell
# constrained, Kerberos only
Set-ADAccountControl -Identity gmsa-web$ -TrustedForDelegation $false -TrustedToAuthForDelegation $false
# constrained with protocol transition (any authentication protocol)
Set-ADAccountControl -Identity gmsa-web$ -TrustedForDelegation $false -TrustedToAuthForDelegation $true
# then set the back-end SPNs in msDS-AllowedToDelegateTo on the gMSA
# turn delegation off
Set-ADAccountControl -Identity gmsa-web$ -TrustedForDelegation $false -TrustedToAuthForDelegation $false
Set-ADServiceAccount -Identity gmsa-web$ -Clear 'msDS-AllowedToDelegateTo'
```
- Avoid unconstrained delegation (`-TrustedForDelegation $true`): it is the setting Microsoft lists as "trust this
  computer for delegation to any service".

## Verify
- [ ] `Get-ADServiceAccount gmsa-web -Properties ServicePrincipalNames` shows the intended SPNs and no other account
  holds them.

## Checked

Documentation: Microsoft Learn "Configuring Kerberos delegation for group Managed Service Accounts", the gMSA overview, and
the Set-ADServiceAccount, Set-ADComputer and Set-ADAccountControl references, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: SPN registration requirement, `-PrincipalsAllowedToDelegateToAccount` on Set-ADComputer and
Set-ADServiceAccount, the Set-ADAccountControl and `msDS-AllowedToDelegateTo` delegation commands. Removed unconfirmed
`setspn` switches, the dsacls self-registration grant, the KRB_AP_ERR_MODIFIED/event 11 claim, IIS
`useAppPoolCredentials` advice and the `klist`/4624 verification (the docs repo has no coverage for them).

Method: documentation only; no commands were run.
