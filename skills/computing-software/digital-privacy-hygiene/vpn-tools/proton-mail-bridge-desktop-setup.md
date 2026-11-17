---
id: computing-software.digital-privacy-hygiene.vpn-tools.proton-mail-bridge-desktop-setup
name: proton-mail-bridge-desktop-setup
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, proton-bridge, proton-mail, imap, thunderbird]
level: practitioner
status: draft
description: "Use Proton Mail Bridge to read Proton Mail in Thunderbird, Outlook or Apple Mail over local IMAP/SMTP, with a bridge password and certificate checks."
sources:
  - "https://proton.me/support/protonmail-bridge-install"
  - "https://proton.me/support/protonmail-bridge-clients"
  - "https://proton.me/support/bridge-cli-guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Proton Mail Bridge for desktop clients

**Goal:** use a normal desktop mail client with Proton Mail while keeping end-to-end encryption.

## How it works
Bridge runs locally, talks to Proton's servers with your account, and exposes IMAP and SMTP on `127.0.0.1`.
Messages are decrypted locally; the mail client never talks to Proton directly. Bridge requires a **paid** Proton
plan.

## Setup
1. Install Bridge from proton.me (Windows, macOS, Linux) and sign in (with 2FA).
2. Bridge shows a **mailbox configuration**: IMAP `127.0.0.1:1143`, SMTP `127.0.0.1:1025`, username, and a generated
   **Bridge password**. Use that password in the client, not your Proton password.
3. In Thunderbird add the account manually with those values; STARTTLS on both. Accept Bridge's self-signed
   certificate (or export it from Bridge settings and trust it) so the client still verifies TLS locally.
4. Choose **combined** (all addresses in one mailbox) or **split** address mode in Bridge.

## Headless / Linux CLI
`protonmail-bridge --cli` then `login`, `info` to print credentials. Run as a user service; Bridge needs a keychain
(`pass` or GNOME Keyring) to store its secrets.

## Security notes
- Decrypted mail now sits in your mail client's local cache. Use full-disk encryption and a screen lock.
- Bridge binds to localhost only; do not change it to listen on the network.
- Revoke a Bridge session from Proton web: Settings > Security > Session management.

## Gotchas
- First sync of a large mailbox takes hours; leave Bridge running.
- If the client reports authentication failed after an update, re-copy the Bridge password.
