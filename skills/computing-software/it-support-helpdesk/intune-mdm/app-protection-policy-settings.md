---
id: computing-software.it-support-helpdesk.intune-mdm.app-protection-policy-settings
name: app-protection-policy-settings
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, app-protection, mam, data-protection-framework, conditional-launch, pin, intune]
level: practitioner
status: docs-checked
description: "Configure Intune app protection (MAM) settings: data transfer and save-as rules, cut/copy limits, PIN and access rules, conditional launch defaults, framework levels."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy-settings-ios"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy-settings-android"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-framework"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-configuration-policies-overview"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# app-protection-policy-settings

App protection policies (APP / MAM) are rules that keep an organization's data safe or
contained in a managed app, whether or not the device is enrolled.

## Start from the data protection framework
Three levels, each building on the previous. The framework's Core Microsoft Apps group
is Edge, Excel, Office, OneDrive, OneNote, Outlook, PowerPoint, SharePoint, Teams, To Do
and Word.

| Level | Microsoft recommends for | Settings the framework page lists |
|---|---|---|
| 1 Basic | Minimum for any enterprise device | PIN to access, encrypt org data, selective wipe; data transfer left open (send/receive "All apps", backup Allow, cut/copy "Any app", third-party keyboards Allow) |
| 2 Enhanced | Most users accessing sensitive data | Back up org data Block; cut/copy/paste "Policy managed apps with paste in"; restricted transfers; minimum OS version |
| 3 High | Users at uniquely high risk | Adds: receive data from "Policy managed apps", Open data into Org documents Block, third-party keyboards Block (iOS) / approved keyboards (Android), print org data Block, simple PIN Block, minimum PIN length 6, PIN reset every 365 days, max allowed threat level Secured, jailbroken/rooted Wipe data |

Policies are assigned through the Intune admin center; the framework page recommends
testing in rings (Quality Assurance, Preview, Production) before wide rollout.

## Data protection settings that cause tickets (iOS/iPadOS and Android pages)
| Setting | Notes from the pages |
|---|---|
| Send Org data to other apps | iOS options include All Apps, None and Policy managed apps (the page lists further variants) |
| Receive data from other apps | All Apps, None, Policy managed apps, All apps with incoming Org data (iOS) |
| Allow user to save copies to selected services | Android page lists OneDrive, SharePoint, Photo Library, Box, iManage, Egnyte and Local Storage; others are blocked |
| Cut and copy character limit for any app | Default 0; shares up to N characters with any app even when cut/copy/paste is restricted (iOS needs Intune SDK 9.0.14+; Android needs Company Portal 5.0.4364.0+) |
| Third party keyboards (iOS) | Block shows the user a one-time message; default Allow |
| Printing Org data | Default Allow |
| Sync policy managed app data with native apps or add-ins | Block stops saving to native Contacts, Calendar and widgets |
| Backup Org data | Defaults to Allow |
| Encrypt org data on enrolled devices (Android) | Default Require |

## Access requirements
PIN or biometrics, minimum PIN length (default 4), PIN reset after N days (default No),
Timeout (default 30 minutes) after which PIN overrides biometrics, "Recheck the access
requirements after (minutes of inactivity)" (default 30), and Work or school account
credentials for access (default Not required; if also PIN/biometric, the user sees both).

## Conditional launch
- Max PIN attempts (default 5): actions Reset PIN or Wipe data.
- Offline grace period: block access after 1440 minutes by default (a value under 30 is
  not recommended); wipe data after 90 days by default. Timers are per app, from last
  check-in.
- Min OS version and Min app version: actions include Warn (dismissible) and Block access.
- Jailbroken/rooted devices: Block access or Wipe data.
- Android: Play Integrity check with Basic integrity, or Basic integrity and device integrity.
- Max allowed device threat level (Secured, Low, Medium, High) needs the Intune MTD
  connector; actions Block access or Wipe data.

## Support tips
- Policy delivery to managed apps is checked on an interval: 30 minutes when an app
  protection policy is assigned (720 minutes for app configuration if none is).
- Validate with Microsoft Edge on the device at `about:Intunehelp`.

## Gotchas
- At level 3 the framework page tells you to set the dialer (Transfer telecommunication
  data to) so calling still works: a policy-managed dialer on Android, or a specific
  dialer app and its URL scheme on iOS/iPadOS.
- A too-strict save/transfer policy blocks legitimate workflows; adjust per app rather
  than loosening everything.

## Verify
On a test device, attempt each blocked action and confirm it is blocked for org data
while allowed paths still work.

## Checked
Date: 2026-11-07. Read in full: the data protection framework article (levels 1-3,
tables), and the app configuration overview note on check-in intervals. The iOS and
Android settings pages (about 42k characters each) were searched and read at the
Access requirements, Conditional launch and data transfer rows, not end to end.
Corrections: offline grace block default is 1440 minutes (skill said 720); level 3 is
not "stricter OS minimums" (level 2 already adds the minimum OS; level 3 adds keyboards,
PIN strength, threat level and print block); "Sync contacts to native app" renamed to
the real setting name. Removed unconfirmed user-visible error messages, the "message
names the policy setting" and org-data-by-account tips, and the `tel` scheme remark.
Method: documentation only; no commands were run.
