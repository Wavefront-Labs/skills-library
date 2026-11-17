---
id: computing-software.it-support-helpdesk.apple-device-management.managed-app-configuration
name: managed-app-configuration
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, vpp-apps, managed-app-configuration, managed-app-config, appconfig]
level: practitioner
status: draft
description: "Push AppConfig dictionaries, managed open-in and removal-on-unenrol to managed apps using the app's configuration keys."
sources:
  - "https://support.apple.com/guide/apple-business-manager/welcome/web"
  - "https://support.apple.com/guide/deployment/distribute-apps-and-books-dep9b8c8a9b7/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# managed-app-configuration

Goal: pre-configure apps and protect their data.
- Apps publish their keys (AppConfig Community); put the dictionary in the app configuration field of the MDM.
- Use variables such as `$EMAIL` or `%SerialNumber%` (MDM-specific syntax; confirm).
- InstallApplication option `ChangeManagementState=Managed` makes the app managed; set `RemoveOnUnenroll`.
- Combine with open-in restrictions to keep data inside managed apps.
- Test config keys before wide deployment.
Practice: Store configuration dictionaries in version control, compare against the vendor documentation after app updates, and test on both supervised and user-enrolled devices.
Gotcha: apps already installed by the user are not managed unless the MDM takes ownership, which prompts the user on supervised and unsupervised devices differently.
Verify:
- App launches pre-signed in.
- `com.apple.configuration.managed` key is visible in app diagnostics.
