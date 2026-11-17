---
id: computing-software.digital-privacy-hygiene.vpn-tools.choosing-a-messenger-by-metadata-exposure
name: choosing-a-messenger-by-metadata-exposure
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, messenger-comparison, sms-unencrypted, secure-messaging, end-to-end-encryption, signal, whatsapp, imessage, telegram, metadata, simplex]
level: intro
status: docs-checked
description: "Compare SMS, iMessage, WhatsApp, Telegram, Signal and SimpleX on encryption defaults and metadata, and choose per conversation instead of per habit."
sources:
  - "https://ssd.eff.org/module/communicating-others"
  - "https://ssd.eff.org/module/why-metadata-matters"
  - "https://www.privacyguides.org/en/real-time-communication/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a messenger by metadata exposure

**Goal:** end-to-end encryption protects message content, but not the fact that you are communicating. Metadata
(who, when, location on a cell call) can reveal a lot, so compare defaults and metadata, not just encryption.

## Why metadata matters (EFF)
End-to-end encryption protects only the content, not who you talk to and when. EFF describes communication
metadata as everything except the content, like the envelope of a letter, and notes that in some countries,
including the US, metadata has historically had less legal protection than content.

## Comparison (check each app's current state)
| Messenger | End-to-end encrypted? | Notes from the sources |
|---|---|---|
| SMS / phone calls | No: SMS is not encrypted at all | Anyone with power over the phone company can read texts or record calls (EFF) |
| iMessage | Only when everyone in the chat uses Apple devices | EFF |
| WhatsApp | Yes, E2EE texting and calls | Owned by Meta (EFF) |
| Telegram | Only if you deliberately turn it on | EFF |
| Signal | Yes, using the Signal protocol | Sealed Sender encrypts the sender address so the server sees only the recipient; Signal needs a phone number to register, but you can set a username and hide your number from contacts (Privacy Guides) |
| SimpleX Chat | Yes | No unique identifiers such as phone numbers or usernames; uses unidirectional queues to protect metadata (Privacy Guides) |

EFF also says services that are not open source, or do not use established protocols like the Signal protocol and
get little attention from researchers, carry some risk.

## Choosing
- Sensitive or metadata-sensitive conversations: Signal, or SimpleX if you want no phone number.
- Family who won't move: WhatsApp is E2EE by default; review its privacy settings.
- Avoid SMS for codes, addresses, health or finances when an alternative exists.

## Verify
- [ ] Sensitive contacts are reachable on an end-to-end encrypted app.
- [ ] If you use Telegram, you have deliberately turned on end-to-end encryption for chats that need it.

## Checked
2026-11-01. Confirmed on EFF SSD "Communicating with Others" and "Why Metadata Matters" and on Privacy Guides
"Real-Time Communication": rows above and the Signal and SimpleX details. Removed: RCS and MLS, carrier lawful
intercept and SS7 claims, iMessage SMS fallback, WhatsApp backup E2EE and metadata list, Signal subpoena-response
detail, Session and Briar, the CISA advice (PDF blocked), the iOS setting path.
Method: documentation only; no commands were run.
