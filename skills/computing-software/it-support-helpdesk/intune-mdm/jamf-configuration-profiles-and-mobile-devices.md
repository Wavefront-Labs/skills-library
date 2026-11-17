---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-configuration-profiles-and-mobile-devices
name: jamf-configuration-profiles-and-mobile-devices
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf-configuration-profiles, jamf-mobile-devices, jamf-pro, configuration-profiles, ios-management]
level: practitioner
status: draft
description: "Build and scope Jamf Pro configuration profiles for Macs and iOS, and manage mobile devices in Jamf: enrollment, inventory, smart groups, commands and apps."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_Configuration_Profiles.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Mobile_Device_Configuration_Profiles.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Mobile_Device_Management_Capabilities.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-configuration-profiles-and-mobile-devices

## Configuration profiles
- Computers > Configuration Profiles (or Mobile Devices > Configuration Profiles).
  Each profile has **payloads** (Wi-Fi, Restrictions, FileVault, PPPC, Certificates,
  System Extensions, Login Items, Application & Custom Settings for plist keys).
- **Level**: Computer level vs User level (macOS); most should be computer level.
- **Distribution**: install automatically or make available in Self Service.
- **Scope**: targets (computers, smart/static groups, buildings, departments),
  limitations (LDAP users/groups, network segments), exclusions.
- Custom settings: upload a plist or use the JSON schema for supported apps (e.g. Chrome,
  Microsoft Office) under Application & Custom Settings.
- Profiles are delivered via APNs; check "Management History > Pending/Failed commands"
  on the device record.

## Editing safely
- Editing a scoped profile redistributes to all (choose "Distribute to newly assigned
  only" where offered when changing scope only).
- Two profiles setting the same payload key conflict; macOS behaviour is undefined.
  One payload type per profile is easier to reason about.
- Signed profiles from outside Jamf can be uploaded but not edited.

## Mobile devices in Jamf Pro
- Enrollment: Automated Device Enrollment via PreStage (ABM token), user-initiated
  enrollment URL, or Apple Configurator.
- Inventory: collected on schedule (default daily) plus on demand ("Update Inventory"
  command). Mobile smart groups by model, OS, supervised, app installed, last inventory.
- Commands on the device record: Lock, Clear passcode, Update inventory, Wipe, Enable
  Lost Mode, Restart, Update OS (supervised), Set wallpaper.
- Apps: App Store apps via Volume Purchasing (Apps and Books), in-house apps, managed app
  configuration (XML keys).

## Verify
A test device in scope shows the profile in Settings (or System Settings > Device
Management) and Management History shows the install command Completed.
