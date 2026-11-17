---
id: computing-software.collaboration-platform-administration.zulip.push-notification-privacy-and-e2ee
name: push-notification-privacy-and-e2ee
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [push-e2ee, push-privacy, legacy-push-protocol, libsodium]
level: advanced
status: docs-checked
description: "Explain what the Zulip push notification service, Apple and Google can see: end-to-end encryption in Zulip Server 12.0+, stored metadata, key rotation and limitations."
sources: ["https://zulip.readthedocs.io/en/latest/production/mobile-push-notifications.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Push notification privacy and E2EE

Since Zulip Server 12.0 (April 2026), together with an up-to-date mobile app, notifications are end-to-end encrypted from your server to the device. If either side is older, the legacy protocol is used; organization administrators can require E2EE for message content.

Encryption: the server encrypts each notification with libsodium `crypto_secretbox_easy` (XSalsa20-Poly1305) using a per-device 256-bit key and a fresh 192-bit nonce. Device registration uses `crypto_box_seal`, so the server can forward the device's APNs or FCM token without learning it.

What the push service forwards to Apple or Google: the opaque device token, a `push_key_id` chosen by the app to pick the decryption key, the ciphertext, and delivery priority (higher for new messages, lower for removals). Content, sender, recipient, channel and topic are inside the ciphertext. All links use TLS.

What the service stores while a device is registered: APNs and FCM tokens, basic organization metadata, optional usage statistics and aggregate counts of notifications per server.

Your Zulip server still sees everything and holds the keys, so E2EE does not defend against a compromised server.

Limitations:

- Incomplete forward secrecy: a device key persists until the app rotates it, generally every 30 days; someone holding captured payloads and the current key can decrypt back to the last rotation.
- Metadata side channels: timing, priority and size of notifications are observable.

The forwarding service code is open source in the server project.

## Checked

2026-11-08. Checked: read against the Zulip mobile-push-notifications page (docs/production/mobile-push-notifications.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.
