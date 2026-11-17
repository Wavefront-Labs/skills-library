---
id: computing-software.cloud-infrastructure-engineering.azure.vm-redeploy-vs-reapply
name: vm-redeploy-vs-reapply
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-redeploy, redeploy, reapply, vm-troubleshooting, failed-state, temp-disk]
level: practitioner
status: docs-checked
description: "Choose and run VM Redeploy (move to a new host, loses temp disk) vs Reapply (re-push VM model to fix a Failed state) and know their side effects."
sources: ["https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/redeploy-to-new-node-windows", "https://learn.microsoft.com/troubleshoot/azure/virtual-machines/linux/redeploy-to-new-node-linux", "https://learn.microsoft.com/cli/azure/vm#az-vm-reapply", "https://learn.microsoft.com/azure/virtual-machines/states-billing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redeploy vs reapply

**Goal:** pick the low-risk fix for a misbehaving VM before escalating to rescue VMs or support.

## Comparison
| | Redeploy | Reapply |
|---|---|---|
| What it does | Shuts down, moves the VM to a **new node**, powers on; configuration and associated resources are retained | Re-applies the VM's state; try it first when the VM is stuck in a failed state |
| Use when | RDP/SSH or application access fails and the OS looks healthy | VM stuck in a **failed** state, before redeploying |
| Temp and ephemeral disk data | **Lost** | Not stated as affected |
| Dynamic IP addresses on the NIC | **Updated** | Not stated as affected |

## Run
```bash
az vm redeploy -g rg -n vm1
az vm reapply  -g rg -n vm1
```
PowerShell: `Set-AzVM -Redeploy -ResourceGroupName rg -Name vm1`; `Set-AzVM -Reapply ...`.
Portal: VM → Help → *Redeploy + reapply*.

## Order of operations for an unreachable VM
1. Boot diagnostics screenshot — is the OS up?
2. Network Watcher IP flow / effective NSG rules.
3. Run Command — if it works, the OS and agent are up: fix in-guest.
4. **Reapply** if the VM shows Failed or the agent reports stale config.
5. **Redeploy** if the OS looks healthy but the host path is broken.
6. Then `az vm repair` rescue VM for OS-level breakage.

## Gotchas
- Redeploy loses anything on the temporary and ephemeral disks — confirm nothing durable lives there.
- Neither fixes guest OS corruption.

## Verify
- [ ] After redeploy: `az vm get-instance-view -g rg -n vm1 --query "instanceView.statuses[].code"` shows `PowerState/running`, connectivity restored.
- [ ] After reapply: the VM is no longer in a failed state.

## Checked

Date: 2026-10-28.

Confirmed against Learn (redeploy to a new node, Linux and Windows): redeploy moves the VM to a new node and retains configuration and associated resources, temporary and ephemeral disk data is lost, dynamic IP addresses on the virtual network interface are updated, reapply is the step to try for a VM stuck in a failed state, portal path Help > Redeploy + reapply. CLI commands via check_commands.py.
Removed: downtime comparison, private and static public IP statements, availability set, dedicated host and AllocationFailed gotchas, SQL tempdb note, the Run Command cmdlet name.

Method: documentation only; no commands were run.
