---
id: computing-software.digital-privacy-hygiene.privacy-configuration.deleting-mobile-advertising-ids
name: deleting-mobile-advertising-ids
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, delete-advertising-id, advertising-id, idfa, app-tracking-transparency, android, ios, smart-tv]
level: intro
status: docs-checked
description: "Delete or zero the advertising IDs on Android, iPhone and Windows that ad networks and data brokers use to link your app activity across apps."
sources:
  - "https://support.google.com/googleplay/android-developer/answer/6048248"
  - "https://support.apple.com/en-us/102420"
  - "https://www.apple.com/legal/privacy/data/en/apple-advertising/"
  - "https://learn.microsoft.com/en-us/windows/privacy/manage-connections-from-windows-operating-system-components-to-microsoft-services"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting mobile advertising IDs

**Goal:** the advertising ID is the identifier ad networks use to join your activity across apps. Remove or zero it.
Menu labels vary by Android maker and OS version.

## Android
Google's Advertising ID page: Settings > **Privacy** > **Ads** > **Delete Advertising ID** and confirm (or **Reset
Advertising ID** for a new value). After deletion, apps that ask for the ID receive a string of zeros (Google Play
services change that began on Android 12 and reached all Google Play devices from 2022-04-01). On some older Android
versions: Settings > Privacy > Advanced > Ads > turn on **Opt out of Ads Personalization**.
Apps may have their own ad settings that still affect which ads you see.

## iPhone and iPad (App Tracking Transparency, iOS 14.5 and later)
- Settings > Privacy & Security > **Tracking** lists apps that asked to track; toggle each one off or on.
- Turning off **Allow Apps to Request to Track** stops the prompts: every app that asks is treated as if you chose Ask
  App Not to Track, and cannot get the advertising identifier (IDFA).
- Asking an app not to track also bars it from tracking via other identifiers such as your email address, and the
  app still works fully.
- The toggle cannot be turned on for child or under-18 accounts, institution-managed Apple Accounts, devices with a
  configuration profile that limits tracking, or an Apple Account created in the last 3 days.
- Apple's own advertising: Settings > Privacy & Security > **Apple Advertising** > Personalized Ads off (Mac:
  System Settings). Apple states its ad platform does not share user data with data brokers.
- Apple TV: Settings > General > Privacy & Security > Tracking.

## Windows
Microsoft's documentation lists the Windows setting "Let apps use advertising ID" (labelled differently by release);
turning it off in the UI turns off the ID rather than only resetting it. Admins can enable the Group Policy
Computer Configuration > Administrative Templates > System > User Profiles > **Turn off the advertising ID**.

## Limits
- Turning off the ID does not stop other ways of linking you; the Apple page itself notes that tracking can use
  other identifying information, which is why the permission also covers email addresses.
- Smart TVs and streaming boxes have their own ad settings that were not checked here; see the smart TV skill.

## Verify
- [ ] Android: Settings > Privacy > Ads shows the ID deleted.
- [ ] iPhone: Allow Apps to Request to Track is off, or the app list shows only apps you chose.

## Checked
Checked 2026-11-08 against the full text of Google Play Console Help "Advertising ID", Apple Support 102420 ("If an
app asks to track your activity"), Apple's "Apple Advertising & Privacy" page and the Windows connection endpoints
page (section 18.1 General). Removed what none of them state: the FTC cases and broker names (the FTC page is blocked
to scripts), the Android "Security & privacy" label, Roku, Fire TV and Google TV menu paths, the Google My Ad Center
step and the Windows Settings click path.
Method: documentation only; no commands were run.
