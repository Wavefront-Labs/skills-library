---
id: computing-software.it-support-helpdesk.intune-mdm.app-configuration-policies
name: app-configuration-policies
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, app-configuration, managed-devices, managed-apps, outlook, tokens, mam, intune]
level: practitioner
status: docs-checked
description: "Use Intune app configuration policies for managed devices vs managed apps: key-value or XML settings, account-restriction keys, tokens, check-in timing, validating delivery."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-configuration-policies-overview"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-configuration-policies-outlook"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-configuration-policies-use-ios"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# app-configuration-policies

App configuration (app config) supplies settings to an app before the user runs it,
typically the first time the app checks for them. Which keys exist, and how they behave,
is decided by the app developer: get keys and values from the app vendor.

## Two channels
In the Intune admin center: Apps > Configuration > Create > **Managed devices** or **Managed apps**.

| Type | Delivered via | Requirement |
|---|---|---|
| **Managed devices** | MDM OS channel (Managed App Configuration on iOS/iPadOS, Android in the Enterprise channel) | Device enrolled; app pinned to the management profile (iOS/iPadOS), or deployed through Managed Google Play or as a directly deployed LOB app (Android) |
| **Managed apps** | MAM channel | App integrates the Intune App SDK or was wrapped with the Intune Wrapping Tool and supports app protection policies; enrollment state and delivery method do not matter. Android needs 10.0 or higher |

Managed devices scenarios: only allow work or school accounts; account setup; general
settings; S/MIME. Managed apps scenarios: general settings; S/MIME; advanced app
protection data protection settings. Some apps let the user override (Outlook Focused
Inbox respects the user's setting). App config for managed devices cannot configure DDM apps.

Check-in: managed apps check for app configuration status every 30 minutes when
deployed with an app protection policy; if no app protection policy is assigned to the
user the interval is 720 minutes.

## iOS/iPadOS managed devices: format and keys
Choose Configuration settings format: **configuration designer** (key, value type
Integer/Real/String/Boolean, value; keys are case sensitive) or **Enter XML data** (a
property list; Intune validates the format but not that the app accepts it). The `{{` and
`}}` characters are for tokens only.

Account restriction keys (managed devices, iOS/iPadOS):

| Key | Values |
|---|---|
| `IntuneMAMAllowedAccountsOnly` | `Enabled`: only the account in `IntuneMAMUPN` is allowed; anything else (case-insensitive non-match to Enabled) allows any account |
| `IntuneMAMUPN` | UPN of the allowed account; on Intune-enrolled devices `{{userprincipalname}}` may be used |
| `IntuneMAMOID` | User Object ID; `{{userid}}` may be used |
| `IntuneMAMRequireAccounts` | `Enabled`: the managed account in `IntuneMAMUPN` must be signed in to receive Org data (needs App SDK for iOS 12.3.3 or later, an app protection policy, and "Receive data from other apps" set to "All apps with incoming Org data") |

Tokens documented for the property list: `{{userprincipalname}}`, `{{mail}}`,
`{{partialupn}}`, `{{accountid}}`, `{{deviceid}}`, `{{userid}}`, `{{username}}`,
`{{serialnumber}}`, `{{serialnumberlast4digits}}`, `{{aaddeviceid}}`, `{{issupervised}}`,
`{{OnPremisesSamAccountName}}`.

## Outlook
Outlook for iOS and Android supports app config through the MDM channel or the app
protection policy channel for: only allow work or school accounts, general settings,
S/MIME and data protection settings. The key-by-key list lives in Microsoft's separate
"Deploying Outlook for iOS and Android app configuration settings" article, which this
skill does not reproduce. Outlook guidance also expects a Conditional Access policy
(Require approved client apps or app protection policy) and app protection policies;
app-based Conditional Access needs Microsoft Authenticator on iOS and Company Portal on Android.

## Checking delivery
- Admin center: Apps > All Apps > the app > Monitor > Device install status; and
  Devices > All devices > a device > App configuration (assigned policies and state).
- Diagnostic logs, iOS/iPadOS: install Microsoft Edge, open `about:intunehelp`, Get
  Started > Share Logs, open `IntuneMAMDiagnostics.txt`; search `ApplicationConfiguration`
  (unmanaged) or `AppConfig` (managed).
- Android managed devices: over USB open
  `Android\data\com.microsoft.windowsintune.companyportal`, the Files folder, then
  `OMADMLog_0`; search `AppConfigHelper`.
- If the log shows the parameter applying but it does not work, the problem is in the
  app's implementation: contact the app developer.

## Gotchas
- Assignment supports include/exclude groups, All Users/All Devices built-in groups, and
  assignment filters for managed iOS and Android devices.
- Android Enterprise policies pick an enrollment type: All Profile Types (no
  certificate profile association), Fully Managed/Dedicated/Corporate-Owned Work Profile
  Only, or Personally-Owned Work Profile Only.
- A Gmail or Nine profile deployed to a userless dedicated device work profile fails
  because Intune cannot resolve the user.

## Checked
Date: 2026-11-07. Read in full: the app configuration overview, the Outlook messaging
access article and the iOS/iPadOS managed devices article (the XML-sample sections and
Company Portal ADE sections were read but are not reproduced).
Removed as unconfirmed: the `com.microsoft.outlook.EmailProfile.*` Outlook keys (not on
any cited page), "don't set the same key in both channels", appconfig.org, the
`<ServerURL>` plist example, Edge `edge://policy`, the iOS Settings profile path, the
Outlook "Collect diagnostics" path, the Android configuration designer remark, the
"targeting" rule that managed apps configs target only users, the Zoom/Wi-Fi/Edge
bookmarks examples, and the "policy status shows Succeeded" Verify step. Added the
documented check-in intervals, Android 10 floor, DDM limitation and the real log search
terms.
Method: documentation only; no commands were run.
