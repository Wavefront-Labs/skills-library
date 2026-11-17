---
id: computing-software.general-digital-literacy.basic-troubleshooting.chromebook-setup-and-powerwash
name: chromebook-setup-and-powerwash
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-device-lifecycle, chromebook, powerwash, chromeos]
level: intro
status: draft
description: "Set up a Chromebook with a Google account, sync settings and apps, check its update expiry, and Powerwash (factory reset) it to fix problems or before passing it on."
sources:
  - https://support.google.com/chromebook/answer/183084
  - https://support.google.com/chromebook
  - https://support.google.com/chrome/a/answer/6220366
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Chromebook setup and Powerwash

## First setup
1. Power on, choose language and Wi-Fi, accept terms.
2. Sign in with a **Google account** (the first account becomes the **owner**). Child accounts use Family Link.
3. Choose sync options: apps, settings, Wi-Fi, wallpaper sync from previous Chromebooks; Android phone link (Phone Hub, Smart Lock).
4. Updates install automatically; restart when the update icon appears.
- Check **Auto Update Expiration**: Settings > About ChromeOS > *Additional details > Update schedule*.

## Everyday basics
- Files live in **My files** (local Downloads) and **Google Drive** (cloud). Back up Downloads, which Powerwash erases.
- Launcher key (Everything button) opens apps and search; Play Store gives Android apps; Linux is optional under Settings > About > Developers.

## Powerwash (factory reset)
- When: persistent crashes, owner change, selling or giving away.
- Back up Downloads/My files to Drive or USB.
- Settings > System preferences > **Reset settings > Powerwash > Reset**, or at sign-in press **Ctrl+Alt+Shift+R**.
- After Powerwash, the first account to sign in becomes the new owner.
- Enterprise/school-enrolled Chromebooks re-enrol automatically; only the admin can release them.

## Recovery
- If ChromeOS is missing or damaged: Esc+Refresh+Power, then recover using the *Chromebook Recovery Utility* USB from another computer, or network recovery on newer models.

## Verify
- [ ] After setup or reset, sign-in works, updates are current, and no old files remain when handing it on.
