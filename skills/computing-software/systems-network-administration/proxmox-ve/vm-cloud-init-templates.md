---
id: computing-software.systems-network-administration.proxmox-ve.vm-cloud-init-templates
name: vm-cloud-init-templates
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [cloud-init, cloudinit, ipconfig0, sshkey, cicustom]
level: practitioner
status: docs-checked
description: "Build a Cloud-Init VM template on Proxmox VE and deploy clones with ssh keys and static IPs."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cloud-Init applies network and ssh key settings on first boot. Proxmox passes the data in a generated ISO, so every Cloud-Init VM needs a CD-ROM drive for it. Prepare your own image where possible, because you then know exactly what is installed; vendor cloud images (qcow2) also work. Then convert to a template and linked-clone it.

```
qm create 9000 --memory 2048 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci
qm set 9000 --scsi0 local-lvm:0,import-from=/path/to/cloudimg.img
qm set 9000 --ide2 local-lvm:cloudinit
qm set 9000 --boot order=scsi0
qm set 9000 --serial0 socket --vga serial0
qm template 9000
qm clone 9000 123 --name ubuntu2
qm set 123 --sshkey /path/to/id_ed25519.pub
qm set 123 --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
```

Ubuntu cloud images require `virtio-scsi-pci` for SCSI drives. The serial console as display is needed by many images; if it fails, return to the default display. Install `cloud-init` inside the VM (not on the host).

Options: `ciuser`, `sshkeys` (one OpenSSH key per line), `nameserver`, `searchdomain`, `ipconfig[n]` (`ip` and `gw`, or `dhcp`; IPv6 supports `auto`), and `ciupgrade` (default 1, package upgrade after first boot). With no address set, IPv4 defaults to DHCP. Prefer ssh keys over `cipassword`, since an encrypted password has to be stored in the Cloud-Init data. `citype` defaults to nocloud for Linux and configdrive2 for Windows (Cloudbase-Init).

Custom data: `qm set 9000 --cicustom "user=local:snippets/userconfig.yaml"` (also `network`, `meta`, `vendor`); the files must be on snippets-enabled storage reachable from every node. Dump generated config as a base with `qm cloudinit dump 9000 user`.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
