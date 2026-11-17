---
id: computing-software.networking-hardware-and-wireless.tailscale.device-identity-collection
name: device-identity-collection
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [device-identity, posture-checking, tailscale-set]
level: advanced
status: docs-checked
description: "Opt a tailnet and its devices in to reporting identity for posture integrations."
sources: ["https://tailscale.com/kb/1326"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Device Identity Collection

Goal: let devices report identity for device posture integrations.

**Tailnet switch.** Device management page, Device Posture Integrations section, enable the Device Identity Collection toggle.

**Per device.** Each device must opt in individually. The feature arrived in Tailscale 1.52. Prerequisite: access to run the CLI on the machine, or an MDM.

Two ways:

1. System policy: set the policy key `PostureChecking` to `always`. This is the recommended method on macOS and Windows and takes priority over CLI configuration.
2. CLI, then reconnect:
```
sudo tailscale set --posture-checking=true
sudo tailscale down
sudo tailscale up
```

Posture rules can use pre-populated host information such as the OS version, custom attributes set through the postures API, or attributes synced from integrations.

Related: The `--report-posture` flag of `tailscale up` lets the management plane gather posture information; it defaults to false.

**Checklist**

1. Tailnet toggle on.
2. Policy key or CLI on each device.
3. Reconnect after CLI change.

## Checked

2026-11-03. Read Device identity collection (kb/1326) and confirmed the tailnet toggle, `PostureChecking` policy, `tailscale set --posture-checking` and v1.52; reworded the `--report-posture` mention. Nothing else was removed.

Method: documentation only; no commands were run.
