---
id: computing-software.systems-network-administration.active-directory.redirect-default-user-and-computer-containers
name: redirect-default-user-and-computer-containers
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ou-delegation, redircmp, redirusr, domain-join]
level: practitioner
status: docs-checked
description: "Redirect the default CN=Computers and CN=Users containers to real OUs with redircmp and redirusr so new objects get GPOs and delegation."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/redirect-users-computers-containers
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-addomain
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Redirecting the default Users and Computers containers

`CN=Computers` and `CN=Users` are containers, not OUs: group policy can be applied to OUs but not to them. Objects
created by earlier-version APIs land there unmanaged.

## Redirect
Log on with domain administrator credentials in the domain being changed. The domain must be at the Windows Server
2003 domain functional level or higher (all DCs on Windows Server 2003 or newer, `ADPREP /FORESTPREP` and `/DOMAINPREP`
run). Create the target OUs first, then:
```cmd
redircmp "OU=New Computers,OU=Staging,DC=corp,DC=example,DC=com"
redirusr "OU=New Users,OU=Staging,DC=corp,DC=example,DC=com"
```
This changes the `wellKnownObjects` attribute on the domain NC head, which earlier-version APIs use. Microsoft lists as
affected: the Domain Join UI, `NET COMPUTER`, `NET GROUP`, `NET USER` and `NETDOM ADD` when `/ou` is not specified or
supported. Some applications need specific security principals in `CN=Users` or `CN=Computers`; check dependencies
before moving objects out.

## Prepare the target OUs
- Link a baseline GPO (security baseline, LAPS, firewall) so new machines are protected from minute one.
- Delegate to helpdesk or provisioning accounts: move objects out of staging and set attributes.
- Protect from accidental deletion (OUs, unlike the default containers, can be deleted accidentally).

## Check current values
```powershell
(Get-ADDomain).ComputersContainer
(Get-ADDomain).UsersContainer
```

## Gotchas
- Tools that hardcode `CN=Users` or pass no path may still land objects in the default containers; fix them to
  pass a path.
- Redirecting users removes the system protection from `CN=Users` (its systemFlags changes from -1946157056 to 0, by
  design), so the container can then be moved, deleted or renamed. Microsoft recommends keeping the container and the
  default accounts in place.
- Redirecting computers into an OU with heavy hardening can break joins that need software installed first; a light
  staging OU is safer.

## Verify
- [ ] A computer joined with the Domain Join UI and no OU lands in the staging OU.
- [ ] Objects left in `CN=Computers` = 0 (report weekly).

## Checked
2026-10-27. Documentation: Microsoft Learn "Redirect users and computers containers" (updated 2026) and the
`Get-ADDomain` reference. Confirmed: functional-level and ADPREP prerequisites; redirection changes `wellKnownObjects` and
applies to earlier-version APIs (Domain Join UI, NET COMPUTER/GROUP/USER, NETDOM ADD without /ou); GPOs cannot be applied to CN
containers; CN=Users loses system protection after redirusr; application-dependency warning; `ComputersContainer` and
`UsersContainer` properties of `Get-ADDomain`. Removed as unconfirmed: the claim that built-in groups and krbtgt stay in
CN=Users and the do-not-move-krbtgt rule, and the statement that `Add-Computer` without `-OUPath` uses the redirected
container (the verify step now uses the documented Domain Join UI).
Method: documentation only; no commands were run.
