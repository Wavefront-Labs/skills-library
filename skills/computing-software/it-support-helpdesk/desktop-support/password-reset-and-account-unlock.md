---
id: computing-software.it-support-helpdesk.desktop-support.password-reset-and-account-unlock
name: password-reset-and-account-unlock
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, identity-support, password-reset, account-unlock, identity-verification, set-adaccountpassword, unlock-adaccount, entra-id, password-writeback, temporary-access-pass]
level: practitioner
status: draft
description: "Reset passwords and unlock accounts safely: verify identity first, AD vs Entra ID vs hybrid writeback, force change at next logon, and cached-credential issues on laptops."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adaccountpassword"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-writeback"
  - "https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# password-reset-and-account-unlock

Goal: the right person gets back in quickly; an attacker impersonating them
does not. Password resets are the #1 social-engineering path into
organisations (the 2023 casino breaches started at a help desk).

## 1. Verify identity before anything
Use the organisation's verification standard, in order of strength:
- Callback to the number in the HR/directory record (not the number the
  caller gives).
- Manager confirmation via a separate channel (Teams/phone from directory).
- In-person with photo ID at a desk.
- Push/number-match to an already-registered MFA method
  (some ITSM tools integrate this).
Not acceptable alone: name + employee ID + date of birth (findable on
LinkedIn/breaches). Executives and IT admins get stricter checks. Record how
you verified in the ticket.

## 2. Find where the account lives
- On-premises AD (or hybrid synced from AD): reset in AD; it syncs to Entra
  within ~2 min with password hash sync.
- Cloud-only Entra account: reset in Entra admin centre / M365 admin centre.
- Hybrid with SSPR **password writeback**: users can self-reset from the
  cloud — point them at aka.ms/sspr next time.

## 3. Reset / unlock
```powershell
Unlock-ADAccount -Identity jdoe
Set-ADAccountPassword -Identity jdoe -Reset -NewPassword (Read-Host -AsSecureString "Temp pwd")
Set-ADUser -Identity jdoe -ChangePasswordAtLogon $true
Get-ADUser jdoe -Properties LockedOut, BadLogonCount, PasswordLastSet, PasswordExpired
```
Entra: user → Reset password (generates temp) — or issue a **Temporary
Access Pass** if the user also lost MFA (see the MFA reset skill).
Deliver the temporary password by the verified channel, never in the ticket
or email to the same mailbox they can't access.

## Laptop gotchas
- Remote user off VPN: the laptop still knows the old password (cached
  credentials). Have them sign in with the old one, connect VPN, then lock
  (Ctrl+Alt+Del → Lock) and unlock with the new one to update the cache —
  or use a pre-logon VPN.
- Entra-joined devices: new password works after the device can reach Entra;
  Windows Hello PIN keeps working.
- Phones and other devices still holding the old password will re-lock the
  account — see lockout-source analysis.

## Verify
User signs in with their own new password (not the temporary one), the
ticket records verification method, and `LockedOut` is False with
`BadLogonCount` 0 after an hour.
