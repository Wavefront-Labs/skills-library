---
id: computing-software.messaging-and-integration.ntfy.android-intents
name: android-intents
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, android, intents, tasker, macrodroid]
level: advanced
status: docs-checked
description: "Automate with the ntfy Android app via broadcast intents for receiving and sending messages (Tasker, MacroDroid)."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/phone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android intents

## Receiving

Listen for the broadcast action `io.heckel.ntfy.MESSAGE_RECEIVED`. Extras include `topic`, `message`, `title`, `priority`, `tags`, `attachment_url`.

- In MacroDroid, enter the package name `io.heckel.ntfy` exactly or intents may be silently dropped.
- Mute automation topics so they do not pop up.

## Sending

Broadcast the action `io.heckel.ntfy.SEND_MESSAGE`.

- Required extras: `topic`, `message`.
- Optional extras: `base_url` (defaults to `https://ntfy.sh`), `title`, `tags`, `priority`.

In Tasker the HTTP Request action works without the app installed, as an alternative to intents.

## Gotchas

- Without `base_url`, sends go to ntfy.sh, not your self-hosted server.

## Checked

2026-11-04. Confirmed against the ntfy phone page (Automation apps): receive and send actions, extras, required and optional extras, `base_url` default, MacroDroid package-name note, muting, Tasker HTTP Request note. Removed: a subscription requirement and the Verify step, not on the page.
Method: documentation only; no commands were run.
