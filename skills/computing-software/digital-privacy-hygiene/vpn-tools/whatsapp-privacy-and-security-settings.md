---
id: computing-software.digital-privacy-hygiene.vpn-tools.whatsapp-privacy-and-security-settings
name: whatsapp-privacy-and-security-settings
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, whatsapp-privacy, whatsapp, secure-messaging, end-to-end-encryption, two-step-verification, protect-ip-in-calls, group-add-privacy, privacy-checkup]
level: intro
status: docs-checked
description: "Lock down WhatsApp: two-step verification PIN, passkey, who can add you to groups, IP protection in calls, default disappearing timer, app and chat lock."
sources:
  - "https://ssd.eff.org/module/how-to-use-whatsapp"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WhatsApp privacy and security settings

**Goal:** message content is end-to-end encrypted, but account takeover, group invites, call routing and backups
are separate settings. Fix them.

## Account security
- Two-step verification: a six-digit PIN required before you can log into WhatsApp on another phone, with an
  optional recovery email. The app periodically asks for the PIN so you remember it.
- Passkeys are another way to protect the account; follow WhatsApp's own directions to enable one.

## Privacy (Settings, Privacy)
- Go through each option (for example whether people see when you are online, and read receipts) so you share no
  more than you intend. The Privacy Checkup gives more detailed guidance.
- Groups: Settings, Privacy, Groups. Everyone lets anyone, even people not in your address book, add you without
  approval. My Contacts limits that to your contacts; others get a pop-up asking to invite you. My Contacts
  Except lets you exclude chosen contacts.
- Hide your IP from another caller: by default WhatsApp switches between server routing and peer-to-peer calls,
  which can leak your IP address. Settings, Privacy, Advanced, "Protect IP address in calls" forces server routing
  at the cost of call clarity.
- Default message timer: Settings, Privacy, Default message timer sets disappearing-message length for new chats;
  a single chat can override it from the chat's name screen.
- App lock: Settings, Privacy, App Lock (biometric or Face/Touch ID) with a delay before auto-locking. Chat Lock
  moves a chat to a Locked Chats folder and hides message content in notifications.

## Backups
Chat backups are optional and not on by default. If you enable them, also enable the end-to-end encrypted backup
(Settings, Chats, Chat backup) so WhatsApp and Google or Apple cannot read it. You choose a passkey or a password
or key; WhatsApp cannot recover the backup if you lose it, so keep it in a password manager.

## Verify
- [ ] Two-step verification on; group adds restricted to contacts.
- [ ] End-to-end encrypted backup on if backups are used.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense page "How to use WhatsApp" (two-step, groups, backups, app/chat lock, disappearing, IP-in-calls and privacy sections read from the downloaded HTML). Dropped as unconfirmed: Security notifications, Linked devices, Silence unknown callers, Block unknown account messages, 7-day timer suggestion, the metadata-reality paragraph, and the OTP-scam cross-reference. The faq.whatsapp.com sources were removed because they were not read.
