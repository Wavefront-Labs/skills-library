---
id: computing-software.it-support-helpdesk.device-provisioning.joiner-account-creation-and-licensing
name: joiner-account-creation-and-licensing
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, account-provisioning, joiners, onboarding, entra-id, group-based-licensing, temporary-access-pass]
level: practitioner
status: draft
description: "Create joiner accounts correctly: required attributes, usage location before licences, group-based licensing and access, hybrid sync timing, and TAP for first sign-in."
sources:
  - "https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users"
  - "https://learn.microsoft.com/en-us/entra/identity/users/licensing-groups-assign"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# joiner-account-creation-and-licensing

## Before the start date
- Confirm the request is authorised (HR record or manager request with approval) and
  gather: legal/preferred name, job title, department, manager, location, start date,
  employment type, end date for contractors.
- Check for a returning employee or duplicate before creating anything.

## Create
- Cloud-only: Entra admin center > Users > New user, or Graph PowerShell:
```powershell
New-MgUser -DisplayName "Jo Smith" -UserPrincipalName jo.smith@contoso.com -MailNickname jo.smith `
  -AccountEnabled:$false -Department "Finance" -JobTitle "Analyst" -UsageLocation GB `
  -PasswordProfile @{ ForceChangePasswordNextSignIn = $true; Password = '<generated>' }
```
- Hybrid: create in AD in the correct OU (sync scope) with the same attributes, then wait
  for or trigger a delta sync (`Start-ADSyncSyncCycle -PolicyType Delta` on the Connect
  server).
- Set `manager` and `employeeId`; dynamic groups and approvals rely on them.

## Licences and access
- **UsageLocation** must be set before any licence can be assigned.
- Prefer group-based licensing and role-based groups (dynamic by department/job title, or
  assigned role groups). Avoid copying "the same as Bob" access.
- Mailbox appears a few minutes after an Exchange Online licence applies.

## First sign-in
Issue a Temporary Access Pass valid for the first day so the user registers MFA/passkey
and Windows Hello securely, instead of reading out a password. Enable the account on the
start date (or schedule it).

## Gotchas
- UPN changes later are painful; get naming right first time (naming convention).
- Licence assignment errors (no licences left, conflicting plans) show on the group's
  Licences page.
- Accounts enabled weeks early are a target; keep them disabled until day one.

## Verify
The user signs in on day one with TAP, registers MFA, has mailbox and Teams, and is in the
expected role groups with no licensing errors.
