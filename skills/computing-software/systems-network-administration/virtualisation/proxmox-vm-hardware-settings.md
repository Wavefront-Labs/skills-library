---
id: computing-software.systems-network-administration.virtualisation.proxmox-vm-hardware-settings
name: proxmox-vm-hardware-settings
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm, qm-config, pve-cpu-type, proxmox-vm, q35, ovmf, virtio-scsi-single, iothread, x86-64-v2-aes, proxmox, proxmox-ve, kvm]
level: practitioner
status: docs-checked
description: "Choose Proxmox VM hardware with qm: machine type (i440fx/q35), BIOS vs OVMF, CPU type for migration, VirtIO SCSI single with iothread, NIC model, ballooning and NUMA."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.conf.5.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VM hardware settings with qm

**Goal:** VMs configured for performance and portability across the cluster, created
reproducibly from the CLI.

## Create a sensible default VM
```sh
qm create 120 --name app01 --ostype l26 --machine q35 --bios ovmf \
  --efidisk0 local-lvm:1,efitype=4m,pre-enrolled-keys=1 \
  --cpu x86-64-v2-AES --sockets 1 --cores 4 --memory 8192 --balloon 4096 \
  --scsihw virtio-scsi-single --scsi0 local-lvm:64,iothread=1,discard=on,ssd=1 \
  --net0 virtio,bridge=vmbr0,tag=120 --agent enabled=1 --onboot 1
qm config 120
```

## Choices
| Setting | Recommendation |
|---|---|
| Machine | `i440fx` is the default; `q35` provides a virtual PCIe bus and is the choice for PCIe passthrough. For Windows guests the machine version is pinned at creation (for example `pc-q35-8.1`) because Windows is sensitive to hardware changes; Linux guests use the latest version by default |
| Firmware | OVMF (UEFI) needs an EFI disk (`--efidisk0`, `efitype=4m`, `pre-enrolled-keys=1` for Secure Boot keys); SeaBIOS is the default |
| CPU type | `host` gives the guest exactly the host CPU flags but can break live migration to hosts with a different CPU. For mixed clusters pick a generic model: `x86-64-v2-AES` (Intel Westmere or newer, AMD Opteron G4 or newer; the GUI default for new VMs) or `x86-64-v3` (Intel Haswell or newer, AMD EPYC or newer). The backend default is `kvm64` |
| Disk controller | `virtio-scsi-single` with the IO Thread (`iothread=1`) setting is recommended for performance and is the default for new Linux VMs; the controller default otherwise is LSI 53C895A. Windows needs the VirtIO driver ISO at install |
| Cache | The default `No cache` notifies the guest of write completion once blocks reach the physical storage write queue, bypassing the host page cache: a good balance of safety and speed |
| NIC | `virtio`; `queues` (0-64) enables multiqueue, recommended equal to the VM's vCPU count (on Windows also set RSS and the maximum RSS queues in the driver) |
| Memory | Ballooning needs the guest balloon driver; `balloon` is the minimum target in MiB and `0` disables it |
| NUMA | `numa=1` is recommended when the host has more than one NUMA node, and is required to hot-plug cores or RAM; set sockets to the host's node count |
| vTPM | `--tpmstate0 local-lvm:1,version=v2.0`; v2.0 is preferred unless an implementation needs v1.2. An emulated TPM gives no real security benefit over a physical one |

## Edit and inspect
```sh
qm set 120 --cores 8
qm set 120 --delete balloon
qm showcmd 120 --pretty         # the actual KVM command line
qm monitor 120                  # QEMU monitor (info block, info cpus)
```
Use `qm pending <vmid>` to see changes that have not been applied yet; most hardware changes need a fresh start of the VM.

## Gotchas
- Live migration requires hosts with CPUs from the same vendor and similar capabilities; a `host` CPU type in a mixed cluster can end on a host with different flags, and Intel to AMD migrations have no guarantee.
- Windows needs the VirtIO storage driver installed before switching a disk to VirtIO or SCSI.

## Verify
`qm config` matches the template; `qm showcmd <vmid> --pretty` shows the CPU model you chose and virtio devices; a live migration to every node works for a mixed-cluster CPU type.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc Machine Type, Hard Disk, Network Device, CPU, Memory, NUMA and TPM sections; generated qm.1-synopsis.adoc showcmd) and confirmed the CPU model definitions and defaults (x86-64-v2-AES GUI default, kvm64 backend default), the machine version pinning rule for Windows, the VirtIO SCSI single and IO Thread recommendation, the cache default, multiqueue guidance, NUMA hot-plug requirement, EFI disk and TPM option syntax, and the live-migration CPU requirements. Corrected the claim that x86-64-v2-AES is a PVE 8 default and that q35 is the default machine type; removed the unconfirmed Windows 11 and NUMA-latency statements.

Method: documentation only; no commands were run.
