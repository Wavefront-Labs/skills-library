---
id: computing-software.networking-hardware-and-wireless.open-vswitch.libvirt-and-kvm
name: libvirt-and-kvm
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, libvirt, kvm, qemu, virtualport, tap, ovs-ifup, selinux, virtual-machines]
level: practitioner
status: docs-checked
description: "Attach libvirt and KVM virtual machines to an Open vSwitch bridge: virtualport type openvswitch in domain XML, or ifup and ifdown scripts for plain KVM tap devices."
sources:
  - https://docs.openvswitch.org/en/latest/howto/libvirt/
  - https://docs.openvswitch.org/en/latest/howto/kvm/
  - https://docs.openvswitch.org/en/latest/howto/selinux/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libvirt and KVM
libvirt domain XML:
```
<interface type='bridge'>
  <source bridge='ovsbr'/>
  <virtualport type='openvswitch'/>
</interface>
```
libvirt-managed NAT networks are not supported with OVS; use a bridge you created with `ovs-vsctl add-br ovsbr`.

Plain KVM with tap scripts. `/etc/ovs-ifup`:
```
#!/bin/sh
switch='br0'
ip link set $1 up
ovs-vsctl add-port ${switch} $1
```
with `/etc/ovs-ifdown` doing the matching `ovs-vsctl del-port`. Start the VM with `kvm ... -net nic -net tap,script=/etc/ovs-ifup,downscript=/etc/ovs-ifdown`.

SELinux checks if ovs-vswitchd is blocked (not every Permission denied is SELinux): `ps -AZ | grep ovs-vswitchd` shows its domain, `semodule -l | grep openvswitch` shows the loaded policy modules, and `grep "openvswitch_t" /var/log/audit/audit.log | audit2allow -M ovslocal` builds a local policy from denials.

Verify: after the VM boots, `ovs-vsctl show` lists the guest's vnet interface on the bridge; for the KVM case `ovs-dpctl show` and `ovs-ofctl show br0` list its tap device (for example tap0).

Gotcha: if a libvirt VM will not start, run libvirtd from a terminal or read the libvirt and Open vSwitch logs.

## Checked

2026-11-09. Confirmed against the Open vSwitch with Libvirt, with KVM and with SELinux how-to pages: bridge-type interface with virtualport openvswitch, no support for libvirt-managed networks such as NAT, ovs-ifup script and kvm tap options, SELinux diagnostic commands. Removed: the claim to make the scripts executable (not on the pages). Reworded: SELinux and verify lines to match the pages.
Method: documentation only; no commands were run.
