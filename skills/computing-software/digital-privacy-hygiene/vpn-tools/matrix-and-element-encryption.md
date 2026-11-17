---
id: computing-software.digital-privacy-hygiene.vpn-tools.matrix-and-element-encryption
name: matrix-and-element-encryption
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, matrix-element, secure-messaging, end-to-end-encryption]
level: practitioner
status: draft
description: "Use Matrix with Element safely: choose a homeserver, set up secure backup and cross-signing, verify sessions, and understand room encryption and metadata."
sources:
  - "https://element.io/help"
  - "https://matrix.org/docs/"
  - "https://www.privacyguides.org/en/real-time-communication/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Matrix and Element encryption

**Goal:** encrypted chats you can still read on a new device, with verified contacts, and realistic expectations
about metadata.

## Homeserver choice
matrix.org (large public), a community server, or self-hosted Synapse/Conduit. The homeserver sees your account,
rooms you're in, who you talk to and when, and device lists. It doesn't see E2EE message content.

## Set up encryption properly
1. Element > Settings > Security & Privacy > **Set up Secure Backup**. Save the **Security Key** (recovery key) in
   your password manager, or set a Security Phrase.
2. Cross-signing: verifying a new login with an existing one (emoji comparison or QR) makes all your sessions
   trusted to others.
3. Verify contacts: open their profile > Verify > compare emoji in person or on a call.

## Rooms
- DMs and private rooms are E2EE by default; encryption can't be turned off once enabled.
- Public rooms are usually unencrypted (anyone can join and read).
- Room settings > Security: who can join, history visibility.

## Hygiene
- Settings > Sessions: sign out unknown/old sessions.
- Losing all sessions **and** the Security Key = old encrypted history unreadable.

## Gotchas
- Bridges to WhatsApp/Telegram/SMS decrypt on the bridge server; those chats aren't E2EE end to end.
- Display names and avatars in rooms are not encrypted.
