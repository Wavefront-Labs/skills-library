---
id: computing-software.general-digital-literacy.file-management.photo-location-and-exif-metadata
name: photo-location-and-exif-metadata
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-media, exif-data, photo-location, metadata-removal]
level: intro
status: draft
description: "See and remove the location, date and camera details stored in photos on iPhone, Android, Windows and Mac before sharing, and know which sites strip it for you."
sources:
  - https://support.apple.com/guide/iphone/adjust-the-date-time-and-location-iph4f78b8f0f/ios
  - https://support.google.com/photos/answer/6153599
  - https://support.microsoft.com/en-us/windows
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Location and EXIF metadata

Photos carry **EXIF** data: date/time, camera, settings and often **GPS coordinates** precise to a house.

## See it
- **iPhone:** open the photo › swipe up or tap ⓘ: map, camera, lens.
- **Android/Google Photos:** open › swipe up › Details.
- **Windows:** right-click › Properties › **Details** (GPS section). **Mac:** Preview › Tools › Show Inspector › ⓘ › GPS tab.

## Remove it before sharing
- **iPhone:** in the Share sheet tap **Options** › turn off *Location* (and *All Photos Data*) for that share. Stop recording it: Settings › Privacy & Security › Location Services › Camera › **Never**.
- **Android:** Google Photos › photo › ⋮ › Edit › remove location; Camera app settings › *Location tags* off. Share via Google Photos with *Remove geographic location* (Settings › Sharing).
- **Windows:** Properties › Details › **Remove Properties and Personal Information** › *Create a copy with all possible properties removed*.
- **Mac:** Photos › Image › Location › **Hide Location**; or export with *Include location information* unticked.

## Who strips it
- Facebook, Instagram, X and WhatsApp remove EXIF from public copies (the platform may still keep it). Email, AirDrop, cloud links, iMessage originals, marketplace uploads and Telegram "as file" keep it.

## Gotchas
- Location also leaks from what's in the picture (house number, school logo, car plate).
- Editing apps may re-add metadata; check the exported copy.

## Verify
- [ ] The shared copy's Properties/Info show no GPS fields.
