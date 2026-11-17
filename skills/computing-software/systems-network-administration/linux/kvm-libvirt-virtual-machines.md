---
id: computing-software.systems-network-administration.linux.kvm-libvirt-virtual-machines
name: kvm-libvirt-virtual-machines
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kvm, libvirt, virsh, qemu, qemu-kvm, virtual-machines, virt-install, virt-manager, libvirt-network, bridge-networking, qcow2, qemu-img, virtio, snapshots, live-migration, storage-pool, virsh-console, nested-virtualization, cockpit-machines, lpic-1, virtualisation, sysadmin, virsh-edit, virsh-snapshot, blockcommit]
level: practitioner
status: docs-checked
description: "Run VMs on Linux with KVM/QEMU and libvirt: host checks, virt-install from ISO or cloud image, bridged vs NAT networks, qcow2 pools and snapshots, virsh day-2 operations, console, live migration."
sources:
  - https://libvirt.org/docs.html
  - https://libvirt.org/manpages/virsh.html
  - https://libvirt.org/formatdomain.html
  - https://docs.kernel.org/virt/kvm/x86/running-nested-guests.html
  - https://github.com/virt-manager/virt-manager/blob/main/man/virt-install.rst
  - https://www.qemu.org/docs/master/system/images.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_virtualization/index
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# KVM/libvirt virtual machines — a hypervisor from the packages you already have

**Goal:** turn a Linux host into a VM host with libvirt, create VMs from ISOs or cloud
images, give them real network access, and manage them from the CLI.

## 1. Host
```bash
grep -cE 'vmx|svm' /proc/cpuinfo           # >0 = VT-x/AMD-V present (also enable in BIOS); nested: cat /sys/module/kvm_intel/parameters/nested
dnf install qemu-kvm libvirt virt-install virt-viewer guestfs-tools   # apt install qemu-system-x86 libvirt-daemon-system virtinst libguestfs-tools
systemctl enable --now libvirtd            # newer: modular virtqemud/virtnetworkd sockets
usermod -aG libvirt $USER                  # then re-login; talk to the system instance: export LIBVIRT_DEFAULT_URI=qemu:///system
virt-host-validate                         # PASS on KVM, cgroups, IOMMU (VFIO passthrough needs intel_iommu=on)
virsh nodeinfo; virsh capabilities | head
```
`qemu:///session` (per-user) VMs are fine for desktops but can't bridge; servers use `qemu:///system`.

## 2. Networking
```bash
virsh net-list --all; virsh net-start default; virsh net-autostart default   # NAT 192.168.122.0/24 via virbr0 + dnsmasq
```
Bridge for VMs on the LAN (NetworkManager host):
```bash
nmcli con add type bridge ifname br0 con-name br0 ipv4.method auto
nmcli con add type bridge-slave ifname eth0 master br0
nmcli con down eth0; nmcli con up br0      # do this on console/out-of-band: it drops the link briefly
```
Then `--network bridge=br0` at install. libvirt-side alternative: a `<forward mode='bridge'>`
network XML pointing at `br0`. Open vSwitch and
VLAN tagging: `<virtualport type='openvswitch'/>` + `<vlan><tag id='10'/></vlan>`.

## 3. Create VMs
```bash
# from ISO, text console install (RHEL/Fedora: add console=ttyS0 to the installer cmdline)
virt-install --name rocky9 --memory 4096 --vcpus 2 --os-variant rocky9 \
  --disk path=/var/lib/libvirt/images/rocky9.qcow2,size=40,format=qcow2,bus=virtio \
  --network bridge=br0,model=virtio --graphics none --console pty,target_type=serial \
  --location /var/lib/libvirt/images/Rocky-9-dvd.iso --extra-args "console=ttyS0 inst.ks=http://10.0.0.9/ks.cfg"
# from a cloud image (fast; needs cloud-init seed)
qemu-img create -f qcow2 -F qcow2 -b /var/lib/libvirt/images/base/ubuntu-24.04.img /var/lib/libvirt/images/web1.qcow2 40G
virt-install --name web1 --memory 2048 --vcpus 2 --os-variant ubuntu24.04 --import \
  --disk path=/var/lib/libvirt/images/web1.qcow2 --cloud-init user-data=user-data.yaml,network-config=network.yaml \
  --network bridge=br0 --graphics none --noautoconsole
osinfo-query os | grep -i rocky            # valid --os-variant values (drives virtio defaults)
```
- Always `bus=virtio` / `model=virtio` for Linux guests; Windows needs the virtio-win ISO drivers.
- Backing-file clones (`-b`) share the base read-only; `virt-clone` or `qemu-img convert -O qcow2`
  for a full copy. Never modify the base image afterwards.
