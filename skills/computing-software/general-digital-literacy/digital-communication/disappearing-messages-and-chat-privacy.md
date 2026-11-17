---
id: computing-software.general-digital-literacy.digital-communication.disappearing-messages-and-chat-privacy
name: disappearing-messages-and-chat-privacy
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, messaging, instant-messaging, disappearing-messages, view-once, chat-lock, end-to-end-encryption, safety-number, whatsapp-privacy, signal]
level: intro
status: docs-checked
description: "Use disappearing messages, view-once media, chat lock and privacy settings in WhatsApp, Signal, iMessage and Telegram, and know their limits (screenshots, backups)."
sources:
  - https://faq.whatsapp.com/673193694148537
  - https://faq.whatsapp.com/1077018839582332
  - https://faq.whatsapp.com/764072925284841
  - https://support.signal.org/hc/en-us/articles/360007320771-Set-and-manage-disappearing-messages
  - https://support.apple.com/guide/iphone/delete-messages-and-attachments-iph2c9c4bfcb/ios
  - https://telegram.org/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disappearing messages and chat privacy settings

**Goal:** control how long messages live and who keeps copies.

## Disappearing messages
- **WhatsApp:** the timer options are 24 hours, 7 days or 90 days (or Off). Set a default for new individual chats at Settings > Privacy > **Default message timer**; groups are set separately and a timer only affects new messages. A message can be *kept*, after which it stays visible to everyone in the chat.
- **Signal:** Settings > Privacy > **Default timer for new chats**, or chat settings > **Disappearing messages** for one chat; choose a time or a custom time of up to 4 weeks. For a sent message the timer starts after sending, for a received one after it is read. In groups, admins can choose who may change the timer.
- **Telegram:** only *Secret Chats* use end-to-end encryption (regular chats are cloud chats); Secret Chats have a self-destruct timer.
- **iMessage:** Settings > Apps > Messages > **Keep Messages** (30 days, 1 year or Forever) deletes older conversations and attachments on that device. Audio messages expire after 2 minutes unless kept (Settings > Apps > Messages > Audio Messages > Expire).

## View once and chat lock (WhatsApp)
- **View once** photos, videos and voice messages disappear after being opened once, must be opened within 14 days, and cannot be forwarded, copied, saved, starred or screenshotted by the recipient. Choose it separately for each item. Unopened view-once media can be restored from a backup; opened media cannot.
- **Chat lock** hides a chat in a locked folder behind extra authentication, without notifying the others. If you forget the secret code, resetting returns locked chats to your list but deletes their messages and media.

## Limits
- Signal states disappearing messages are not for situations where the contact is your adversary: anyone can photograph the screen before the message disappears.
- Disappearing messages are not a reason to send something you'd regret seeing again.

## Verify
- [ ] A test message to yourself or a friend disappears after the timer.

## Checked
Date: 2026-10-27. Documentation: WhatsApp Help Center (disappearing messages, view once, chat lock; via search results), Signal Support (disappearing messages), Apple Support (Messages), Telegram FAQ. Confirmed: timer values and menu paths, 14-day view-once window and restrictions, chat lock reset behaviour, Telegram Secret Chat encryption. Removed unconfirmed claims (Signal 30-second option and view once, WhatsApp privacy-setting list, "no per-chat iMessage timer", backup-persistence remarks).
Method: documentation only; no commands were run.
