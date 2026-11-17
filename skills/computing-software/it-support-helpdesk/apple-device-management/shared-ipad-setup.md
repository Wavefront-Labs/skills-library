---
id: computing-software.it-support-helpdesk.apple-device-management.shared-ipad-setup
name: shared-ipad-setup
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, shared-ipad, managed-apple-accounts, education]
level: practitioner
status: docs-checked
description: "Set up Shared iPad with Managed Apple Accounts so several students or staff share supervised iPads, covering requirements, ADE options, user space and caching."
sources:
  - "https://support.apple.com/guide/deployment/shared-ipad-overview-dep9a34c2ba2/web"
  - "https://support.apple.com/guide/deployment/prepare-shared-ipad-dep6fa9dd532/web"
  - "https://support.apple.com/guide/deployment/automated-device-enrollment-management-dep73069dd57/web"
  - "https://support.apple.com/guide/deployment/restrictions-for-supervised-devices-dep6b5ae23e9/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shared-ipad-setup

Goal: several people share one organisation-owned iPad and each keeps personal data.
- Requirements: a device management service, Managed Apple Accounts that the organisation owns, and a supervised iPad with at least 32 GB of storage. Supported: all iPad Pro models, iPad (5th generation) or later, iPad Air 2 or later, iPad mini (4th generation) or later.
- Enable it in the Automated Device Enrolment settings your MDM exposes: "Configure as Shared iPad" and "Number of Shared iPad users" (iPadOS 9.3 or later). Apple advises keeping the user count low.
- User space: if you set neither a quota nor a user count (iPadOS 13.4 or later), Shared iPad uses a maximum of 10 users. On 32 GB devices 10 GB goes to the system and 8 GB to apps and media, the rest is divided among users with a 1 GB minimum each. On 64 GB or more, 10 GB goes to the system and 16 GB to apps and media, with a 2 GB minimum per user. When more space is needed for a new user the oldest user's local data is removed. Apple notes Photos will not sync with a Managed Apple Account at a 1 GB quota.
- Content caching matters: configure it to cache iCloud data so signing in on a previously used iPad is quick; plan for users to return to the same device.
- Guests: any user can tap Guest at the login screen for a Temporary Session (iPadOS 13.4 or later); all of that guest's data is deleted at logout. The restriction "Allow Shared iPad Temporary Session" turns it off (supervised restrictions list).
- Apps: deploy the apps every user needs to all devices beforehand, to avoid install traffic during use; users cannot delete apps on Shared iPad. Apps marked "Optimised for Shared iPad" in Apple School Manager save their content to iCloud.
- Updates: only the MDM that enrolled the iPad can start iPadOS updates; remove Shared iPad users with the `DeleteUser` command before updating to iPadOS 17.
Practice: load required apps first and look at remaining storage before choosing a user count; pilot in one class before a school-wide rollout.
Gotcha: low-storage iPads cap how many users can be cached.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "Shared iPad overview" and "Prepare Shared iPad" (all sections including the command table), plus the first rows of the enrolment-options table in "Automated Device Enrolment and device management" (searched for the rest) and the "Allow Shared iPad Temporary Session" row of "Device management restrictions for supervised Apple devices" (the restrictions page was read in full, but only that row is used).
- Removed as unconfirmed: the Jamf prestage path, "personal APFS volume per user", and the Verify steps ("login window shows users", "a second user cannot see the first user's data").
- The original source URL (shared-ipad-dep2d0e6e0f2) is not a real page and was replaced; see shared-ipad-sessions-and-quota for the configuration keys.
