---
id: computing-software.systems-network-administration.virtualisation.proxmox-cloud-init-templates
name: proxmox-cloud-init-templates
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-cloud-init, qm-cloudinit, cloud-init, vm-template, cloud-image, snippets, cicustom, proxmox-vm, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Build Proxmox cloud-init templates from distro cloud images: import the disk, add the cloudinit drive, set user/keys/IP, custom user-data via snippets, and clone."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#qm_cloud_init
  - https://github.com/proxmox/pve-docs/blob/master/qm-cloud-init.adoc
  - https://pve.proxmox.com/pve-docs/qm.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud-init templates on Proxmox VE

**Goal:** new Linux VMs in seconds with hostname, users, SSH keys and network set at first
boot, from vendor cloud images.

## Build the template
```sh
wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
qm create 9000 --name ubuntu-2404-tmpl --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0 \
  --scsihw virtio-scsi-pci --agent enabled=1 --serial0 socket --vga serial0
qm set 9000 --scsi0 local-lvm:0,import-from=/root/noble-server-cloudimg-amd64.img,discard=on
qm set 9000 --ide2 local-lvm:cloudinit --boot order=scsi0
qm set 9000 --ciuser ops --sshkey /root/ops.pub --ipconfig0 ip=dhcp
qm template 9000
```
The admin guide notes that Ubuntu cloud images require the `virtio-scsi-pci` controller for SCSI drives, and that many cloud images need a serial console used as the display (`--serial0 socket --vga serial0`); switch back to the default display if that does not work for your image. Setting `--boot order=scsi0` restricts the BIOS to the image disk and speeds up boot. The `--ide2 <storage>:cloudinit` drive carries the cloud-init data. Install `qemu-guest-agent` in the image or through user-data.

## Deploy
```sh
qm clone 9000 121 --name web01 --full
qm set 121 --ipconfig0 ip=10.0.120.21/24,gw=10.0.120.1 --nameserver 10.0.0.10 --searchdomain <domain>
qm resize 121 scsi0 +30G
qm start 121
```
The docs show deploying by cloning, then setting `--sshkey` and `--ipconfig0`; templates are mainly valuable because linked clones are much faster than full copies.

## Custom user-data (packages, scripts)
Enable `snippets` content on a storage and write `web.yaml` into its `snippets/` folder:
```yaml
#cloud-config
packages: [qemu-guest-agent, nginx]
runcmd: [systemctl enable --now qemu-guest-agent]
```
`qm set 121 --cicustom "user=local:snippets/web.yaml"`. The `user`, `network`, `meta` (and `vendor`) configs can each be custom; any kind without a custom file uses the generated config. The snippet files must be on a snippets-capable storage available on every node the VM may migrate to, or the VM cannot start. Dump the generated config as a starting point: `qm cloudinit dump 121 user` (also `network`, `meta`).

## Gotchas
- Cloud-init applies configuration at boot inside the guest; check the guest's cloud-init behaviour before expecting later setting changes to be re-applied.
- Windows uses Cloudbase-Init, which does not support every cloud-init feature; it needs `ostype` set to a Windows version and `citype` `configdrive2` (the default for Windows ostypes).

## Verify
`qm cloudinit dump <id> network` shows the intended IP; the VM boots, is reachable by SSH
key, and `cloud-init status --long` reports done with no errors.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm-cloud-init.adoc and generated qm-cloud-init-opts.adoc) and confirmed the template build sequence (--scsihw virtio-scsi-pci, --ide2 cloudinit, --boot order=scsi0, --serial0 socket --vga serial0, qm template), the cloud-init options (ciuser, sshkeys, ipconfig[n], nameserver, searchdomain, cicustom with user, network, meta, vendor), the snippets requirement and qm cloudinit dump. Corrected the SCSI controller from virtio-scsi-single to virtio-scsi-pci per the docs; removed the unconfirmed Regenerate Image, instance-id, first-boot disk growth and machine-id claims.

Method: documentation only; no commands were run.
