---
id: computing-software.general-digital-literacy.internet-navigation.reviewing-phone-app-permissions
name: reviewing-phone-app-permissions
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, online-privacy, app-permissions, location-permission, privacy-dashboard, app-privacy-report, permission-manager, tracking-transparency]
level: intro
status: docs-checked
description: "Review and limit what phone apps can access (location, camera, microphone, contacts, photos, tracking) using iPhone and Android privacy settings and dashboards."
sources:
  - https://support.apple.com/guide/iphone/iph251e92810/ios
  - https://support.apple.com/guide/iphone/control-the-location-information-you-share-iph3dd5f9be/ios
  - https://support.google.com/android/answer/9431959
  - https://support.google.com/android/answer/13530434
  - https://support.google.com/android/answer/13627979
  - https://ico.org.uk/for-the-public/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing phone app permissions

**Goal:** apps get only the access they need, only when they need it.

## iPhone
- Settings › **Privacy & Security** › Location Services, or a category such as Contacts, Calendars, Reminders or Motion & Fitness: each lists the apps that asked for access, and you can switch each on or off.
- Location: Settings › Privacy & Security › Location Services › tap the app. Choose While Using the App or Ask Next Time rather than Always; turn off *Precise Location* to share only your approximate location with apps that do not need your exact one.
- **Tracking:** Settings › Privacy & Security › Tracking › turn off *Allow Apps to Request to Track*.
- **App Privacy Report** (Settings › Privacy & Security › App Privacy Report) shows how apps use the permissions you granted and their network activity; it can be turned off, which deletes its data.

## Android
- Settings › Security & Privacy › **Privacy** › **Permission manager** (pick a permission to see its apps) or **Privacy dashboard** (app activity for the last 7 days on Android 13 and up, 24 hours on Android 12; some steps need Android 12 or 13+).
- For location, camera and microphone you may get *Allow only while using the app*, *Ask every time* or *Don't allow*; *All the time* is for location only.
- Android revokes permissions of apps unused for a long time: review under Apps › Unused apps; per app, App Info › Unused apps › *Pause app activity if unused* controls the exclusion. Menus vary by device and Android version.

## Rules of thumb
A torch app wanting contacts or a game wanting your microphone is a red flag: deny or uninstall.
Messaging apps reasonably need contacts and mic; maps need location while using.

## Verify
- [ ] No app has "Always" location unless you deliberately allowed it; unused apps are removed.

## Checked

Checked 2026-10-27 against Apple iPhone User Guide (control access to information in apps; control location information you share), Android Help (change app permissions 9431959, privacy dashboard 13530434, unused apps 13627979). Confirmed: Settings > Privacy & Security paths, While Using, Ask Next Time, Precise Location, App Privacy Report, Android Permission manager and Privacy dashboard windows, Unused apps setting.

Method: documentation only; no commands were run.
