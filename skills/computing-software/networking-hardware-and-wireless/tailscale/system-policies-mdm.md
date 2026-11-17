---
id: computing-software.networking-hardware-and-wireless.tailscale.system-policies-mdm
name: system-policies-mdm
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [system-policies, mdm, always-on]
level: advanced
status: docs-checked
description: "Use MDM-deployed system policy keys to control exit nodes, updates and runtime behaviour."
sources: ["https://tailscale.com/kb/1315"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System policies

Goal: centrally configure Tailscale clients with MDM or group policy.

Policy keys are grouped by category, and each key lists the platforms that support it (Android, iOS, Linux, macOS, macOS standalone only, tvOS, Windows).

**Examples from the docs**

- Auto update: `ApplyUpdates`, `CheckUpdates`, `InstallUpdates` (Windows), `SUAutomaticallyUpdate`, `SUEnableAutomaticChecks` and `UnstableUpdates` (macOS standalone only).
- Exit nodes: `AdvertiseExitNode`, `AllowedSuggestedExitNodes`, `ExitNode.AllowOverride`, `ExitNodeAllowLANAccess`, `ExitNodeID`.
- Organization: `ManagedByCaption`, `ManagedByOrganizationName`, `ManagedByURL`.
- Runtime configuration: `AllowIncomingConnections`, `AlwaysOn.Enabled`, `AlwaysOn.OverrideWithReason`, `AuthKey`, `EncryptState`, `Hostname`, `ForceEnabled`.
- UI visibility settings to hide items that might confuse users.

**Related**

- With `AlwaysOn.Enabled` and `AlwaysOn.OverrideWithReason` set, `tailscale down` accepts `--reason="<description>"`.
- Force a device to use an exit node by policy through MDM.

The docs table can be filtered by category and by platform, and each key row names the platforms that support it, so check that column before writing a profile for a mixed fleet.

Filter the table by category and platform in the docs before writing a profile.

**Checklist**

1. Check key support per platform.
2. Test a profile on one device.
3. Document overrides.

## Checked

2026-11-03. Read System policies (kb/1315) and confirmed the listed policy keys and their categories, and the `tailscale down --reason` link to `AlwaysOn` policies. Nothing else was removed.

Method: documentation only; no commands were run.
