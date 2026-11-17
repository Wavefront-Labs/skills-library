---
id: computing-software.systems-network-administration.proxmox-ve.vm-create-and-manage-with-qm
name: vm-create-and-manage-with-qm
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [qm, qm-create, vmid, qemu-server, qm-destroy]
level: intro
status: docs-checked
description: "Create, start, stop and destroy QEMU/KVM virtual machines with qm and find their config files."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`qm` manages QEMU/KVM VMs: create, destroy, start, stop, suspend, resume, set options, create and delete disks. VM configs are plain `OPTION: value` text files in the cluster filesystem at `/etc/pve/qemu-server/<VMID>.conf`, replicated to all nodes. Lines starting with `#` are comments. VMIDs below 100 are reserved and VMIDs are unique cluster wide. Hand edits need a VM restart, whereas `qm set` and the GUI hot-plug most changes into a running VM.

```
qm create 300 -ide0 local-lvm:4 -net0 e1000 -cdrom local:iso/proxmox-mailgateway_2.1.iso
qm start 300
qm shutdown 300 && qm wait 300
qm shutdown 300 && qm wait 300 -timeout 40
qm stop 300 -overrule-shutdown 1
qm destroy 300 --purge
```

`qm stop` is a hard stop and can lose data; prefer `shutdown`. Destroying a VM always drops it from ACLs and removes its firewall config. `--purge` additionally removes it from replication jobs, backup jobs and HA resource configuration, and from HA affinity rules that reference it.

An example config:

```
boot: order=virtio0;net0
cores: 1
memory: 512
name: webmail
ostype: l26
net0: e1000=EE:D2:28:5F:B6:3E,bridge=vmbr0
virtio0: local:vm-100-disk-1,size=32G
```

Setting the right OS type (`ostype`) lets Proxmox tune low-level parameters; Windows expects a local-time BIOS clock and Unix systems UTC. For firmware, the default SeaBIOS is fine unless you want PCIe passthrough, where OVMF (UEFI) and the q35 machine type are the usual choice.

## Checked

2026-11-09. Confirmed against the Proxmox VE docs chapter Qemu/KVM Virtual Machines (chapter-qm) and the qm manual page: config file location and format, VMID rules, create/shutdown/wait/stop -overrule-shutdown/destroy --purge examples and purge scope, ostype clock note, SeaBIOS versus OVMF and q35 guidance.

Method: documentation only; no commands were run.
