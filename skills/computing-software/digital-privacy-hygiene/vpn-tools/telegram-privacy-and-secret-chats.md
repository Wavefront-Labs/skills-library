---
id: computing-software.digital-privacy-hygiene.vpn-tools.telegram-privacy-and-secret-chats
name: telegram-privacy-and-secret-chats
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, telegram-privacy, messenger-comparison, secure-messaging]
level: practitioner
status: docs-checked
description: "Configure Telegram privacy: secret chats for end-to-end encryption, 2-Step Verification, passcode, last-seen and phone-number visibility, usernames."
sources:
  - "https://telegram.org/faq#secret-chats"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telegram privacy and secret chats

**Goal:** if you must use Telegram, know which chats are actually encrypted end to end and lock down what others see.

## Encryption reality
- **Cloud chats** (private and group chats): server-client encryption. Telegram describes secret chats as adding a
  further layer of client-client encryption; cloud chats do not have it.
- **Secret chats**: end-to-end encrypted, so only you and the recipient can read them. They are device-specific and
  not part of the Telegram cloud, so you can only read them on the device where they started, and logging out loses
  them. Messages cannot be forwarded, deletions on your side are ordered on the other side too, and the
  self-destruct timer applies to all messages in them (only to messages sent after the timer is set).
- Start one: open the contact's profile, tap the three dots, then Start Secret Chat.
- To check a secret chat, compare its visualised key with the one in your friend's secret chat settings.
- For sensitive information Telegram itself recommends secret chats in official or verifiable open-source apps,
  preferably with a self-destruct timer, plus 2-Step Verification and a strong app passcode (Settings, Privacy and
  Security).

## 2-Step Verification
Settings, Privacy and Security, 2-Step Verification adds a password on top of the SMS code, with an optional
recovery email, which should itself be protected with a strong password and 2-Step Verification. A passkey can
replace the SMS code entirely.

## Visibility
- People can contact you if they know your phone number or you message them first; whether others can find you by
  number or see it depends on your privacy settings.
- A public username lets people reach you via a t.me link without your number, but it is a public handle; set one
  only if you need it.
- Last seen: if you do not share yours with someone you cannot see theirs; they see only an approximate value
  (recently, within a week, within a month, long time ago). The same rules apply to online status, with brief
  exceptions of about 30 seconds after some actions.

## Checked
Method: docs-checked 2026-11-09 against the Telegram FAQ page (secret chats, encryption, 2-Step Verification, last seen, usernames and t.me sections read from the downloaded HTML). Dropped as unconfirmed: the recommended-values table (Nobody/My Contacts per setting), peer-to-peer call relaying, active-session auto-termination, contact-sync upload, and the claim that groups are never E2EE as worded (kept only the FAQ's cloud-chat description). telegram.org/privacy and the EFF page were removed from sources because they were not read.
