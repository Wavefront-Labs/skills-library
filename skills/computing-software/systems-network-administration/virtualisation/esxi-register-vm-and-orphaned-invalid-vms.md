---
id: computing-software.systems-network-administration.virtualisation.esxi-register-vm-and-orphaned-invalid-vms
name: esxi-register-vm-and-orphaned-invalid-vms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [register-vmx, invalid-orphaned-vm, vim-cmd, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Register and unregister VMs from their .vmx file with the vSphere Client or vim-cmd, and the rules for doing it through vCenter when the host is managed."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1006160
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Register and unregister VMs

**Goal:** add a VM to inventory from its `.vmx` file, or remove it from inventory without
touching its files.

## Rules from the Broadcom article
- Register a VM on one ESXi host at a time.
- If the host is managed by vCenter Server, register through vCenter. Bypassing vCenter may
  cause a mismatch between the host and vCenter inventory and unexpected results.

## Register in vCenter (vSphere Client)
1. Click the host, then the Datastores tab, then the datastore, then the Files tab.
2. Open the VM's directory and select its `.vmx` file.
3. Click **Register VM** and follow the wizard.

## Register from the ESXi host
SSH in as root and run:
```sh
vim-cmd solo/registervm /vmfs/volumes/<datastore_name>/<VM_directory>/<VM_name>.vmx
```

## Unregister
- vCenter: power off the VM, right-click it and choose **Remove from inventory**.
- ESXi host, as root over SSH:
```sh
vim-cmd vmsvc/getallvms | grep <vm_name>     # VM ID is the leftmost column
vim-cmd vmsvc/unregister <VM ID>
```

## Invalid or orphaned VMs
The article only points to a separate Broadcom article, "Virtual machines appear as invalid
or orphaned in vCenter Server", for that case. This skill does not cover the repair steps.

## Checked
Date: 2026-11-07. Read the whole Broadcom KB article "Add or Register a Virtual Machine (VM)
in vCenter Server". Everything above is on it. Removed as not on the page: the
orphaned/invalid/inaccessible definitions and repair steps (`vmsvc/reload`, `.vmx~`
restore), the PowerCLI New-VM and Remove-VM examples, the side-effects list for the new
managed object ID, the "I moved it" and "I copied it" answer, and the hostd restart
section. The linked invalid/orphaned article was not opened.
Method: documentation only; no commands were run.
