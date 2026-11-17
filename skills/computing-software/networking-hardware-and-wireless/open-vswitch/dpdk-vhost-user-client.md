---
id: computing-software.networking-hardware-and-wireless.open-vswitch.dpdk-vhost-user-client
name: dpdk-vhost-user-client
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, dpdk, vhost-user, dpdkvhostuserclient, qemu, virtio, vhost-server-path, hugepages, tx-retries]
level: advanced
status: docs-checked
description: "Connect QEMU VMs to Open vSwitch DPDK with dpdkvhostuserclient ports: vhost-server-path, tx-retries-max, IOMMU, QEMU hugepage and chardev args."
sources:
  - https://docs.openvswitch.org/en/latest/topics/dpdk/vhost-user/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vhost-user client ports
OVS acts as the client; QEMU creates the socket in server mode.

Port:
```
ovs-vsctl add-port br0 vhost-client-1 -- set Interface vhost-client-1 \
  type=dpdkvhostuserclient options:vhost-server-path=/path/to/vhost-client-1
```
Interface option: `options:tx-retries-max` (default 8, 0 to 32) sets retries when the virtqueue is full. Do not set `n_rxq`: the queue count follows the QEMU `queues=` setting once the virtio device connects. Global (Open_vSwitch `other_config`, default false, restart the daemon after changing): `vhost-iommu-support` and `vhost-postcopy-support` (experimental). Requires QEMU 2.7 or later.

QEMU needs shared hugepage memory and a server chardev:
```
-object memory-backend-file,id=mem,size=4096M,mem-path=/dev/hugepages,share=on
-numa node,memdev=mem -mem-prealloc
-chardev socket,id=char1,path=/path/to/vhost-client-1,server
-netdev type=vhost-user,id=mynet1,chardev=char1,vhostforce,queues=2
-device virtio-net-pci,mac=00:00:00:00:00:01,netdev=mynet1,mq=on,vectors=6,mrg_rxbuf=on
```
vectors = queues * 2 + 2.

Gotcha: use at least two PMDs with multiqueue, otherwise traffic goes to one vhost queue. If the port is not yet configured in OVS, QEMU waits for the connection, and ports reconnect automatically after an OVS restart.

## Checked
2026-11-09. Read in full: docs.openvswitch.org topics/dpdk/vhost-user (client type, vhost-server-path, QEMU chardev with server, hugepage memory-backend-file with share=on, queues and vectors = q*2+2, tx-retries-max, iommu and postcopy settings, QEMU 2.7 requirement). Removed: statistics:ovs_tx_retries, the link_state verify step and the share=on failure claim (not stated); dropped the unused conf.db source.
Method: documentation only; no commands were run.
