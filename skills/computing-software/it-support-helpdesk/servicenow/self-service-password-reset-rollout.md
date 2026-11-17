---
id: computing-software.it-support-helpdesk.servicenow.self-service-password-reset-rollout
name: self-service-password-reset-rollout
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, self-service-portal, self-service, sspr, password-reset, entra-id, authentication-methods, account-unlock]
level: practitioner
status: draft
description: "Roll out and support Entra ID self-service password reset: methods and policy, combined registration, password writeback for hybrid, user comms, and fixing common SSPR failures."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr-writeback"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/troubleshoot-sspr"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# self-service-password-reset-rollout
Goal: password resets and unlocks (often 20-30% of desk contacts) move to
self-service without weakening identity proofing.

## Configure (Entra admin center > Protection > Password reset)
- Scope: start with a pilot group, then All.
- Methods: require 2 methods for users (Authenticator app notification/
  code, SMS, email, security questions last resort). Admin roles always
  require 2 strong methods regardless.
- Registration: use **combined security info registration**
  (`https://aka.ms/mysecurityinfo`) so MFA and SSPR methods are one step;
  require registration at sign-in with a re-confirm period (e.g. 180 days).
- Notifications: notify users on reset; notify admins when other admins
  reset.

## Hybrid: password writeback
- Requires Entra Connect (or Cloud Sync) with **password writeback**
  enabled and Entra ID P1.
- Connector account needs Reset password, Change password, and write
  `lockoutTime`/`pwdLastSet` on user OUs.
- Enable "Allow users to unlock accounts without resetting".
- On-prem password policy (length, history, min age) still applies; a
  min password age of 1 day blocks a second reset the same day.

## Windows sign-in screen
Enable the "Reset password" link on the Windows login screen (Intune
setting `Authentication/AllowAadPasswordReset` for Entra-joined, or the
SSPR credential provider) so locked-out users can help themselves.

## Rollout comms
Announce, run a registration campaign, put the reset URL
(`https://aka.ms/sspr` / `passwordreset.microsoftonline.com`) on the desk
IVR message and lock screen, and have agents walk callers through SSPR
instead of resetting for them.

## Troubleshooting
- "Your account isn't enabled for password reset": user not in scoped
  group or not licensed.
- Writeback errors: check the Entra Connect event log (source
  PasswordResetService), connector permissions, and that the account is
  not protected by AdminSDHolder.
- Reset succeeds but old password still works on-prem: writeback off or
  replication delay between DCs.
- Audit: Entra > Audit logs, service "Self-service Password Management".

## Verify
Pilot users reset and unlock from the browser and Windows sign-in screen,
on-prem logins accept the new password, and reset calls trend down.
