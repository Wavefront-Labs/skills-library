---
id: computing-software.networking-hardware-and-wireless.tailscale.device-approval
name: device-approval
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [device-approval, needs-approval, pre-approved]
level: practitioner
status: docs-checked
description: "Enable device approval and pre-approve trusted automation with auth keys."
sources: ["https://tailscale.com/kb/1099"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Device approval

Goal: stop new devices passing traffic until an admin approves them.

**Enable.** Owner, Admin or IT admin: Device management page of the admin console.

**Effect.** A new device shows a Needs approval badge at the top of the Machines page and cannot send or receive traffic until approved. Approve from its menu; the device connects immediately, with no restart.

**Pre-approve.** Owner, Admin, IT admin or Network admin can generate an auth key with Pre-approved selected (Keys page, Generate auth key). The option only appears when device approval is enabled. A device using that key is approved automatically. Keys can carry tags, set from the admin console or API.

**Automation.** Configure a webhook for `nodeNeedsApproval`, verify the node against your own criteria (for example an internal device registry or a third-party posture check), then POST `{"authorized": true}` to `https://api.tailscale.com/api/v2/device/<id>/authorized`. The same call with `false` revokes authorization.

**Checklist**

1. Enabled on Device management page.
2. Pre-approved keys only for trusted automation.
3. Review the Needs approval list.

## Checked

2026-11-09. Confirmed against the Tailscale Device approval page: roles, Device management and Machines pages, Needs approval badge, pre-approved auth keys, nodeNeedsApproval webhook and the authorized API call. Removed the unsourced note about user approval.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1099 (Device approval), read in full.
