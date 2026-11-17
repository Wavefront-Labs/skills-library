---
id: computing-software.systems-network-administration.virtualisation.virt-v2v-vmware-to-kvm-conversion
name: virt-v2v-vmware-to-kvm-conversion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [virt-v2v, v2v, vmware-to-kvm, vddk, libvirt, virtio, kubevirt, conversion]
level: advanced
status: docs-checked
description: "Convert VMware guests to KVM, libvirt, oVirt or OpenShift Virtualization with virt-v2v: vCenter and VDDK inputs, output modes, virtio driver injection and Windows prerequisites."
sources:
  - https://libguestfs.org/virt-v2v.1.html
  - https://libguestfs.org/virt-v2v-input-vmware.1.html
  - https://libguestfs.org/virt-v2v-output-local.1.html
  - https://libguestfs.org/virt-v2v-support.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Convert VMware guests with virt-v2v

**Goal:** move a powered-off VMware VM to a KVM-based platform with drivers, bootloader and tools fixed automatically.

## What virt-v2v changes in the guest
Attempts to remove VMware Tools and copies in virtio drivers and guest agents so the guest boots on KVM. For Windows the drivers come from the `virtio-win` package (searched in `/usr/share/virtio-win`); setting `VIRTIO_WIN` to an ISO or directory overrides that, but the manual recommends leaving it unset. Windows conversion finishes at first boot, which can reboot several times; do not interrupt it.

## Inputs
```bash
# From vCenter over HTTPS (slow, simple)
virt-v2v -ic 'vpx://administrator%40vsphere.local@vcenter.example/DC1/Cluster1/esxi01.example?no_verify=1' \
  -ip /root/vcenter.pw  'app01'  -o local -os /var/tmp/v2v -of qcow2

# From vCenter with VDDK (much faster)
virt-v2v -ic 'vpx://...' -it vddk -io vddk-libdir=/opt/vmware-vix-disklib-distrib \
  -ip /root/vcenter.pw 'app01' -o libvirt -os default

# From an OVA or local VMX
virt-v2v -i ova app01.ova -o local -os /var/tmp/v2v
```
`-ip` takes a file containing the password, not the password itself. `-io vddk-thumbprint=XX:XX:...` is optional and hardens against some man-in-the-middle attacks; since virt-v2v 2.10 it is fetched automatically when omitted (the `openssl` command must be installed).

## Outputs
`-o libvirt` (the default; `-os` names a storage pool), `-o local` (disks plus libvirt XML in the directory given by `-os`, same as `-o disk`), `-o qemu`, `-o null`, `-o openstack`, `-o ovirt` and `-o ovirt-upload` (oVirt builds only), and `-o kubevirt`, which the manual marks experimental. For Proxmox VE, write disks with `-o local` and attach them with `import-from` on `qm create` or `qm set` (documented in the Proxmox qm manual).

## Prerequisites
- Source VM shut down cleanly. Guests using Windows Fast Startup or hibernated cannot be converted. Convert from a snapshot only as a throwaway test.
- virt-v2v cannot reconfigure guest networking; if the target is on a different subnet, update the guest's network configuration afterwards (see `virt-customize`).
- Windows guests whose BitLocker key is held in the VMware vTPM will ask for the recovery key at first boot on the target, so have it ready.

## Gotchas
- VDDK is a separate VMware download with its own licence.
- Check the virt-v2v support notes for supported guest operating systems.

## Verify
The converted VM boots on virtio disk and NIC, `lsmod | grep virtio` (Linux) or Device Manager shows Red Hat VirtIO devices, and the app passes its checks.

## Checked

Checked 2026-10-27 against the virt-v2v manual pages in the libguestfs/virt-v2v repository (virt-v2v, virt-v2v-input-vmware, virt-v2v-output-local, virt-v2v-support). Confirmed: the output modes (`libvirt` default, `local`, `disk`, `qemu`, `null`, `openstack`, `ovirt`, `ovirt-upload`, experimental `kubevirt`; there is no `rhv-upload`), `-it vddk` with `-io vddk-libdir`, `-ip` taking a password file, the optional VDDK thumbprint (automatic since 2.10), the `VIRTIO_WIN` override and the recommendation to leave it unset, the Fast Startup and hibernation limitation, the vTPM and BitLocker recovery-key behaviour, and that guest networking is not reconfigured. The Proxmox qm manual (proxmox/pve-docs) documents `import-from` for attaching disk images.

Method: documentation only; no commands were run.
