---
id: computing-software.systems-network-administration.proxmox-ve.vm-numa-and-vcpu-hotplug
name: vm-numa-and-vcpu-hotplug
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [numa, hotplug, vcpus, hot-plug, udev]
level: advanced
status: docs-checked
description: "Enable NUMA emulation and vCPU or memory hot-plug on Proxmox VE VMs, with the guest-side udev rule."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Check whether the host is NUMA with `numactl --hardware | grep available`; more than one node means yes. On NUMA hosts enable the VM's NUMA option so resources are distributed properly, and set the VM's socket count to the host's NUMA node count. The NUMA option is also required to hot-plug cores or RAM.

vCPU hot-plug is a newer, complicated feature, so use it only when absolutely needed; resource limits (cpulimit, cpuunits) can replace most use cases. The maximum number of pluggable CPUs is always `cores * sockets`. Start with fewer using the `vcpus` setting:

```
qm set 100 --vcpus 2
```

Only Linux guests are supported, with a kernel newer than 3.10 (newer than 4.7 recommended). To bring hot-added CPUs online automatically, save this under `/etc/udev/rules.d/` in a file ending in `.rules`:

```
SUBSYSTEM=="cpu", ACTION=="add", TEST=="online", ATTR{online}=="0", ATTR{online}="1"
```

CPU hot-remove depends on the machine type and needs guest cooperation: the delete command is just a request forwarded to the guest OS through a mechanism such as ACPI, so removal is not guaranteed.

Hugepages and fine-grained NUMA topology are separate options in `qm.conf` (`hugepages`, `numaX`); consult the qm.conf options reference in the qm chapter before using them.

## Checked

2026-11-09. Compared with the NUMA and CPU hot-plug sections and the option reference of https://pve.proxmox.com/pve-docs/chapter-qm.html. The qm set --vcpus line is an illustrative command built from the documented vcpus option.

Method: documentation only; no commands were run.

