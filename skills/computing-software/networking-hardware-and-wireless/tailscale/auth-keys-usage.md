---
id: computing-software.networking-hardware-and-wireless.tailscale.auth-keys-usage
name: auth-keys-usage
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [auth-keys, reusable-keys, tskey]
level: practitioner
status: docs-checked
description: "Generate one-off or reusable auth keys and register nodes non-interactively."
sources: ["https://tailscale.com/kb/1085"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auth keys

Goal: add a device without interactive login.

**Key types**

- One-off: usable once.
- Reusable: usable for many devices; dangerous if stolen, so keep in a key vault.

**Expiry.** Choose 1 to 90 days. An expired key does not remove devices it already authorized; they stay until their node key expires.

**Generate.** Owner, Admin, IT admin or Network admin: Keys page, Generate auth key, then set description, reusable, expiry and device settings:

- Ephemeral: remove the device after it goes offline.
- Pre-approved: auto-authorize when device approval is enabled.
- Tags: tag devices that use the key.

**Register**
```
sudo tailscale up --auth-key=tskey-abcdef1432341818
```
Keys are case-sensitive.

**Identity.** A device registered with an untagged key takes the identity of the user who generated it. With tags, after login the device assumes the key's tags. Key expiry for tagged devices is off by default and does not change when you edit tags unless you re-authenticate.

Revoked and expired keys are listed on the Keys page. To create keys programmatically, use an OAuth client with the API.

**Checklist**

1. Prefer tagged, short-lived keys.
2. Store reusable keys in a vault.
3. Check Keys page for revoked ones.

## Checked

2026-11-03. Read Auth keys (kb/1085) and confirmed one-off and reusable keys, 1 to 90 day expiry, key options and tagged-key identity. Nothing else was removed.

Method: documentation only; no commands were run.
