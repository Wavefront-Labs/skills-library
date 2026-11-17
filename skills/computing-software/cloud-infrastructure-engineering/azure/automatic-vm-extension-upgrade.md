---
id: computing-software.cloud-infrastructure-engineering.azure.automatic-vm-extension-upgrade
name: automatic-vm-extension-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-extensions, automatic-extension-upgrade, auto-upgrade-minor-version, enableautomaticupgrade, patching]
level: practitioner
status: gated
description: "Keep VM and scale set extensions patched: enableAutomaticUpgrade vs autoUpgradeMinorVersion, supported extensions, rollout safety and checking versions across the fleet."
sources: ["https://learn.microsoft.com/azure/virtual-machines/automatic-extension-upgrade", "https://learn.microsoft.com/cli/azure/vm/extension#az-vm-extension-set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic extension upgrade

**Goal:** agents like AMA, Dependency agent and Key Vault extension get security fixes without redeploying VMs.

## Two different flags
| Property | Behaviour |
|---|---|
| `autoUpgradeMinorVersion: true` | Separate extension property, not described on the Automatic Extension Upgrade page (gated: unconfirmed, source is paywalled or blocked) |
| `enableAutomaticUpgrade: true` | Platform upgrades the extension when the publisher releases a new version; must be set on every extension definition individually |

## Enable
```bash
az vm extension set -g rg --vm-name vm01 -n AzureMonitorLinuxAgent --publisher Microsoft.Azure.Monitor \
  --enable-auto-upgrade true
az vmss extension set -g rg --vmss-name vmss-web -n AzureMonitorLinuxAgent --publisher Microsoft.Azure.Monitor \
  --enable-auto-upgrade true
```
Bicep: `properties: { enableAutomaticUpgrade: true, autoUpgradeMinorVersion: true, ... }`.

## Rollout safety
Upgrades follow an availability-first model; VM health is checked after each upgrade (waits up to five minutes) and failed upgrades are rolled back automatically. Scale sets with application health probes or the Application Health extension also have application health monitored between batches.

## Supported extensions
Only extensions listed in the Supported extensions table of the Learn page (it includes the Dependency Agent for Linux and Windows); check the table before enabling.

## Fleet check
```kusto
resources
| where type == "microsoft.compute/virtualmachines/extensions"
| extend auto = tobool(properties.enableAutomaticUpgrade), ver = tostring(properties.typeHandlerVersion)
| summarize count() by tostring(properties.type), ver, auto
```

## Gotchas
- Policies deploying extensions (DINE) should set the flag in their templates, or newly deployed agents won't auto-upgrade.

## Verify
- [ ] ARG shows `enableAutomaticUpgrade = true` for all supported agents; versions converge after a publisher release.

## Checked
2026-10-28. Confirmed on the automatic-extension-upgrade page: `enableAutomaticUpgrade` must be true on each extension definition, availability-first rollout, five-minute health wait, automatic rollback of failed upgrades, Supported extensions table with Dependency Agent. Gated: the `autoUpgradeMinorVersion` description. Removed: major-version rule, named supported extensions other than Dependency Agent, unsupported-extension failure, restart/maintenance-window advice. Command flags were checked by check_commands.
Method: documentation only; no commands were run.
