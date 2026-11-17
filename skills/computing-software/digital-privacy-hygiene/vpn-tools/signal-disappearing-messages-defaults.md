---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-disappearing-messages-defaults
name: signal-disappearing-messages-defaults
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, disappearing-messages, signal, signal-messenger, message-retention, data-minimization, device-seizure, view-once-media]
level: intro
status: docs-checked
description: "Set a default disappearing-message timer in Signal, per-chat timers and view-once media, and know the limits: screenshots, who can change it, backups and notifications."
sources:
  - "https://support.signal.org/hc/en-us/articles/360007320771-Set-and-manage-disappearing-messages"
  - "https://ssd.eff.org/module/how-to-use-signal"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disappearing messages in Signal

**Goal:** reduce what exists on phones if one is lost, seized or compromised later.

## Default timer for new chats
- Android: Settings > Privacy > Disappearing messages > Default timer for new chats; tap Save.
- iPhone: Settings > Privacy > Disappearing messages; tap Set.
- Desktop: Settings (Preferences) > Default timer for new chats; it applies automatically.

## Per chat
Open the chat settings (tap the contact or group name) > Disappearing messages, on any device,
for one-to-one and group chats. Choose a time or a custom time up to 4 weeks. Anyone in the chat
(including any group member) can change the timer. The chat header shows a timer icon and the
thread shows an alert with the new time. Timer changes sync to linked devices. To turn off, pick
Off at the top of the list.

## How the timer behaves
- It applies only to messages after the timer is set or changed.
- Sent message: the timer starts after you send it (not on delivery or read receipt). Received
  message: it starts after you have read it.
- When the timer ends the message is deleted from disk. Rules cover text, files, photos,
  location and GIFs; deleting a reply may behave unexpectedly (EFF).
- Each message shows a countdown icon on its bubble.

## What it does not do
- Signal says it is not for cases where your contact is the adversary: they can photograph the
  screen. EFF adds that contacts can log or screenshot the conversation.
- Push notifications can reveal message text; set Profile > Notifications > Show to hide
  names or content.
- Backups: Signal Secure Backups exclude view-once messages and messages scheduled to disappear
  within the next 24 hours (EFF); to keep a chat out of backups, set it to disappear within 24
  hours or less.

## View-once media
In a chat, select a photo or video and tap the infinity icon above the text box to switch it to
view-once; the recipient can view it once but could still screenshot it.

## Verify
- [ ] Default timer set; a new chat shows the timer icon in its header.

## Checked

Date 2026-11-08. Pages read: Signal Support "Set and manage disappearing messages" and EFF Surveillance Self-Defense "How to use Signal" (disappearing messages, backups and notifications sections). Corrected: the minimum is not a stated 30 seconds; the pages say only up to 4 weeks. Removed as not on the pages: the context-to-timer table, the group-admin restriction, retroactivity wording beyond "new messaging", and the "default 1 week or 4 weeks" examples.

Method: docs-only read of cited pages, 2026-11-08
