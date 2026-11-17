---
id: computing-software.general-digital-literacy.digital-communication.sharing-with-qr-codes
name: sharing-with-qr-codes
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, file-sharing, qr-codes, create-qr-code, wifi-qr-code, share-link, page-qr-code, share-wifi-password]
level: intro
status: draft
description: "Create QR codes to share a web page, Wi-Fi password, contact card or file link from Chrome, Edge, phones and free generators, and print them so they scan reliably."
sources:
  - https://support.google.com/chrome
  - https://support.microsoft.com/en-us/microsoft-edge
  - https://support.apple.com/guide/iphone/welcome/ios
  - https://support.google.com/android
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Share with QR codes

**Goal:** people point their camera and get the link, Wi-Fi login or contact, no typing.

## Make one
- **Chrome / Edge (desktop):** click the share/QR icon in the address bar (or right-click page › *Create QR code for this page*) › Download PNG.
- **Android:** Settings › Wi-Fi › gear next to your network › **Share** shows a Wi-Fi QR code. Chrome on Android › Share › QR code.
- **iPhone:** no built-in QR creator for links; use the Shortcuts app action *Generate QR Code* or a trusted generator. Wi-Fi sharing to nearby Apple devices happens automatically when you're in each other's contacts.
- **Contact card:** many generators create vCard QR codes; LinkedIn and WhatsApp offer QR codes for your profile.
- **Files:** upload to OneDrive/Google Drive, set the link permission (view only, anyone with link), then make a QR code of that link.

## Choose a generator carefully
- Prefer **static** codes (the URL is encoded directly; works forever, free).
- "Dynamic" codes from QR services redirect through their servers; free trials often expire and the code stops working, or shows ads.

## Printing well
- At least **2 × 2 cm** (larger for distance: about 1/10 of the scanning distance), dark code on a light background, with a quiet border around it.
- Shorter URLs make simpler, more scannable codes.
- Add a text label of what it opens ("Menu: example.com/menu") so people can check before scanning.
- Test with both iPhone and Android cameras before printing many.

## Safety
- Don't put private links (edit permissions, personal documents) on public QR codes.
- Scammers paste fake QR stickers over real ones (parking meters); check your codes in public places still point to your link.

## Verify
- [ ] Code scans on two different phones and opens the intended page or joins the Wi-Fi.
