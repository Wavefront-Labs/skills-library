---
id: computing-software.general-digital-literacy.digital-communication.airdrop-and-quick-share
name: airdrop-and-quick-share
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, file-sharing, airdrop, quick-share, nearby-share, share-nearby]
level: intro
status: docs-checked
description: "Send photos and files to nearby devices with AirDrop on Apple devices and Quick Share on Android and Windows, set who can find you, and avoid unsolicited AirDrops."
sources:
  - https://support.apple.com/en-us/119857
  - https://support.google.com/android/answer/9286773
  - https://www.android.com/quick-share/with-windows-pc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AirDrop and Quick Share

**Goal:** send a video or document to someone in the same room in seconds, without email or a cable.

## AirDrop (iPhone, iPad, Mac)
1. Both devices: Wi-Fi and Bluetooth on, devices close together; turn Personal Hotspot off on either device first.
2. **Receiving:** Control Centre, touch and hold the connectivity controls, tap **AirDrop**, then choose **Contacts Only** or **Everyone for 10 Minutes**. After 10 minutes the setting returns to Contacts Only if you are signed in to your Apple Account (iOS 16.2 and later), otherwise to Receiving Off.
3. **Sending:** Share button, then **AirDrop**, then the person or device. The recipient accepts.

## Quick Share (Android, Chromebooks, Windows)
1. Android: open **Share > Quick Share**, or the Quick Share tile in Quick Settings, or Settings and search "Quick Share". The receiver must be in Receive mode (the Quick Share page) with an unlocked screen.
2. Visibility (Settings > Quick Share > **Who can share with you**): *Your devices*, *Contacts*, or *Everyone for 10 minutes* (it switches back after 10 minutes).
3. The receiver taps **Accept**. Received files appear in the Files app under Downloads > Quick Share.
4. Windows PCs use the **Quick Share for Windows** app from Google (select PCs only).

## Between iPhone and Android
- Quick Share on Pixel 8a or later, and some Samsung, Oppo, OnePlus, Vivo, Xiaomi, Honor, Transsion and Motorola phones, can send to an iPhone, iPad or Mac whose AirDrop is set to **Everyone for 10 minutes**. Receiving from Apple devices needs a Pixel 9 or later (not the 9a) or a listed brand.
- On other devices, Quick Share can show a **QR code**: the iPhone scans it and downloads the files from a Google link; files are end-to-end encrypted, available for 24 hours, limited to 10 GB per 24 hours, 1,000 files per session and 20 receivers.

## Safety
- Leave AirDrop on **Contacts Only** and Quick Share on **Your devices** or **Contacts** except when you need Everyone.
- Check the sender's name before you accept, and decline anything you did not expect.

## Verify
- [ ] Test transfer works; receiving visibility back to Contacts Only / Your devices afterwards.

## Checked
Date: 2026-10-27. Documentation: Apple Support "How to use AirDrop on your iPhone or iPad", Google "Use Quick Share on your Android device" and android.com Quick Share for Windows page. Confirmed: AirDrop options and 10-minute revert, Wi-Fi/Bluetooth/Hotspot requirement, Quick Share visibility names and menu, receive folder, AirDrop interop device lists, QR-code limits. Removed unconfirmed claims (NameDrop, file destinations on Apple devices, Samsung app, legal remarks).
Method: documentation only; no commands were run.
