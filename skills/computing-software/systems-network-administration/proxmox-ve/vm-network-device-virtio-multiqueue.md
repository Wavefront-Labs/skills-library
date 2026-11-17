---
id: computing-software.systems-network-administration.proxmox-ve.vm-network-device-virtio-multiqueue
name: vm-network-device-virtio-multiqueue
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [net0, virtio-net, multiqueue, mtu, nic-model]
level: practitioner
status: docs-checked
description: "Configure VM network devices in Proxmox VE, choosing VirtIO, MTU and multiqueue settings."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A VM can have several NICs. Models: Intel E1000 (the default, emulates a gigabit card), VirtIO paravirtualized (use for maximum performance; the guest needs the driver), Realtek 8139 (100 Mbit, only for pre-2002 OSes) and vmxnet3 (only for VMs imported from other hypervisors). Each NIC gets a random MAC address.

In the default bridged mode, each virtual NIC is a tap device attached to a bridge, `vmbr0` by default, giving direct access to the LAN. NAT mode uses the QEMU user network stack with a built-in DHCP server on 10.0.2.0/24; it is much slower, for testing only, and available only via CLI or API.

```
qm set 100 --net0 virtio,bridge=vmbr0,tag=5,firewall=1
qm set 100 --net0 virtio,bridge=vmbr0,queues=4
```

MTU can be overridden per device for VirtIO NICs; leaving it empty or setting `mtu=1` inherits the bridge MTU.

Multiqueue lets the guest process packets on several vCPUs. Set `queues` to the vCPU count (sockets times cores) and tell the guest driver: `ethtool -L ens1 combined X` with X equal to the vCPU count. On Windows install the Red Hat VirtIO Ethernet adapter driver, enable Receive Side Scaling and set Maximum number of RSS Queues to the vCPU count. Values above one raise CPU load on host and guest as traffic grows, so use it only for busy routers, reverse proxies or HTTP servers with many connections.

You can also create a VM with no network device.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
