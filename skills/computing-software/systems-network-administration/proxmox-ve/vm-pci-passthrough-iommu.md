---
id: computing-software.systems-network-administration.proxmox-ve.vm-pci-passthrough-iommu
name: vm-pci-passthrough-iommu
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [pci-passthrough, iommu, vfio, hostpci, intel-iommu]
level: advanced
status: docs-checked
description: "Enable IOMMU and VFIO and pass a PCI or PCIe device through to a Proxmox VE VM with hostpci."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A passed-through device is owned by the VM and unavailable to the host and other VMs. Passthrough works on i440fx and q35; PCIe passthrough only on q35. Passing through PCI devices blocks live migration.

Host setup:
1. Enable IOMMU (VT-d or AMD-Vi) in BIOS/UEFI. AMD enables it by default, as do Intel with kernels 6.8 or newer; on older kernels with Intel add `intel_iommu=on` to the kernel command line. Optionally add `iommu=pt` for performance.
2. Load modules via `/etc/modules-load.d/vfio.conf` with `vfio`, `vfio_iommu_type1`, `vfio_pci`. Mediated devices do not need this.
3. `update-initramfs -u -k all`, then reboot.

Verify:

```
dmesg | grep -e DMAR -e IOMMU -e AMD-Vi
lsmod | grep vfio
lspci -nnk
pvesh get /nodes/{nodename}/hardware/pci --pci-class-blacklist ""
```

`lspci -nnk` should show `Kernel driver in use: vfio-pci` (or no driver line). The pvesh call lists IOMMU groups; the device may share a group only with its own functions or its root port. Try another slot if grouping is poor. If binding fails, set `options vfio-pci ids=1234:5678` in `/etc/modprobe.d/`, or blacklist the host driver, or add `softdep <module> pre: vfio-pci`, then rebuild initramfs and reboot. `options vfio_iommu_type1 allow_unsafe_interrupts=1` may be needed but can destabilise the system.

Attach:

```
qm set VMID -hostpci0 02:00,pcie=on,x-vga=on
```

For GPUs prefer q35, OVMF and PCIe; OVMF needs a UEFI-capable GPU ROM. Options: `x-vga`, `pcie`, `rombar`, `romfile`. A passed-through GPU cannot be shown in noVNC or SPICE.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
