---
id: computing-software.digital-privacy-hygiene.privacy-configuration.facebook-off-meta-activity
name: facebook-off-meta-activity
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, off-meta-activity, facebook-privacy, ad-tracking-controls]
level: practitioner
status: draft
description: "Disconnect and clear the activity other apps and websites send to Meta about you, stop future linking, and limit partner data use in ads."
sources:
  - "https://www.facebook.com/help/2207256696182627"
  - "https://www.facebook.com/help/568137493302217"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Facebook off-Meta activity

**Goal:** reduce how much of your web and app activity outside Facebook/Instagram is tied to your Meta account.

## What it is
Businesses send Meta data via the Meta Pixel, SDKs and Conversions API (visits, purchases, app opens). Meta links
it to your account for ads and measurement.

## Controls
Accounts Center > Your information and permissions > **Your activity off Meta technologies**:
1. **Recent activity**: review which businesses sent data.
2. **Clear previous activity**: disconnects past activity from your account.
3. **Manage future activity** > **Disconnect future activity**: stops linking new activity to your account (applies
   to the accounts in this Accounts Center).
4. Disconnect specific businesses individually if you don't want a full disconnect.

## Ad settings
Accounts Center > Ad preferences > Ad settings > **Activity information from ad partners**: set to not use it.

## Reduce collection at the source
- Tracker blocking (uBlock Origin, Brave, Firefox ETP strict) blocks the Meta Pixel on websites.
- On phones, deny App Tracking (iOS ATT) and delete the advertising ID (Android).

## Gotchas
- Disconnecting doesn't stop businesses sending data; Meta still receives it in de-identified form for measurement.
- Logged-in WhatsApp and Messenger are separate settings.
