---
id: computing-software.networking-hardware-and-wireless.open-vswitch.gre-tunnel-between-hosts
name: gre-tunnel-between-hosts
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, gre, tunneling, tunnel, remote-ip, overlay]
level: intro
status: docs-checked
description: "Connect VMs on two hosts over an Open vSwitch GRE tunnel with ovs-vsctl add-port and options:remote_ip, plus connectivity checks and the MTU caveat."
sources:
  - https://docs.openvswitch.org/en/latest/howto/tunneling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gre tunnel between hosts
The how-to uses two hosts, each with eth0 on the Transport Network (its IP is used to reach the other host) and eth1 on a Management Network. Do not add eth0 to the OVS bridge. Each VM appears as a tap device such as tap0.

host1:
```
ovs-vsctl add-br br0
ovs-vsctl add-port br0 tap0
ovs-vsctl add-port br0 tap1
ovs-vsctl add-port br0 gre0 -- set interface gre0 type=gre options:remote_ip=<IP of eth0 on host2>
```
host2 mirrors this, using the IP of eth0 on host1 as `remote_ip`. Only add the tap ports if the VMs are not attached to OVS automatically.

The page notes the same approach works for the other tunneling protocols OVS supports (see tunnel-interface-options). Depending on the protocol, the physical switches on the Transport Network may need configuration, for example an MTU adjustment.

Testing per the page: pings between any VMs should work, on the same host or across hosts. `ip route show` inside a VM should show only the subnets configured in the guest, not the hosts' subnets (use very different guest subnets to illustrate this).

Troubleshooting per the page:
- host1 and host2 need full connectivity over eth0, which may need extra IP routes or rules.
- gre0 on host1 must point to eth0 on host2, and gre0 on host2 to eth0 on host1.
- All VMs must be on the same subnet; this configuration has no IP routing.

## Checked
2026-11-04. Confirmed against the OVS how-to "Connecting VMs Using Tunnels". Removed the kernel-before-3.11 / Linux GRE module / dmesg and lsmod troubleshooting line, which is not on the page.
Method: documentation only; no commands were run.
