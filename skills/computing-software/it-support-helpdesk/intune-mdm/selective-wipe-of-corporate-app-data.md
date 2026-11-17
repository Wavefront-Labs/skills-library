---
id: computing-software.it-support-helpdesk.intune-mdm.selective-wipe-of-corporate-app-data
name: selective-wipe-of-corporate-app-data
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, selective-wipe, app-selective-wipe, mam-wipe, wipe-requests, leaver, lost-device, intune]
level: practitioner
status: docs-checked
description: "Remove only corporate data from managed apps with an Intune app selective wipe: device and user requests, triggers, monitoring and deleting requests, and device wipe contrast."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-selective-wipe"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# selective-wipe-of-corporate-app-data

An **app selective wipe** removes company data from Intune managed apps (apps with the Intune App SDK and at least one
enabled, licensed user in your organisation) without wiping personal data. It suits lost or stolen devices and leavers,
especially employee-owned devices. Supported platforms: iOS/iPadOS, Android and Windows. On Android and iOS, deploying app
protection policies is required to enable it.

## Device-based request
1. Intune admin center > Apps > **App selective wipe** > Create wipe request.
2. Select user, then Select the device, then Create.
3. The service creates and tracks a separate wipe request for each protected app on the device, so one user can show several requests.

## User-based request
Apps > App selective wipe > **User-Level Wipe** > Add > pick the user. This issues wipe commands to all apps on all of the
user's devices, and the user keeps getting wipe commands at every check-in from all devices. To re-enable the user, remove
them from the list.

## Other triggers
- A selective wipe can be configured as an action in app protection policy Access settings when conditions are not met
  (for example the offline grace period "Wipe data" setting).
- For MDM-enrolled devices, MDM selective wipe is the Retire action ("Remove devices - retire"). Full device wipe and MDM
  selective wipe work only on devices enrolled in Intune MDM; MAM selective wipe does not need enrolment.
- A full device **Wipe** factory resets the device and removes personal data too; not for BYOD "company data only" cases.
  A tenant can submit up to 500 Wipe actions per day.

## When it happens
The user must open the app for the wipe to occur, and it may take up to 30 minutes after the request. If the user is in the
app, the Intune SDK checks every 30 minutes for a request, and also checks when the app is first launched and the user signs in
with their work or school account. Because it depends on the app, a powered-off phone or an unopened app stays Pending, so
for real exposure add identity-side controls under your own offboarding process.

## What is removed
Company app data from the app. Contacts synced directly from the app to the native address book are removed; contacts synced
from the native address book to another external source cannot be wiped (currently Outlook only). On iOS 16 and later the
device name in wipe actions and status is generic.

## Monitoring
Apps > App selective wipe lists requests grouped by user, with device name, device type and status (pending, failed or
successful). Completed requests stay in the report for 4 days. A request left Pending stays for the Offline grace period
wipe data value plus 4 days (94 days by default). Pending requests display until you delete them: right-click and choose
Delete wipe request. User-level wipes stay until an administrator deletes them.

## Verify
Each per-app request shows successful; opening the app shows the work account data removed and personal data intact.

## Checked
Date: 2026-11-08. Read in full: Intune "How to wipe only corporate data from Intune-managed apps" (updated 2026-04-14),
the Selective wipe section of the app protection policy overview, and "Wipe devices with Microsoft Intune" (2026-09-25).
Removed as unconfirmed: the specific data list (Outlook cache, OneDrive/Teams, Edge), Android work profile advice,
Entra revoke-sessions and password reset steps, "removing the user from the APP assignment does not wipe", the uninstall and
per-instance gotchas, and the Verify sign-in-log step.
Method: documentation only; no commands were run.
