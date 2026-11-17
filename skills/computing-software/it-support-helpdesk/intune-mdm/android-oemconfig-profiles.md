---
id: computing-software.it-support-helpdesk.intune-mdm.android-oemconfig-profiles
name: android-oemconfig-profiles
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, oemconfig, samsung-knox-service-plugin, zebra-oemconfig, managed-configuration, android-enterprise, android-enrollment]
level: advanced
status: docs-checked
description: "Configure OEM-specific Android settings with OEMConfig in Intune: add the OEM app, designer vs JSON editor, conflicts between profiles, the 500 KB limit and status checks."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/android-oem-configuration-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# android-oemconfig-profiles

OEMConfig is a Google-defined standard: the device maker ships an app containing a schema of
its own settings, Intune reads the schema and shows it in the admin center, and the OEMConfig
app on the device applies the settings (not an Intune agent). OEMConfig profiles are a type
of device configuration policy similar to app configuration. It needs Android Enterprise devices
enrolled in Intune MDM, and only works with devices that support it and have a matching OEM
app. A Sony app on a Zebra device does nothing.

## Setup
1. Get the OEM's app from managed Google Play and add it to Intune, then assign it to the
   devices. Some OEMs preinstall it. Check the supported-apps table on the Intune page; for
   example Samsung is `com.samsung.android.knox.kpu` (Knox Service Plugin), and Zebra has
   `com.zebra.oemconfig.release` (OEMConfig Powered by MX, Android 11 and newer) and
   `com.zebra.oemconfig.common` (Legacy, Android 11 and earlier).
2. Devices > Manage devices > Configuration > Create > New policy > Platform **Android
   Enterprise** > Profile type **OEMConfig**.
3. Basics: pick the associated OEMConfig app. If an app you synced is not listed, Intune may
   need to onboard it.
4. Configure settings with the **Configuration designer** or the **JSON editor**. The editor
   gives a full template; you can download it, edit elsewhere and paste back, and use it to back
   up a configuration. The two views stay in sync, and invalid input blocks switching. An
   empty bundle in the designer is deleted when you switch to JSON. Selecting **Clear**
   removes a setting from the profile, so the device value is left unchanged.
5. Assign. Required RBAC: Mobile apps, Device Configurations, and Android Enterprise > Read.

## Rules that bite
- One profile per device: the OEMConfig model supports a single policy per device on non-Zebra
  devices, and several profiles give inconsistent behaviour. More precisely, each top-level
  parent group or bundle (for example Wi-Fi) can be in only one profile; two profiles with the
  same bundle both go to **Conflict** and neither deploys. Zebra devices can take several
  profiles using the Legacy Zebra OEMConfig app.
- Maximum profile size is 500 KB; larger profiles are not deployed (the console reports
  "Profile is larger than 500KB"). Reduce settings or values.
- Intune does not validate the schema or values. It saves what you enter (for example text in
  a port field), so follow the OEM documentation.
- Intune always syncs the latest OEM app version and keeps no older schema. Version conflicts
  are for the OEM to resolve.

## Status and troubleshooting
- Devices > Manage devices > Configuration > the profile: Overview, Properties, Device status,
  User status.
- Per-setting status: Devices > All devices > the device > App configuration > the OEMConfig
  profile > a setting. Zebra devices show one row covering all settings.
- Settings that behave wrongly inside the app are for the OEM app's developer, not Intune.
- Check the app is installed on the device (assignment) and that you chose the correct
  OEM app for that hardware.

## Checked
Date: 2026-11-08. Read in full: Intune "Use and manage Android Enterprise devices with OEMConfig" (updated 2026-09-15). The Samsung Knox and Zebra source URLs were 404 or empty and were dropped. Removed as unconfirmed: Knox licence requirements, E-FOTA licensing, device-wide vs work profile Knox sections, on-device app logs and StageNow/MX log claims, the "Not applicable settings after app update" claim, and "firmware" cause for not applied.
Method: documentation only; no commands were run.
