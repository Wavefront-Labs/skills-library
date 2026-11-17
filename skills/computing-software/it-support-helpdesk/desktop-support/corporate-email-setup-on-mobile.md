---
id: computing-software.it-support-helpdesk.desktop-support.corporate-email-setup-on-mobile
name: corporate-email-setup-on-mobile
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, mobile-device-support, mobile-email-setup, outlook-mobile, exchange-activesync, app-protection, intune-company-portal, conditional-access, ios-mail, comptia-a-plus]
level: intro
status: draft
description: "Set up work email on iPhone and Android the way policy expects (Outlook app plus app protection or enrolment), and fix blocked, quarantined or not-syncing mobile mail."
sources:
  - "https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/outlook-for-ios-and-android/outlook-for-ios-and-android"
  - "https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-device-compliance"
  - "https://learn.microsoft.com/en-us/exchange/clients/exchange-activesync/exchange-activesync"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# corporate-email-setup-on-mobile

Goal: the user has work mail, calendar and contacts on their phone through
the approved app, in a way that passes conditional access.

## Know the policy first
Most Microsoft 365 tenants require one of:
- **Approved client app / app protection policy**: Outlook for iOS/Android
  (plus Microsoft Authenticator or Company Portal as broker). Native Mail /
  Gmail apps are blocked.
- **Compliant device**: phone enrolled in Intune via Company Portal.
Check Entra → Conditional access policies or the internal KB before
walking the user through anything.

## Set up (BYOD, app protection)
1. Install **Microsoft Authenticator** (iOS broker) or **Company Portal**
   (Android broker — required even when not enrolling).
2. Install **Outlook**, add account with the work address, complete MFA.
3. Accept "Your organisation is now protecting its data in this app"; set
   the app PIN if prompted.

## Common failures
| Symptom | Cause / fix |
|---|---|
| "Your IT department requires additional protection" loop | broker app missing — install Authenticator/Company Portal and sign in there |
| "You can't get there from here" | CA requires compliant device — enrol via Company Portal |
| Native Mail: "Cannot get mail", mail blocked | legacy ActiveSync blocked by policy — use Outlook |
| Mail syncs, contacts don't appear in phone dialler | app protection blocks contact export — allowed only if policy permits "Save contacts" |
| Quarantined device (EAS) | Exchange admin centre → Mobile → Quarantine → allow, or `Set-CASMailbox -ActiveSyncAllowedDeviceIDs` |
| Old device still syncing after replacement | remove from user's mobile devices list (`Get-MobileDevice -Mailbox`), wipe account if lost |

## Gotchas
- iOS Focus/notification settings and Android battery optimisation kill
  Outlook notifications — whitelist Outlook from battery optimisation.
- Shared mailboxes can be added in Outlook mobile (Add shared mailbox),
  only if the user has Full Access.
- Password change → mobile prompts; repeated wrong-password attempts from the
  phone can lock the AD account.

## Verify
User receives a test email and calendar invite on the phone within a minute,
and Entra sign-in logs show the sign-in as successful with the expected
client app and CA policy result.
