---
id: computing-software.networking-hardware-and-wireless.tailscale.policy-file-sections
name: policy-file-sections
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailnet-policy-file, tagowners, autoapprovers]
level: advanced
status: docs-checked
description: "Know every top-level section of the policy file and what each controls."
sources: ["https://tailscale.com/kb/1337"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailnet policy file sections

Goal: know which top-level key does what.

| Key | Purpose |
|---|---|
| `grants` | Network and application access control (preferred) |
| `acls` | Network-level access rules (legacy but supported) |
| `ssh` | Who can use Tailscale SSH |
| `autoApprovers` | Who can advertise subnet routers, exit nodes and app connectors without approval |
| `nodeAttrs` | Attributes applied to devices and users |
| `postures` | Device posture rules referenced by policies |
| `tagOwners` | Who may assign which tags |
| `groups` | Named groups of users, devices and subnets |
| `hosts` | Named aliases for devices and subnets |
| `ipsets` | Named network segments |
| `tests` | Assertions about access policies that must not change |
| `sshTests` | Assertions about Tailscale SSH |

**Notes**

- Access is deny by default; rules only add permission.
- Grants and ACLs can coexist in one file. Tailscale recommends grants for new configuration, and says ACLs will keep working indefinitely.
- Tailscale translates ACLs into low-level rules from source IP to destination IP and port.
- The file can be edited in the Access controls page (including a visual policy editor) or through the Tailscale API.
- `tests` and `sshTests` are the guard rails for refactors.

**Checklist**

1. Prefer `grants` for new rules.
2. Define `tagOwners` before using tags.
3. Add `tests` for critical access.

## Checked

2026-11-03. Read Tailnet policy syntax (kb/1337) and confirmed the top-level sections, deny-by-default, grants versus ACLs and the tests sections. Nothing else was removed.

Method: documentation only; no commands were run.
