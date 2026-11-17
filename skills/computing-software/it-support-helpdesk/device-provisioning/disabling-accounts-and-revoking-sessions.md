---
id: computing-software.it-support-helpdesk.device-provisioning.disabling-accounts-and-revoking-sessions
name: disabling-accounts-and-revoking-sessions
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, account-disable, offboarding, leavers, revoke-sessions, entra-id, active-directory, authentication-methods-removal]
level: practitioner
status: draft
description: "Cut a leaver's access completely and on time: disable in AD/Entra, revoke sessions and tokens, remove MFA and devices, and close the gaps SSO does not cover."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.users.actions/revoke-mgusersigninsession"
  - "https://learn.microsoft.com/en-us/powershell/module/activedirectory/disable-adaccount"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# disabling-accounts-and-revoking-sessions

## Timing
Agree the exact time with HR. Routine leavers: end of last working day. Hostile or
sensitive exits: disable while the person is in the meeting being told.

## Core steps
1. **Disable**:
   - Hybrid: `Disable-ADAccount -Identity jsmith` (AD is the source), then a delta sync so
     Entra follows (`Start-ADSyncSyncCycle -PolicyType Delta`). Reset the password too.
   - Cloud-only: `Update-MgUser -UserId jsmith@contoso.com -AccountEnabled:$false`.
2. **Revoke sessions**: `Revoke-MgUserSignInSession -UserId jsmith@contoso.com` (or Entra
   portal > user > Revoke sessions). Refresh tokens die at once; existing access tokens can
   live up to about an hour unless the app supports continuous access evaluation.
3. **Remove authentication methods** (Authenticator, phone, FIDO2) and disable or delete
   their registered devices so personal devices lose app access.
4. **Mobile and mail**: retire/wipe corporate apps on personal devices (MAM selective
   wipe); remove ActiveSync partnerships if used.
5. **Privileged access**: remove admin roles, PIM eligibility, break-glass knowledge, and
   rotate any shared secrets they knew.

## What SSO does not cover
- SaaS apps with local accounts, vendor portals, social media, domain registrar, cloud
  consoles with separate logins.
- API keys, personal access tokens, service accounts they owned, SSH keys on servers.
- VPN certificates, Wi-Fi certificates, door badges, building alarm codes.
Keep an app inventory with owners so the leaver checklist lists these.

## Then
Mailbox and OneDrive handling (see leaver-mailbox-and-onedrive-retention), device return
(see recovering-and-wiping-returned-devices), licence removal after retention is set.

## Gotchas
- Disabling only in Entra for a synced user gets overwritten at the next sync.
- Group membership removal can trigger data loss in some apps; disable first, clean
  groups later per retention policy.

## Verify
Sign-in logs show only failed attempts after the disable time, no active sessions remain,
and the leaver checklist is signed off with each app owner's confirmation.
