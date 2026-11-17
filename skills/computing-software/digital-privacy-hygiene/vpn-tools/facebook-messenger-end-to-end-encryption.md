---
id: computing-software.digital-privacy-hygiene.vpn-tools.facebook-messenger-end-to-end-encryption
name: facebook-messenger-end-to-end-encryption
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, messenger, end-to-end-encryption, secure-storage, messenger-e2ee]
level: practitioner
status: docs-checked
description: "Know what Messenger's default end-to-end encryption covers, why to set a recovery method for message history, and what Meta can still see when you report."
sources:
  - "https://about.fb.com/news/2023/12/default-end-to-end-encryption-on-messenger/"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Facebook Messenger end-to-end encryption

**Goal:** know when Messenger is end-to-end encrypted and keep your history recoverable without weakening it.

## Status
Meta announced in December 2023 a rollout of default end-to-end encryption for personal messages and calls on
Messenger and Facebook. The rollout was gradual, so confirm in the app that a given chat shows it as encrypted
(menu names change; use the in-app help if you cannot find it).

## Message history
Meta's announcement describes Secure Storage for encrypted message history and a prompt to set a recovery method,
such as a PIN, so messages can be restored after you lose, change or add a device. Pick a recovery method you can
reproduce and store it with your other recovery codes: a lost recovery method on a new device may mean lost history.

## What Meta says it can see
Meta states that nobody, including Meta, can see what is sent or said unless you choose to report a message.
Reporting is therefore a deliberate disclosure: do it only when you want Meta to see that content.

## Disappearing messages
In end-to-end encrypted conversations, Meta describes disappearing messages that last 24 hours, with a notice if
someone screenshots one. Do not treat them as protection from the recipient.

## Gotchas
- The rollout was gradual, so check each chat rather than assuming.
- For metadata-sensitive conversations, compare messengers' own documentation before choosing.

## Checked
2026-11-01. Confirmed against Meta's December 2023 announcement: default encryption rollout for personal messages
and calls, Secure Storage with a recovery method such as a PIN, nobody can see content unless reported, 24-hour
disappearing messages and screenshot notice. Removed as unconfirmed: business and group chat status, menu paths,
verify-keys steps, the logged-in-devices list, link-preview behaviour, the engineering blog URL (not read) and the
Signal comparison.
Method: documentation only; no commands were run.
