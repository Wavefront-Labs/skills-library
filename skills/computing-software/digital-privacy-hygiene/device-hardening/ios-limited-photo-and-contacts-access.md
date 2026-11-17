---
id: computing-software.digital-privacy-hygiene.device-hardening.ios-limited-photo-and-contacts-access
name: ios-limited-photo-and-contacts-access
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, limited-photo-access, app-permissions, app-privacy-report]
level: practitioner
status: draft
description: "Give iPhone and Android apps only selected photos and contacts with limited access, use the system photo picker, and audit full-access grants."
sources:
  - "https://support.apple.com/guide/iphone/control-access-to-information-in-apps-iph251e92810/ios"
  - "https://developer.android.com/about/versions/14/changes/partial-photo-video-access"
  - "https://support.apple.com/guide/personal-safety/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Limited photo and contacts access

**Goal:** an app that wants one photo or one contact doesn't get your whole library or address book.

## iPhone
- Settings > Privacy & Security > **Photos** > app: None, **Limited Access** (pick specific photos), Add Photos Only,
  Full Access. Limited apps get only selected items; change selection via "Edit Selected Photos".
- Settings > Privacy & Security > **Contacts** (iOS 18+): Limited Access lets you choose individual contacts.
- Many apps use the system **photo picker** (no permission needed; they only get what you pick).

## Android 14+
- When an app asks for photos/videos: "Select photos and videos" (partial), "Allow all", or "Don't allow".
- Settings > Apps > [app] > Permissions > Photos and videos: change later.
- System photo picker on Android 13+ gives selected items without permission.

## Audit
1. iOS: Settings > Privacy & Security > Photos and Contacts: review apps with Full Access.
2. Android: Settings > Security & privacy > Privacy > Permission manager > Photos and videos / Contacts.
3. Downgrade to Limited for chat, social and shopping apps.

## Location data in photos
Even limited sharing passes EXIF location unless removed; iOS share sheet > Options > Location off.

## Gotchas
- Messaging apps that upload your full contacts for "find friends" only need limited access if you add people
  manually.
- Social apps may nag repeatedly for full access; declining is fine.
