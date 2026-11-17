---
id: computing-software.general-digital-literacy.digital-communication.sending-photos-and-videos-in-full-quality
name: sending-photos-and-videos-in-full-quality
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, dc-messaging, send-hd-photos, media-quality, file-sharing]
level: intro
status: docs-checked
description: "Send photos and videos without heavy compression: WhatsApp HD and document mode, iMessage and RCS settings, AirDrop or Quick Share, and cloud links for originals."
sources:
  - https://faq.whatsapp.com/164676891531296
  - https://telegram.org/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Send photos and videos in full quality

## Why quality drops
- Messaging apps compress images and videos to save data, and standard picture messaging (MMS) is limited to small sizes.

## WhatsApp
- Before sending, switch the photo from Standard to **HD** in the HD Media menu (then Done, then Send). HD images are sharper but use more data and take longer to upload. HD is not available for status updates or profile pictures.
- Documents sent through the document picker can be up to 2 GB (older help pages mention 100 MB; the current help pages list 2 GB). Whether a photo sent as a document keeps full resolution is not stated in the help pages, so test it with the recipient.
- Photos, videos and voice messages sent as media have a much smaller size limit than documents.

## Other apps
- Telegram supports files of up to 2 GB each; check the app for a send-as-file option.
- For other apps (iMessage, Google Messages, Signal), look in the app's own settings and help for a media-quality option; labels differ between versions.

## Better for many or big files
- AirDrop (Apple) and Quick Share (Android and Windows) send directly between nearby devices (see the AirDrop and Quick Share skill).
- Shared albums or a cloud link (Google Drive, OneDrive, iCloud) for whole events.

## Privacy
- Original photos can carry location data. Remove it, or share a link with restricted access, before sending to people outside your close circle.

## Verify
- [ ] The recipient confirms the file size or resolution matches the original.

## Checked
Date: 2026-10-27. Documentation: WhatsApp Help Center (sending media, via search results), Telegram FAQ. Confirmed: WhatsApp HD Media option and limits, 2 GB document limit, Telegram 2 GB files. Removed unconfirmed claims (WhatsApp storage menu path, iMessage Low Quality Image Mode, RCS behaviour, Signal media-quality path, document-mode metadata claims).
Method: documentation only; no commands were run.
