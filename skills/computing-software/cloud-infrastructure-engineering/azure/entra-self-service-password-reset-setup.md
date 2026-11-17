---
id: computing-software.cloud-infrastructure-engineering.azure.entra-self-service-password-reset-setup
name: entra-self-service-password-reset-setup
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, sspr, self-service-password-reset, authentication-methods, password-writeback]
level: practitioner
status: docs-checked
description: "How Entra self-service password reset decides eligibility, which methods and registration settings matter, notifications, and on-premises password writeback."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra self-service password reset (SSPR)

**Goal:** users reset or unlock their own passwords with strong verification, cutting help-desk load.

## What SSPR checks
At the SSPR portal the user enters a user ID and passes a captcha. Entra then checks that the user is enabled for SSPR, has registered enough methods for the policy (one or two), and where the password is managed. If an Entra administrator role is assigned, the strong two-gate policy is enforced regardless. If the password is managed on-premises (federated, pass-through authentication or password hash sync) and writeback is not configured, the user is told to contact an administrator.

## Methods and registration
- Methods available for SSPR: Microsoft Authenticator push notifications, hardware OATH tokens (preview), software OATH tokens, SMS, voice call, and email OTP.
- The number of methods required to reset is one or two. Microsoft recommends users register two or more.
- Authenticator, software OATH tokens and hardware OATH tokens count as a single method for SSPR, so they cannot together satisfy a two-method requirement. Authenticator cannot be the only method when one is required, and with two required, Authenticator plus only one other is not allowed.
- Raising the requirement from one to two blocks users who have only one method registered; removing a method from the policy blocks users who lack data for the remaining ones.
- Require registration at sign-in: applies to modern authentication or browser sign-in to Microsoft 365, the Entra admin center, the Access Panel, federated apps and custom Entra apps. Without it users can register at https://aka.ms/ssprsetup. Re-confirmation of authentication info can be 0 to 730 days (0 means never) and is available only when registration is required.
- Notifications: optionally email users when they reset, and notify Global Administrators when another administrator resets their password.

## Hybrid: password writeback
Writeback to the on-premises directory is configured through Microsoft Entra Connect cloud sync and can be switched on or off in the admin center without reconfiguring Connect. With it off, federated, pass-through and password-hash-sync users cannot reset. A separate option lets users unlock their on-premises account without resetting the password; by default a reset also unlocks. SSPR behaves like an admin-initiated reset in Active Directory, so third-party password filters must be configured to apply to that scenario; Entra password protection for AD DS is supported by default.

## Gotchas
- Users without registered methods cannot reset until an administrator resets their password.
- SSPR for administrators is not enabled in the tenant by default per the page; admin roles are held to the two-method policy.
- Personal Microsoft accounts granted guest access cannot use Entra SSPR.

## Verify
A registered test user completes the reset from https://aka.ms/sspr; for hybrid, the new password works on-premises.

## Checked
Confirmed against the concept page "How it works: Microsoft Entra self-service password reset" (last updated 2026-10-06 on the page), 2026-11-08. Removed: admin center menu paths, licence requirements, sync-account permissions, Service Bus connectivity, Conditional Access registration user action, pilot-group rollout steps and audit log names, because the page does not state them.
Method: docs-only read of cited pages, 2026-11-08
