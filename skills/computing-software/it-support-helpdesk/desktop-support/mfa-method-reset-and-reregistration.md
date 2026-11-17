---
id: computing-software.it-support-helpdesk.desktop-support.mfa-method-reset-and-reregistration
name: mfa-method-reset-and-reregistration
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, identity-support, mfa-reset, microsoft-authenticator, temporary-access-pass, require-re-register-mfa, authentication-methods, entra-id, lost-phone, passkey, passkeys]
level: practitioner
status: docs-checked
description: "Handle lost or replaced MFA devices in Entra ID: issue a Temporary Access Pass, require MFA re-registration, revoke sessions and fix TAP sign-in problems."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userdevicesettings"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# mfa-method-reset-and-reregistration

Goal: a user with a lost or new phone regains MFA quickly, and the reset cannot be abused to take over the account.

## Before acting
Verify identity to the highest standard you have; an MFA reset hands over the account. Microsoft says a TAP also eases recovery when a user loses or forgets a strong method. For a lost phone, also revoke sessions.

## Option A: Temporary Access Pass
- Policy first: Entra admin centre, Entra ID > Authentication methods > Policies > Temporary Access Pass, Enable, choose users/groups (Authentication Policy Administrator). You can create a TAP for any user, but only users in the policy can sign in with it.
- Policy defaults: minimum lifetime 1 hour, maximum 8 hours, default 1 hour (range 10 to 43,200 minutes); one-time use false; length 8 (range 8 to 48). Enforcing one-time use makes every pass one-time.
- Create: Entra ID > Users > user > Authentication methods > Add authentication method > Temporary Access Pass; set start time or duration. Note the value before selecting OK; it cannot be shown again.
- Roles: Authentication Administrators create/delete/view TAPs for members (not themselves); Privileged Authentication Administrators also for admins.
- PowerShell: `New-MgUserAuthenticationTemporaryAccessPassMethod -UserId user2@contoso.com -BodyParameter $propertiesJSON` with `isUsableOnce` and `startDateTime`. `Get-` and `Remove-MgUserAuthenticationTemporaryAccessPassMethod` exist.
- User opens Security info, enters their UPN, then the TAP, and registers a new method (for example FIDO2 key or Authenticator passkey / phone sign-in). A TAP does not replace the password. They should remove old methods after registering.
- One TAP per user; a new one overrides the existing one.
- Limits: a one-time TAP must finish passwordless registration within 10 minutes of sign-in (not for multiuse). TAP does not work with the NPS extension or the AD FS adapter. Users in SSPR or ID Protection MFA registration policy scope are sent to interrupt-mode registration, which does not support FIDO2 or phone sign-in. Changes can take minutes to replicate.
- Expiry: an expired or deleted TAP cannot authenticate, but sessions already established are not invalidated; tokens issued are capped at the TAP expiry. Use sign-in frequency Conditional Access to limit session length.
- External guests cannot get a TAP ("Temporary Access Pass cannot be added to an external guest user"); internal guests can.
- Windows setup: during Entra join a TAP can join the device and register Windows Hello for Business; on already-joined or hybrid-joined devices the user must first sign in another way.

## Option B: change methods or require re-register
Entra ID > Users > user > Authentication methods (at least Authentication Administrator):
- Add or change a phone number with + Add authentication method.
- Require re-register MFA: deactivates hardware OATH tokens and deletes phone numbers, Microsoft Authenticator apps and software OATH tokens; the user is asked to set up a new method at next sign-in if needed.
- Revoke sessions: invalidates refresh tokens, forcing reauthentication.
- Reset password: assigns a temporary password to change at next sign-in.
- Deleting app passwords is under Multifactor authentication > Manage user settings; non-browser apps using them stop working.
- Users manage their own methods in Security info; admins cannot edit public profile phone fields for MFA (those should not be used for MFA).
- Graph PowerShell phone methods: `Get-`, `New-` and `Remove-MgUserAuthenticationPhoneMethod`.

## Troubleshooting TAP sign-in
TAP not offered, or "blocked due to User Credential Policy": user not in the TAP policy scope; no valid TAP; a one-time TAP already used; or a multiuse TAP while the policy requires one-time.

## Verify
User signs in with the new method, Authentication methods shows only current methods, and the ticket records how identity was verified.

## Checked
Date: 2026-11-09. Confirmed in the two Microsoft Learn pages. Removed as unconfirmed: the Graph authentication methods overview source (not read), the aka.ms/mysecurityinfo address, Revoke-MgUserSignInSession and Remove-MgUserAuthenticationMicrosoftAuthenticatorMethod commands, Authenticator cloud backup advice, SMS-only gotcha, FIDO2 key deletion, the trusted-location policy note and sign-in log monitoring advice.
Method: docs-checked 2026-11-09 against the two Microsoft Learn pages listed in sources, downloaded and read in full.
