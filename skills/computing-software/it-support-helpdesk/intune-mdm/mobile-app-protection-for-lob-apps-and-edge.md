---
id: computing-software.it-support-helpdesk.intune-mdm.mobile-app-protection-for-lob-apps-and-edge
name: mobile-app-protection-for-lob-apps-and-edge
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, app-wrapping-tool, edge-mobile-managed, jailbreak-detection, intune-app-sdk, conditional-launch, mam]
level: practitioner
status: docs-checked
description: "Protect in-house mobile apps with the Intune App SDK or App Wrapping Tool, configure Edge for iOS and Android with app config keys, and block jailbroken or rooted devices in MAM."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/developer/apps-prepare-mobile-application-management
  - https://learn.microsoft.com/en-us/mem/intune/apps/manage-microsoft-edge
  - https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy-settings-ios
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mobile-app-protection-for-lob-apps-and-edge

## LOB apps: SDK vs App Wrapping Tool
| Option | When (per Microsoft) |
|---|---|
| App Wrapping Tool | Internal LOB apps not on the Apple App Store or Google Play; no source code needed, but valid signing credentials are; apps you did not develop; minimal user authentication. Command-line tool for Android and iOS |
| Intune App SDK | Apps in the public stores, developers who can integrate it, frequently updated apps; any app including LOB can use it |
- The wrapping tool does not support apps from the App Store or Google Play. For ISV apps, check the ISV supports the wrapped app.
- Intune releases wrapping tool updates regularly; fold them into your release cycle so apps support the newest policy settings.
- Both support, among others: restricting web content to a managed browser, PIN and credentials, offline grace period, blocking jailbroken or rooted devices, min app version, min OS, Play Integrity verdict (Android), MAM without enrollment and full wipe.
- Only the SDK supports: selective wipe in multi-identity scenarios, prevent "Save as", targeted app configuration over the MAM channel, multi-identity, customizable style, max MTD risk level, and the Require app protection policy CA grant.
- Guidance covers native Android and iOS (Obj-C, Swift) only; other platforms may build plug-ins on the native SDK.

## Edge for iOS and Android
- Under Enterprise enhanced data protection (Level 2) the setting Restrict web content transfer with other apps is Microsoft Edge, so protected Outlook and Teams open links in Edge.
- Managed app configuration keys:
  - `com.microsoft.intune.mam.managedbrowser.homepage` (homepage shortcut; replaced by the Homepage shortcut URL UI)
  - `com.microsoft.intune.mam.managedbrowser.bookmarks` (list of Title|URL pairs, pairs separated by `||`; shown only in the work account, users cannot delete them)
  - `com.microsoft.intune.mam.managedbrowser.AllowListURLs` and `BlockListURLs`
  - `com.microsoft.intune.mam.managedbrowser.managedTopSites` (up to eight shortcuts including the homepage)
- Application Proxy redirection lets users reach intranet sites by internal URL; the user must be assigned to the Application Proxy app, and Microsoft apps need Restrict web content transfer set to Microsoft Edge.

## Jailbroken or rooted devices
App protection conditional launch has a Jailbroken/rooted devices setting (no value) with actions Block access or Wipe data. Users can still use the app for personal tasks but must use another device for work data. Related health checks on iOS: Min OS version, Max OS version (SDK 14.4.0 or later), Min app version, Min SDK version, Max allowed device threat level, Offline grace period (iOS defaults 1440 minutes block, 90 days wipe) and Max PIN attempts (default 5).

## Checked
Date: 2026-11-08. Read: "Prepare Line-of-Business Apps for App Protection Policies" (updated 2026-04-08), the iOS conditional launch settings, and the Edge for iOS and Android configuration sections of "Manage web access by using Microsoft Edge". Removed as unconfirmed: re-signing and re-wrap advice, the broker app statement for wrapped apps, personal and work profile switching in Edge, all compliance policy jailbreak or root settings and their Conditional Access link, Play Integrity wording as a compliance setting, and the Verify steps.
Method: documentation only; no commands were run.
