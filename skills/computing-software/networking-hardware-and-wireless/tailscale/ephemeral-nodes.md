---
id: computing-software.networking-hardware-and-wireless.tailscale.ephemeral-nodes
name: ephemeral-nodes
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [ephemeral-nodes, ephemeral-auth-key, state-mem]
level: practitioner
status: docs-checked
description: "Use ephemeral auth keys for short-lived containers and CI so nodes clean up automatically."
sources: ["https://tailscale.com/kb/1111"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ephemeral nodes

Goal: register short-lived devices that disappear when done.

**Behaviour**

- Removed automatically after a short period of inactivity; a recreated node gets a new IP address.
- Removed immediately if you run `tailscale logout`.
- Created only with an ephemeral auth key, or by running `tailscaled` with the `--state=mem:` flag.
- The Machines page shows an Ephemeral badge.

**Steps**

1. Keys page: generate an auth key with Ephemeral enabled. Pre-approved appears only if device approval is enabled.
2. Use it in your scripts:
```
sudo tailscale up --auth-key=<your ephemeral key>
```
3. Trigger a build; the new device appears in Machines, and vanishes after it goes away.

**Tips from the docs**

- To avoid updating every device's netmap when an ephemeral device is added, use an ephemeral tagged auth key and restrict what tagged devices can access in policy.
- Guides exist for Heroku, Google Cloud Run, GitHub Actions, AWS Lambda and Kubernetes.
- Reusable keys are dangerous if stolen; keep them in a vault.

**Checklist**

1. Ephemeral flag on the key.
2. Key tagged.
3. Policy limits tagged devices.

## Checked

2026-11-03. Read Ephemeral nodes (kb/1111) and confirmed inactivity removal, `tailscale logout`, `--state=mem:`, the Ephemeral badge and the netmap tip. Nothing else was removed.

Method: documentation only; no commands were run.
