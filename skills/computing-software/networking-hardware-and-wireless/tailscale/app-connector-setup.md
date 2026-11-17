---
id: computing-software.networking-hardware-and-wireless.tailscale.app-connector-setup
name: app-connector-setup
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [app-connector, advertise-connector, nodeattrs]
level: advanced
status: docs-checked
description: "Prepare the policy file and a Linux node so a SaaS or self-hosted app is reached through an app connector."
sources: ["https://tailscale.com/kb/1342"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# App connector setup

Goal: route traffic for an application through a designated tailnet node.

**Requirements**

- Owner, Admin or Network admin to edit the policy file and manage app connector settings.
- A Linux device (physical or VM) with a publicly accessible IP address and IP forwarding enabled.
- A SaaS or self-hosted application you administer.

**Preset app type**

1. Add the app connector in the admin console; this adds a target entry to `nodeAttrs` automatically.
2. Update the policy file with `tagOwners`, `autoApprovers` and `grants` entries.
3. Configure the Linux node as the connector.
4. Optional: restrict the app to accept traffic only from the connector device with an IP allowlist.

**Custom app type**

1. Add entries to `nodeAttrs`, `tagOwners`, `autoApprovers` and `grants`.
2. Configure the Linux node.
3. Add the settings in the admin console.
4. Optional IP allowlist.

**tagOwners example**
```
"tagOwners": {
  "tag:github-app-connector": ["group:github-admins"]
}
```

The node itself is started with `--advertise-connector` and the tag, as in the HA skill.

**Checklist**

1. Tag owners defined.
2. Auto-approve rule present.
3. Connector node forwards IP.
4. Allowlist the connector in the app.

## Checked

2026-11-03. Read App connector setup (kb/1342) and confirmed role and Linux node requirements including a public IP and IP forwarding, preset and custom app types, and tagOwners. Nothing else was removed.

Method: documentation only; no commands were run.
