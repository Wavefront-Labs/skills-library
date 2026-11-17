---
id: computing-software.digital-privacy-hygiene.device-hardening.android-private-space
name: android-private-space
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, android-private-space, android, secure-folder, app-permissions, shared-device]
level: intro
status: draft
description: "Set up Android 15+ Private space (or Samsung Secure Folder) to keep sensitive apps locked, hidden and paused, and understand what it does not protect against."
sources:
  - "https://developer.android.com/about/versions/15/features"
  - "https://source.android.com/docs/security/features"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android Private space

**Goal:** keep dating, health, banking or work apps out of sight on a phone others sometimes use, with a
separate lock.

## Set up (Android 15+, Pixel wording)
1. Settings > Security & privacy > **Private space** > Set up.
2. Choose a Google account: a separate account keeps Play history, contacts and photos for the space apart from
   the main profile.
3. Set a separate lock (different PIN or pattern from the main screen lock is the point).
4. Optional: **Hide private space when it's locked** so it vanishes from the app drawer; open it by searching
   "private space" in the launcher.
5. Install apps into it from the Play Store inside the space (or clone an installed app).

## Behaviour
- It is a separate user profile with its own encryption keys; when locked, its apps are stopped: no
  notifications, no background sync, no location use.
- Auto-lock can be set to lock every time the device locks.
- Files and photos inside are visible only to space apps; share out deliberately.

## Samsung equivalent
**Secure Folder** (Settings > Security and privacy > More security settings > Secure Folder), Knox-backed, with
its own lock and option to hide the icon.

## Limits
- Not a defense against someone who knows the space PIN, or forensic extraction of an unlocked phone.
- Device admin/stalkerware with Accessibility in the main profile can still observe screen content while the
  space is open.
- Check backup: data inside may not be in the main Google backup; deleting the space deletes its data.

## Verify
- [ ] Space lock differs from the main lock; apps inside stop notifying when locked.
