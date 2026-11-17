---
id: computing-software.digital-privacy-hygiene.privacy-configuration.clearing-windows-activity-history
name: clearing-windows-activity-history
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, windows-activity-history, windows, microsoft-account, privacy-dashboard, group-policy]
level: intro
status: docs-checked
description: "Turn off and clear Windows activity history on the PC, check the cloud copy is gone, and lock it off with Group Policy on shared machines."
sources:
  - "https://support.microsoft.com/en-us/windows/windows-activity-history-and-your-privacy-2b279964-44ec-8c2f-e0c2-6779b07d2cbd"
  - "https://account.microsoft.com/privacy"
  - "https://learn.microsoft.com/en-us/windows/privacy/manage-connections-from-windows-operating-system-components-to-microsoft-services"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clearing Windows activity history

**Goal:** stop Windows recording which apps, files and sites you used, and remove what is already stored.

## On the PC (Windows 11)
Settings > Privacy & security > **Activity history**:
- **Store my activity history on this device**: Off. Features that rely on it, such as Timeline, stop working.
- **Clear activity history for this account**: select **Clear history**.

Activity history is kept per account (local, Microsoft or work/school) associated with the device. Hiding an account in
the list does not delete its data.

## Windows 10
Settings > Privacy > Activity history: clear the **Store my activity history on this device** checkbox, then under
**Clear activity history** select **Clear**. In Timeline you can also clear single activities or a whole day.

## The cloud copy
Microsoft deprecated the option to send activity history to Microsoft in the 23 January 2024 updates (Windows 11
23H2/22H2 KB5034204, Windows 10 22H2 KB5034203). Older builds still show it: turn it off or update. If cloud history was
stored before that update, **Clear** also deletes it; otherwise it is deleted automatically within 30 days of the last
sync. The Microsoft account privacy dashboard (account.microsoft.com/privacy) is where other data Microsoft holds is
reviewed; it needs sign-in, so its categories are not covered here.

## Lock it down (shared PCs)
Group Policy, Computer Configuration > Administrative Templates > System > OS Policies. Set each to Disabled:
- **Enables Activity Feed**
- **Allow publishing of User Activities**
- **Allow upload of User Activities**

## Verify
- [ ] Activity history storing is off and the history has been cleared for each account on the PC.
- [ ] Any older build no longer has the send-to-Microsoft option on.

## Checked
Date: 2026-11-08.
Confirmed against the Microsoft Support page "Windows activity history and your privacy" (Windows 11 and 10 menu paths,
setting names, deprecation dates and KB numbers, 30-day cloud deletion) and the Learn page on managing connections from
Windows components (the three OS Policies Group Policy names and path). Removed: privacy dashboard category list, search
permission, File Explorer and Start menu recent-items steps (not on the cited pages), and Copilot/Cortana voice data.
The account.microsoft.com page requires sign-in and was not read.
Method: documentation only; no commands were run.
