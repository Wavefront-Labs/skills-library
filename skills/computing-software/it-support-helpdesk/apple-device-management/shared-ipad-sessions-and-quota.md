---
id: computing-software.it-support-helpdesk.apple-device-management.shared-ipad-sessions-and-quota
name: shared-ipad-sessions-and-quota
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, shared-ipad, quota, temporary-session]
level: practitioner
status: docs-checked
description: "Tune Shared iPad quota size, resident users, session timeouts and temporary sessions with the SharedDeviceConfiguration setting of the Settings command."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/settings.yaml"
  - "https://support.apple.com/guide/deployment/prepare-shared-ipad-dep6fa9dd532/web"
  - "https://support.apple.com/guide/deployment/shared-ipad-overview-dep9a34c2ba2/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shared-ipad-sessions-and-quota

Goal: keep Shared iPad storage and sessions predictable.
- These are keys of the `SharedDeviceConfiguration` setting of the MDM Settings command (`Item` = `SharedDeviceConfiguration`), for Shared iPad on iOS or iPadOS 13.4 or later. They are not a configuration profile payload; `com.apple.shareddeviceconfiguration` is the Lock Screen Message payload.
- `QuotaSize` (integer, megabytes): quota for each user, or the minimum if the quota is too small. For Temporary Session guests it is available on iOS 17 or later.
- `ResidentUsers` (integer): the expected number of users; if above what the device supports, the MDM uses the device maximum. The older `MaximumResidentUsers` setting was deprecated in iOS 13.4 in favour of this one. With neither a quota nor a user count set, Shared iPad uses a default of 10 users.
- `UserSessionTimeout` (seconds, iOS 14.5 or later): the user session logs out after that much inactivity; minimum 30, 0 removes the timeout. `TemporarySessionTimeout` works the same for guests. `TemporarySessionOnly` (boolean, default false, iOS 14.5 or later): true shows only the Guest pane.
- `OnlineAuthenticationGracePeriod` (days, iOS 16.0 or later): existing users are verified locally by passcode; after this many days online authentication is required, and 0 requires it every time. `ManagedAppleIDDefaultDomains` (iOS 16.0 or later) lists sign-in domains; if more than 3 are listed the system shows 3 at random.
- Resetting a quota or user count needs users cleared from the device first. When the maximum is reached, a new sign-in removes a user whose data has finished syncing; if none are synced the new sign-in fails.
- Storage planning: on 32 GB iPads each user gets a minimum of 1 GB, on 64 GB or more 2 GB. Apple recommends the lowest quota that works, to maximise cached users and speed sign-in.
Practice: set the quota for the smallest-storage model in the fleet, record the chosen values in the build standard, and run updates outside class time.
Gotcha: when the device is full and no user has finished syncing, new logins fail; lower `ResidentUsers` or clear users.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read: the `MaximumResidentUsers` and `SharedDeviceConfiguration` sections of the apple/device-management Settings command YAML (a search then read of those sections, not the whole 1,300-line file); Apple Platform Deployment "Prepare Shared iPad" and "Shared iPad overview" in full.
- Corrected: the original named a key `OnlineUserTimeout`, which does not exist (the keys are `UserSessionTimeout` and `OnlineAuthenticationGracePeriod`), and described the keys as a Shared iPad configuration payload; they belong to the Settings command.
- Removed as unconfirmed: "Bind schedule updates after hours" as a feature, "monitor storage in inventory", "quota values show in device info" and the "login works after a sync" Verify step.
- The original source URL (shared-ipad-dep2d0e6e0f2) is not a real page and was replaced.
