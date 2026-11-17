---
id: computing-software.general-digital-literacy.web-browsers.syncing-browser-data-across-devices
name: syncing-browser-data-across-devices
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-profiles-sync, sync-across-devices, browser-sync, sync-passwords, sync-bookmarks, sync-passphrase]
level: intro
status: docs-checked
description: "Turn on sync in Chrome and Edge to share bookmarks, passwords, tabs and history across devices, choose what syncs, and protect Chrome data with a passphrase."
sources:
  - https://support.google.com/chrome/answer/165139
  - https://support.google.com/chrome/answer/185277
  - https://support.google.com/chrome/answer/9175737
  - https://support.microsoft.com/en-us/edge/sign-in-to-sync-microsoft-edge-across-devices
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sync bookmarks and passwords across devices

**Goal:** a bookmark or password saved on the laptop is on the phone too.

## Chrome
- Sign in: profile icon > Sign in to Chrome with a Google Account. Signed in, your info is saved in the Google Account and available on every device signed in with it: bookmarks, reading list, passwords, payment info, identity and contact info, extensions, web apps, and settings.
- Tabs and history: More > Settings > You and Google > your account name > turn on **History and tabs**. The same page lets you choose what is saved in your Google Account.
- Existing local info: profile icon > **Save x items in Account**.
- **Passphrase (optional):** More > Settings > You and Google > your account name > Encryption options > Use your own passphrase. Google cannot read passphrase-encrypted Chrome data. Costs: you need it to sign in on new devices, only addresses typed in the address bar sync as history, and passwords cannot be checked at passwords.google.com. Changing or removing it deletes the data it encrypted from Google's servers and signs you out everywhere; export passwords first.
- Sync stopped or paused: select **Verify it's you** > Sign in again. If sync turns off every time Chrome closes, More > Settings > Privacy and security > Site settings > Additional content settings > On-device site data > turn on "Allow sites to save data on your device".

## Edge
Settings > Profiles > Sign in, choose the account, Sign in to sync data. Manage items at Settings > Profiles > Sync (toggles per data type). Microsoft lists favourites, passwords, history, extensions, settings, open tabs, autofill entries and payment info as syncable on computers.

## Gotchas
- Sync mirrors changes: deleting data while signed in and syncing removes it from all synced devices (Microsoft says this for Edge). Export bookmarks occasionally.
- Whoever gets the account gets the synced passwords: use a strong password and 2-step verification.
- Do not sign in on a shared or public computer.

## Verify
- [ ] Add a test bookmark on one device; it appears on the other.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Get your bookmarks, passwords, and more on all your devices", "Sign in to Chrome", "Fix issues with sync in Chrome"; Microsoft Support "Sign in to sync Microsoft Edge across devices", read in October 2026. Confirmed: the data types, menu paths, passphrase effects, resume and keep-sync-on steps, Edge Profiles > Sync path and deletion warning. Removed as unconfirmed: Firefox and Safari steps, "Send to your devices" and the sync timing claims.
Method: documentation only; no commands were run.