- `--cpu host-passthrough` for max performance when you won't migrate; libvirt documents migrating a
  host-passthrough guest as dangerous unless both hosts are identical (hardware, QEMU, microcode, configuration).
  `host-model` is the usual choice for migratable guests.
- Secure Boot/UEFI guests: `--boot uefi` (OVMF); TPM: `--tpm emulator`.

## 4. Day 2 with virsh
```bash
virsh list --all; virsh start web1; virsh shutdown web1; virsh destroy web1 (power-off); virsh autostart web1
virsh console web1                           # exit with Ctrl+]  (guest needs a getty on ttyS0)
virsh domifaddr web1; virsh net-dhcp-leases default
virsh dominfo web1; virsh domblklist web1; virsh domstats web1 --cpu-total --balloon
virsh setmem web1 4G --live; virsh setvcpus web1 4 --live   # within <maxMemory>/<vcpu> max; use --config too to persist
virsh edit web1                              # XML; validates on save
virsh attach-disk web1 /var/lib/libvirt/images/data.qcow2 vdb --driver qemu --subdriver qcow2 --persistent
virsh blockresize web1 vda 60G               # then grow the partition/fs inside
virsh snapshot-create-as web1 pre-upgrade --disk-only --atomic --quiesce   # external disk-only snapshot; --quiesce asks the guest agent to freeze filesystems
virsh snapshot-list web1; virsh snapshot-revert web1 pre-upgrade  # see the snapshot-revert section of the virsh manual for what your libvirt version can revert
virsh blockcommit web1 vda --active --pivot  # merge external snapshot back into base
virsh dumpxml web1 > web1.xml; virsh define web1.xml   # backup/restore definition
virsh undefine web1 --remove-all-storage --nvram
```
Storage pools: `virsh pool-list; virsh pool-define-as data dir --target /srv/vmimages; virsh pool-build data; virsh pool-start data; virsh pool-autostart data`.
`qemu-img info --backing-chain x.qcow2`, `qemu-img check -r all x.qcow2`, `virt-sparsify --in-place x.qcow2`.
Guest tools: `qemu-guest-agent` inside → `virsh domfsfreeze` for consistent snapshots, `virsh domifaddr --source agent`.

## 5. Migration and performance
```bash
virsh migrate --live --persistent --undefinesource web1 qemu+ssh://host2/system   # shared storage (NFS/Ceph/iSCSI) or --copy-storage-all
```
Both hosts need the same bridge names, CPU compatibility (`host-model`) and libvirt user SSH.
Performance: hugepages (`<memoryBacking><hugepages/>`), the disk `<driver>` `cache` and `io` attributes
tuned for shared storage, CPU pinning (`virsh vcpupin`) for
latency-sensitive guests, `virtio-net` multiqueue (`queues` on the interface `<driver>`). libvirt adds a virtio memballoon device
automatically for KVM guests; set `<memory>`=`<currentMemory>` on databases. Nested KVM on x86: the `nested`
parameter is on by default since kernel 4.20; to set it, put `options kvm-intel nested=y` in modprobe.d.

## Failure modes
- "Permission denied" on an image: the SELinux label or the QEMU user's directory access; keep images in a libvirt pool so libvirt manages labels.
- VM has no network on bridge: host firewall rules on the bridge, or the switch port blocks unknown MACs.
- Guest hangs or crashes after migrating with `host-passthrough`: the hosts differ; use `host-model` or a named CPU model.
- Console shows nothing: guest missing `console=ttyS0` in its kernel cmdline / `serial-getty@ttyS0`.
- `virsh` sees nothing while `virt-manager` shows VMs: URI mismatch (session vs system).

## Verify
- [ ] `virt-host-validate` passes; a VM installs from the CLI and `virsh console` reaches a login prompt.
- [ ] The VM has a LAN IP via the bridge, pings out, and survives `virsh autostart` + host reboot.
- [ ] A disk-only snapshot, a change in the guest, and `blockcommit` back leaves one clean qcow2 (`qemu-img info --backing-chain`).

## Checked

Checked 2026-10-27 against libvirt master docs (virsh, virt-install, formatdomain, formatnetwork, daemons), virt-install man page, qemu-img docs and the Linux kernel nested-KVM doc. Confirmed: virsh options (--quiesce, --atomic, --nvram, --remove-all-storage, --undefinesource, --copy-storage-all, domifaddr --source agent, net-dhcp-leases, domfsfreeze, blockcommit --pivot, console escape ^]), virt-install --cloud-init user-data and network-config sub-options, --boot uefi, --tpm emulator, host-passthrough migration caveat, openvswitch virtualport, nested default since 4.20, modular daemons, qemu-img --backing-chain and check -r all. Removed or softened: the --tpm sub-option syntax, external-snapshot revert wording, Wi-Fi bridging note, SELinux, firewall and bridge-nf specifics, cache/io/discard values.

Method: documentation only; no commands were run.
