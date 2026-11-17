---
id: computing-software.networking-hardware-and-wireless.tailscale.tailnet-dns-name
name: tailnet-dns-name
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailnet-name, rename-tailnet, tailnet-id]
level: practitioner
status: docs-checked
description: "Know the tailnet name types and how to rename or revert the tailnet DNS name."
sources: ["https://tailscale.com/kb/1217"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailnet names

Goal: understand and change your tailnet DNS name.

**Name types.** A machine name identifies a device; the tailnet ID is the string used with the API; the tailnet DNS name is the DNS suffix.

**Default.** New tailnets get `tail<ID>.ts.net`, where `<ID>` is a random hexadecimal string such as `tailnet-fe8c.ts.net`. It enables MagicDNS names and is the fully qualified domain name for HTTPS certificates.

**Rename**

1. Owner, Admin or Network admin only.
2. DNS page of the admin console, then Rename tailnet.
3. Confirm using a randomized name.
4. Pick a generated option, or Re-roll options for more.
5. Select Rename tailnet.

The chosen name becomes active immediately. Existing links to devices that used the default name for MagicDNS, HTTPS certificates or sharing change accordingly.

**Constraints**

- After a randomized name has been used for HTTPS certificates you cannot re-generate it, but you can switch between the randomized and default names.
- To revert: DNS page, Rename tailnet, confirm, choose the name.

**Checklist**

1. Rename before issuing certificates or shares if possible.
2. Update saved links after a rename.
3. Remember only the default and randomized names can be swapped.

## Checked

2026-11-03. Read Tailnet name (kb/1217) and confirmed the `tail<ID>.ts.net` default, randomized-name rename flow and revert rule. Nothing else was removed.

Method: documentation only; no commands were run.
