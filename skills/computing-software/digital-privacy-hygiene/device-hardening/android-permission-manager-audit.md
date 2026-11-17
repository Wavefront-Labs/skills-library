---
id: computing-software.digital-privacy-hygiene.device-hardening.android-permission-manager-audit
name: android-permission-manager-audit
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, android-permission-manager, app-permissions, android, privacy-dashboard, special-app-access, adb]
level: practitioner
status: draft
description: "Audit an Android phone's app permissions with Permission manager, Privacy dashboard and Special app access, including the dangerous ones (accessibility, notification access)."
sources:
  - "https://ssd.eff.org/module/how-to-get-to-know-android-privacy-and-security-settings"
  - "https://developer.android.com/guide/topics/permissions/overview"
  - "https://support.google.com/android"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android permission manager audit

**Goal:** every app holds only the access its job needs, and nothing holds the powers malware abuses.

## 1. Runtime permissions
Settings > Security & privacy > Privacy > **Permission manager** lists each permission and the apps holding it.
Work through: Location, Camera, Microphone, Contacts, Call logs, SMS, Phone, Nearby devices, Photos and videos,
Files, Physical activity, Body sensors, Notifications.
- Location: prefer **Allow only while using the app**; turn off **Use precise location** for weather, shopping, news.
- Photos (Android 14+): choose **Allow limited access** / selected photos rather than all.
- Turn on **Remove permissions if app is unused** (per app, App info) so old apps lose access automatically.

## 2. Privacy dashboard
Settings > Security & privacy > Privacy > **Privacy dashboard** shows which apps used location, camera and mic in
the last 24 hours (7 days on newer versions). An app using the mic when you never opened it is a red flag.
Quick Settings tiles for **Camera access** and **Microphone access** cut access device-wide; the green dot at top
right shows live use.

## 3. Special app access (the dangerous list)
Settings > Apps > Special app access. Review especially:
- **Accessibility** (Settings > Accessibility > Downloaded apps): can read the screen and tap for you. Banking
  trojans and stalkerware live here; only screen readers, password managers and known tools should appear.
- **Device admin apps**: should be Find My Device and work MDM only.
- **Notification access**: can read every message and 2FA code.
- **Display over other apps**, **Install unknown apps**, **All files access**, **Usage access**, **Modify system settings**.

## 4. From a computer (bulk or stubborn cases)
```bash
adb shell dumpsys package com.example.app | grep -A40 "runtime permissions"
adb shell pm revoke com.example.app android.permission.ACCESS_FINE_LOCATION
adb shell appops get com.example.app
```

## Verify
- [ ] No app has Accessibility, Notification access or Device admin without a reason you can state.
- [ ] Location holders are mostly "while using"; few have precise location.
