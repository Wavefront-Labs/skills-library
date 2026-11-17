---
id: computing-software.systems-network-administration.virtualisation.esxi-kill-hung-vm
name: esxi-kill-hung-vm
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxcli-vm-process, hung-vm, vm-kill, vim-cmd, vmx-process, invalid-vm, orphaned-vm, vsphere-troubleshooting, vmware, esxi]
level: practitioner
status: docs-checked
description: "Stop a VM that will not power off: vSphere Client, vim-cmd, esxcli vm process kill soft/hard/force, esxtop kill and the vmx process kill as a last resort."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1014165
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Killing a hung VM on ESXi

**Goal:** stop a stuck VM with the least invasive method that works.

If you are troubleshooting an unresponsive VM rather than just stopping it, the Broadcom
article prefers collecting performance metrics and then suspending or crashing the VM to
gather troubleshooting data before powering it off.

## Escalation ladder
1. vSphere Client: right-click the VM and Power off. If it fails with "Another task is
   already in progress", wait for that task. If the VM still runs, try Power off from the
   Host Client of the host running it. If the VM is encrypted, the user needs the
   Cryptographic Operations privileges.
2. From the ESXi shell with vim-cmd:
```sh
vim-cmd vmsvc/getallvms                 # VMID, name, .vmx path
vim-cmd vmsvc/power.getstate <VMID>
vim-cmd vmsvc/power.shutdown <VMID>
vim-cmd vmsvc/power.off <VMID>          # if shutdown fails
```
3. ESXCLI process kill:
```sh
esxcli vm process list                  # World ID, UUID, name, .vmx path
esxcli vm process kill -t soft  -w <WorldID>
esxcli vm process kill -t hard  -w <WorldID>
esxcli vm process kill -t force -w <WorldID>
```
   Run `esxcli vm process list` again to confirm the VM is gone.
4. esxtop: press `c` (CPU screen), `Shift+v` (VMs only), `f` and `c` to add the Leader
   World ID column, identify the VM, press `k`, enter the Leader World ID at the "World to
   kill" prompt, wait 30 seconds and check it is gone.
5. Last resort, hazardous: `ps | grep vmx` and identify the parent vmx process of the
   target VM only (the second column is the parent PID). Run `kill <PID>`, wait 30 seconds,
   check again, then `kill -9 <PID>` if needed. Killing the wrong process can affect other VMs.

If none of this works and the host is responsive, the article says a reboot of the host is
required to power off the VM. It adds that failure of every method usually points to the
infrastructure under the VM (the ESXi host or its hardware); for a suspected host problem it
describes vMotioning the unaffected VMs away and forcing a purple diagnostic screen (see its
article 344096 on NMI facilities).

## Verify
`esxcli vm process list` (or `ps | grep vmx`) no longer shows the VM.

## Checked
Date: 2026-11-07. Read the whole Broadcom KB article "Unable to Power off a Virtual Machine
in an ESXi host" (options 1 to 5, additional information). Every command above is on it;
the esxcli flags are written as the article's short -t/-w forms. Removed as not on the
page: the pending-question step, descriptions of what soft/hard/force do internally,
`ps -c`, the "why VMs hang" list, the invalid/orphaned/lock-file clean-up section and
the guest filesystem check in Verify. Linked articles were not opened.
Method: documentation only; no commands were run.
