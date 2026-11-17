---
id: computing-software.digital-privacy-hygiene.privacy-configuration.managing-google-maps-timeline
name: managing-google-maps-timeline
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, google-timeline, location-history, google-maps, google, location]
level: intro
status: docs-checked
description: "Control Google Maps Timeline: check it is off, delete saved visits and routes, understand the encrypted backup, and know other Google location data stays."
sources:
  - "https://support.google.com/maps/answer/6258979"
  - "https://support.google.com/accounts/answer/3118687"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing Google Maps Timeline

**Goal:** decide deliberately whether Google keeps a record of the places and routes your devices visit. Sources: the
Google Maps Help article "Manage your Google Maps Timeline" and the Google Account Help article "Manage your Timeline
data".

## What Timeline is
- Timeline saves your visits and routes to a map on each signed-in device. The data shown comes from the device, so
  Timeline is not available for Maps on a computer; use the Google Maps app.
- When it is on, your precise device location is regularly saved to the device, even when Google apps are not in use.
  Google can estimate location from Wi-Fi and mobile network signals, GPS and sensors.
- Optional backup: Maps saves an encrypted copy of your Timeline on Google's servers, which lets you import it onto
  another device.
- Timeline is off by default for your Google Account and can be turned on only if you opt in.

## Turn off
Google Account > the "Timeline" section > switch Timeline off at the top. You can also turn off or delete all of your
Timeline in My Google Activity.

## Delete
- Delete all of it, or only parts. Deleting parts is done in the Google Maps app on your mobile device; you can edit or
  delete visits and routes at any time.
- Timeline data may still be saved on other eligible devices unless you delete all of your data. Turning Timeline off
  does not remove earlier data; delete it manually.
- Data is kept according to your auto-delete settings, or until you delete it.

## What turning it off does not change
- Google says your settings do not change for Google Location Services, Location Sharing or Find Hub.
- If Search Services History or Web & App Activity is on, your account may still save location data (for example the
  general area of your device and its IP address) as part of Search and Maps use, and location can be included in
  photos depending on your camera app settings. Review those settings separately.
- Google is rolling out changes to Search-services settings; if the screens differ from the articles, history for
  Search services is still controlled by Web & App Activity.

## Verify
- [ ] Timeline shows off for the account, and previous Timeline data is deleted on every device you wish.
- [ ] Web & App Activity and Search Services History reviewed.

## Checked
Checked 2026-11-08 against the full text of both cited Google Help articles. The generic Maps Help root, My Activity
and EFF Android guide sources were dropped. Removed what the articles do not state: the rename and migration history,
the 3/18/36-month auto-delete choices, the Chrome-history tick box, Google Photos "Estimate missing locations", Family
Link, Maps location-sharing removal steps, the new-phone re-enable warning and the carrier and Wi-Fi scanning claims.
Method: documentation only; no commands were run.
