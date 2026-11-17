---
id: computing-software.cloud-infrastructure-engineering.azure.vm-start-failures-and-os-provisioning-timeouts
name: vm-start-failures-and-os-provisioning-timeouts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-troubleshooting, osprovisioningtimedout, vm-start-failure, provisioning-failed, guest-agent]
level: practitioner
status: docs-checked
description: "Fix VMs that fail to create or start: OSProvisioningTimedOut, client errors, allocation failures, disk lease conflicts and agent communication errors, using Learn's error list."
sources: ["https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/troubleshoot-deployment-new-vm-windows", "https://learn.microsoft.com/troubleshoot/azure/virtual-machines/linux/linux-azure-guest-agent", "https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/error-messages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM start failures and provisioning timeouts

**Goal:** classify a create/start failure correctly - image, capacity, configuration or guest - and pick the right fix.

Learn splits create-time failures in two: a **provisioning failure** (the OS image fails to load, from incorrect preparatory steps or wrong settings at image capture) and an **allocation failure** (the cluster or region has no resources or cannot support the requested VM size). Start with the activity log to find the error code.

## Error map
| Error | Meaning (from the Learn error-message list) | Fix |
|---|---|---|
| `OSProvisioningTimedOut` | OS provisioning did not finish in the allotted time; the VM may still finish, so check the provisioning state later | Make sure the image was properly prepared (generalized). If the message says the guest agent was detected running, the guest was not prepared as an image: use the VHD as is with `CreateOption=Attach`, or prepare it properly for `FromImage` |
| `OSProvisioningClientError` | Guest OS provisioning failed (the page lists: image not properly generalized, SSH host key generation failed, username invalid for the Linux distribution) | Prepare the image properly; verify the Linux agent is set up correctly; fix the OS profile username |
| `AllocationFailed` / `OverConstrainedAllocationRequest` | Allocation failed, or the required size is not available in the selected location | Per the message: reduce the VM size or number of VMs, retry later, or deploy to a different availability set or Azure location |
| `AcquireDiskLeaseFailed` / `ConflictingUserInput` (disk already owned by VM) | Blob already in use, or the disk is already owned by another VM | Release or detach from the other VM, or use a different disk |
| `VMAgentStatusCommunicationError` | The VM has not reported status for the VM agent or extensions | Verify a running VM agent that can establish outbound connections to Azure storage |
| `VMStartTimedOut` | VM did not start in the allotted time; it may still start | Check the power state later |

## Provisioning versus allocation
- Image prepared incorrectly or wrong capture settings: provisioning failure. Cluster/region has no capacity or size support: allocation failure.
- If the guest OS was not prepared to be used as a VM image, the `OSProvisioningTimedOut` message offers two ways out: use the VHD as is with `CreateOption=Attach`, or prepare it properly for use as an image.

## Investigate
```bash
az vm get-instance-view -g rg -n vm01 --query "instanceView.statuses"
az vm boot-diagnostics get-boot-log -g rg -n vm01
```
Linux guest agent events are written to `/var/log/waagent.log`. Check that the agent service (`walinuxagent` or `waagent`) is running and that `AutoUpdate.Enabled=y` is set in `/etc/waagent.conf`.

## Agent cannot reach the host
The Linux agent talks to the Fabric Controller at 168.63.129.16, a virtual public IP that should not be blocked. Test it from the VM with `curl http://168.63.129.16/?comp=versions` (root required), and check that outbound ports 80, 443 and 32526 are open in the local firewall; check IPTables or a third-party firewall, and any proxy.

## Recover a stuck VM
The error list says to use `reapply` (or `redeploy` for uniform scale sets) when data disks are force detached (`DataDisksForceDetached`). The commands are:
```bash
az vm reapply -g rg -n vm01
az vm redeploy -g rg -n vm01
```
For a broken guest, the `vm-repair` extension provides `az vm repair create` to build a rescue VM from a copy of the OS disk.

## Checked
Date: 2026-11-07
Read in full: Learn "Understand common error messages when you manage virtual machines in Azure" (error codes and messages used in the table), "Troubleshoot the Azure Linux Agent" (168.63.129.16, ports 80/443/32526, waagent.log, AutoUpdate.Enabled, curl test), and "Troubleshoot deployment issues when creating a new Windows VM" (a short page: the provisioning-versus-allocation definitions only).
Removed as unconfirmed on these pages: `SkuNotAvailable`, `ZonalAllocationFailed`, the quota error row, cloud-init log paths, the Windows Panther setup log, the Trusted Launch/Gen2 error, the claim that redeploy/reapply clear failed states, the "attach-style needs no credentials" claim, the `tail -100` and the Verify checklist. Command existence for the `az vm` lines was checked against the CLI reference by the review tooling; the `vm-repair` extension reference page was not opened.
Method: documentation only; no commands were run.
