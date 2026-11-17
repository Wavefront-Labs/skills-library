---
id: computing-software.systems-network-administration.virtualisation.proxmox-pci-gpu-passthrough
name: proxmox-pci-gpu-passthrough
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-pci-passthrough, iommu, vfio, gpu-passthrough, resource-mapping, mediated-devices, proxmox-vm, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Pass PCIe devices and GPUs to Proxmox VMs: IOMMU enablement, IOMMU groups, vfio binding, resource mappings for cluster use, SR-IOV/mdev, and migration limits."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#qm_pci_passthrough
  - https://github.com/proxmox/pve-docs/blob/master/qm-pci-passthrough.adoc
  - https://pve.proxmox.com/pve-docs/qm.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCI and GPU passthrough on Proxmox VE

**Goal:** give a VM direct access to a GPU, NIC or HBA with near-native performance, in a
way the cluster can manage.

## Enable IOMMU
- BIOS/UEFI: enable IOMMU support (usually called `IOMMU` or `VT-d`; the exact name is in the motherboard manual).
- Kernel: IOMMU is enabled by default on AMD CPUs, and on Intel CPUs with kernel 6.8 or newer; on older kernels add `intel_iommu=on` to the kernel command line (x86 only). If the hardware supports IOMMU passthrough mode, add `iommu=pt` for possibly better performance. Edit the command line with the boot-loader method for your system (`/etc/default/grub` plus `update-grub`, or `/etc/kernel/cmdline` plus `proxmox-boot-tool refresh`).
- Modules: make sure `vfio`, `vfio_iommu_type1` and `vfio_pci` are loaded by listing them in a file under `/etc/modules-load.d/` (for example `vfio.conf`), then run `update-initramfs -u -k all`; check with `lsmod | grep vfio`.
- Check: the docs verify with `pvesh get /nodes/<node>/hardware/pci --pci-class-blacklist ""`, which also shows IOMMU groups.

## IOMMU groups
The device to pass through must be in a separate IOMMU group. It is fine for a device to share a group with its own functions (for example a GPU with its HDMI audio device) or with its root port or PCI(e) bridge. If you do not get the needed separation, putting the card in another physical slot can help on some platforms.

## Bind and assign
- Proxmox VE tries to make the device unavailable to the host automatically. If that does not work, pass the device IDs to the vfio-pci module in a `.conf` file under `/etc/modprobe.d/` (`options vfio-pci ids=<vendor>:<device>,<vendor>:<device>`) or blacklist the host driver, and refresh the initramfs; if vfio-pci loads too late, set a softdep (`softdep <host-module> pre: vfio-pci`).
- **Resource mapping** (Datacenter → Resource Mappings → PCI): name the device per node so
  a VM can start on any node with a matching device.
- Assign: `qm set 130 --hostpci0 mapping=gpu-a100,pcie=1` or by address, for example `qm set 130 -hostpci0 02:00,pcie=on,x-vga=on` for a primary GPU. For GPUs the docs recommend the `q35` machine type, OVMF (UEFI) instead of SeaBIOS (the GPU needs a UEFI-capable ROM) and PCIe instead of PCI; `pcie` is only available on q35. Other options: `rombar`, `romfile`, and the `device-id`, `vendor-id`, `sub-device-id`, `sub-vendor-id` overrides.

## SR-IOV and mediated devices
NICs with SR-IOV expose virtual functions (VFs). Set the VF count through a driver option such as `max_vfs` in a file under `/etc/modprobe.d/` (then update the initramfs), or at runtime with `echo 4 > /sys/bus/pci/devices/<address>/sriov_numvfs`, made persistent with the `sysfsutils` package (`/etc/sysfs.conf` or `/etc/sysfs.d/`); pass the VFs to VMs instead of the whole card. Mediated devices use the `mdev=<type>` property on a `hostpciX` entry (for example `qm set <vmid> -hostpci0 00:02.0,mdev=i915-GVTg_V5_4`); PVE creates the device at VM start and cleans it up at stop.

## Limits
- PCI or USB devices that are passed through block live migration; offline migration is possible, and hardware passthrough configuration may need adapting to the device location on the target host.
- Cluster-level resource mappings let devices be used properly with HA, detect hardware changes and allow non-root users to configure them.

## Verify
`lspci -nnk -s <addr>` shows `Kernel driver in use: vfio-pci`; inside the guest the device
appears with its vendor driver loaded (`nvidia-smi`, `lspci`).

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm-pci-passthrough.adoc, qm.adoc Online Migration requirements, generated qm.conf.5-opts.adoc hostpci[n]) and confirmed the IOMMU defaults (Intel default-on from kernel 6.8), the iommu=pt note, the vfio module list and location, vfio-pci ids and softdep options, IOMMU group rules, the hostpci option names and the SR-IOV and mdev procedures. Moved the vfio module list to /etc/modules-load.d as the docs state and removed the unconfirmed BIOS Above-4G, ACS override, memory-locking and device-reset claims.

Method: documentation only; no commands were run.
