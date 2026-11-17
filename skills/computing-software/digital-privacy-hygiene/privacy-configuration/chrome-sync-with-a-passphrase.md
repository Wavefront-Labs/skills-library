---
id: computing-software.digital-privacy-hygiene.privacy-configuration.chrome-sync-with-a-passphrase
name: chrome-sync-with-a-passphrase
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, chrome-sync-passphrase, chrome, encryption, google-account]
level: practitioner
status: docs-checked
description: "Encrypt Chrome synced data with your own passphrase so Google cannot read it, know which features it disables, and how changing or removing it deletes server data."
sources:
  - "https://support.google.com/chrome/answer/165139"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chrome sync with a passphrase

**Goal:** browser data syncs between devices while Google's servers hold data it cannot read. Source: Google's Chrome
Help page "Get your bookmarks, passwords, and more on all your devices". Menu names change with Chrome versions.

## What it does
Signed in to Chrome, you can sync bookmarks, reading list, passwords, payment info, identity and contact info,
extensions, web apps, settings, and (if you turn on History and tabs) tabs and history. Synced data is always
protected by encryption; a passphrase additionally lets you use Google's cloud without Google being able to read it.
Payment methods and addresses from Google Wallet are not encrypted by a passphrase.

## Set it up (computer)
1. Sign in to Chrome with your Google Account.
2. More > Settings > **You and Google** > select your account name.
3. At the bottom, **Encryption options** > **Use your own passphrase to encrypt all the Chrome data in your Google
   Account** > enter and confirm the passphrase > Save.
Store the passphrase in a password manager.

## Trade-offs while a passphrase is set
- You need it to sign in to Chrome on a new device and on devices already signed in.
- Your feed shows no suggestions based on sites you browse in Chrome.
- You cannot check saved passwords on passwords.google.com or use Smart Lock for Passwords.
- Not all history syncs: only web addresses typed into the address bar, so other devices' sites appear in History only
  if you typed them.

## Change, forget or remove the passphrase
Changing it deletes the data it encrypted from Google's servers and signs you out of all your devices; your passwords
and other info are deleted from the Google Account and from the device. Before resetting, export your passwords and
import them again afterwards (Chrome password import and export).
1. Remove it: open **Chrome data** in your Google Account dashboard > at the bottom, Delete data > Delete. You can then
   resume saving data, without a passphrase.
2. Optionally set a new passphrase with the steps above.
If sync fails with a passphrase, Google suggests updating Chrome to the latest version.

## Related
- Chrome history saved to your account that is also added to Web & App Activity can personalise other Google products;
  Google says a passphrase lets you store Chrome data without Google reading your history.

## Checked
Checked 2026-11-08 against the full text of Google's Chrome Help page 165139. Removed what it does not state: the
Sync and Google services menu route, the Google Pay wording (the page says Google Wallet), the chrome.google.com/sync
reset link (a redirect to an unsupported page), the device-data-retained claim, and the Firefox and Brave Sync
comparison. The support.google.com/chrome landing page is a stub and was dropped.
Method: documentation only; no commands were run.
