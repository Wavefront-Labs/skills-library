---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-setup-pin-and-registration-lock
name: signal-setup-pin-and-registration-lock
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-setup, signal-pin, registration-lock, signal, signal-messenger, secure-messaging, end-to-end-encryption, screen-lock]
level: intro
status: docs-checked
description: "Set a strong Signal PIN, turn on Registration Lock and an app lock, so a SIM swap or a stolen code can't take over your account."
sources:
  - "https://ssd.eff.org/module/how-to-use-signal"
  - "https://signal.org/blog/signal-pins/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signal setup, PIN and Registration Lock

**Goal:** an end-to-end encrypted messenger whose account can't be hijacked by someone who only gets a text message.

## Signal PIN
- Created during setup, after the profile step. It keeps your information safe on Signal's servers: if you switch
  phones you can recover your settings, profile and contacts with it.
- Signal PINs are at least 4 digits but can be longer or alphanumeric. Choose a long, strong PIN or passphrase
  (EFF links its strong-passwords guide for this) and store it in your password manager.
- Signal does not have access to your keys or data, so a forgotten PIN is not recoverable. The apps ask you to
  re-enter it occasionally to help you remember it; these reminders get less frequent over time.

## Registration Lock
On Android, tap your profile picture, then Account; on iPhone, profile picture, then Settings, then Account. Set
the Registration Lock toggle on (create a PIN first if you have not). It stops your phone number being registered
on a different device without the PIN. Write the PIN down: without it you cannot get back into the account for at
least seven days if you change phones.

## Lock the app
If your phone is locked by a fingerprint, face or PIN, you can also lock the Signal app itself, so that after
unlocking the phone you must authenticate again to open Signal or read chats. Find the option in Signal's privacy
settings (names vary by platform).

## Gotchas
- Never share a registration code with anyone.

## Verify
- [ ] Registration Lock on; PIN stored in the vault.
- [ ] Opening Signal requires authentication.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense "How to use Signal" page (PIN, Registration Lock and app-lock sections, via targeted search of the downloaded HTML) and the Signal blog post "Introducing Signal PINs". Dropped as unconfirmed: the 7-day inactivity wording and menu paths for screen lock, screen security and notification previews, the alphanumeric-PIN menu label, the contacts-permission note, and the disappearing-messages cross-reference. support.signal.org could not be read so it was removed from sources.
