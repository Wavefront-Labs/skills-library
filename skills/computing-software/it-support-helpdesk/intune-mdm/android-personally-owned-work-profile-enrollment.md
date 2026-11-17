---
id: computing-software.it-support-helpdesk.intune-mdm.android-personally-owned-work-profile-enrollment
name: android-personally-owned-work-profile-enrollment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, android-work-profile-enrollment, android-enterprise, work-profile, byod, company-portal, managed-google-play, intune, android-enrollment-troubleshooting]
level: practitioner
status: docs-checked
description: "Enroll and support Android personally owned work profile devices in Intune: web-based vs Company Portal enrollment, restrictions, user flow, limitations and remove or retire."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-work-profile-enroll"
  - "https://learn.microsoft.com/en-us/mem/intune/user-help/enroll-device-android-work-profile"
  - "https://support.google.com/work/android/answer/6191949"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# android-personally-owned-work-profile-enrollment

A work profile is a separate area on a personal Android device that holds work apps and data.
Intune manages the profile and its contents; personal apps and data stay separate and
unaffected. Google marks work apps with a briefcase icon and they sit in the launcher's Work
tab. Grey work icons can mean the profile is paused.

## Enrollment methods
| Method | Delivery | Status |
|---|---|---|
| Company Portal app | Custom DPC | Being phased out; migrates to web-based enrollment when enabled |
| Web-based enrollment | Android Management API | Default for new tenants; Company Portal not needed to enroll |

Web-based needs Chrome, Edge or Samsung browser. Entry points: Teams or Outlook (recommended,
when Conditional Access requires enrollment), the Company Portal app, or the URL
aka.ms/enrollmyandroid. Company Portal older than 2604.x is routed to app-based enrollment.

## Admin setup
1. Connect the Intune tenant to an Android Enterprise account; confirm Android Enterprise is
   available in the country or region.
2. Devices > Enrollment > Android tab > Enrollment Profiles > **Personally owned devices with a
   work profile**. Tick *Use web enrollment for all users...* to enable web-based enrollment.
   It applies at tenant level and cannot be reversed. If passkeys are the only accepted
   authentication method, leave it off and use Company Portal enrollment.
3. Optional device platform restriction (Enrollment options > Device platform restriction >
   Android restrictions): *Platform* Allow/Block for work profile and *Personally owned*
   Allow/Block. Personal devices are allowed by default. Block on *Personally owned* does not
   apply to AMAPI devices and is unreliable on Android 12+ with Custom DPC. Instead block work
   profile for all users and add a higher-priority allow restriction for an approved group.
   If work profile is blocked, devices fall back to device administrator unless that is blocked
   too; DA is deprecated and unavailable on GMS devices.
4. Device enrollment managers can enroll up to 10 devices per account.

## User flow (Company Portal)
Use the primary user account (secondary accounts are not supported). Install Company Portal
from Google Play > sign in > **BEGIN** > privacy screen **CONTINUE** > accept Google terms
(Samsung adds a Knox privacy screen) > wait for profile creation > sign in again when
prompted > **RESOLVE** any required settings > **CONFIRM DEVICE SETTINGS** > **DONE**.
Intune installs Microsoft Intune, Company Portal, Microsoft Authenticator and a hidden Android
Device Policy app.

## Common failures
- Cannot create profile or enroll: outdated Google Play services (update), Android Enterprise
  not available in the country, or enrolling from a secondary user.
- Private space (Android 15) is a personal profile and is unsupported. Enrolling it creates a
  second device administrator record.
- Web enrollment: users already on an old Custom DPC profile may get an error re-enrolling
  from the personal profile; open the app in the work profile instead. Skip any browser prompt
  to add the work account. Entra Terms of Use before profile creation are unsupported.
- A device already enrolled that lands on Get Started may only need Workplace Join redone.

## Remove or reset
- User: Settings > Passwords and accounts > Work tab > Remove Work Profile, which deletes the
  profile's apps and data.
- IT: the **Retire** action returns the device to a state ready to re-enroll.

## Checked
Date: 2026-11-08. Read in full: Intune "Set up enrollment of Android Enterprise personally owned work profile devices" (updated 2026-07-08), the user help page "Enroll device with Android work profile" (updated 2026-04-08), and Google "What is an Android Work Profile?". Removed as unconfirmed: the compliance policy settings list, the failure table causes (OEM block, license, Pending apps, device limit, Secure Folder), the user-pause note about notifications, copy/paste guidance, and the claim that Retire removes only the work profile.
Method: documentation only; no commands were run.
