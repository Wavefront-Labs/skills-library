---
id: computing-software.networking-hardware-and-wireless.open-vswitch.vtep-emulator
name: vtep-emulator
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, vtep, vtep-ctl, ovs-vtep, hardware-vtep, logical-switch, vxlan, ovsdb]
level: sme
status: docs-checked
description: "Run the Open vSwitch VTEP emulator: create a vtep database, start ovs-vtep, and use vtep-ctl for a physical switch, logical switch bindings and manager."
sources:
  - https://docs.openvswitch.org/en/latest/howto/vtep/
  - http://www.openvswitch.org/support/dist-docs/vtep-ctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VTEP emulator
Create the VTEP database next to the OVS one, and run one ovsdb-server for both (`--remote=db:hardware_vtep,Global,managers` plus the `ovs.db` and `vtep.db` files):
`ovsdb-tool create /etc/openvswitch/vtep.db vtep/vtep.ovsschema`

Start the emulator for bridge `br0`:
`./ovs-vtep --log-file=/var/log/openvswitch/ovs-vtep.log --pidfile=/var/run/openvswitch/ovs-vtep.pid --detach br0`

Configure with vtep-ctl:
```
ovs-vsctl add-br br0
ovs-vsctl add-port br0 p0
vtep-ctl add-ps br0
vtep-ctl set Physical_Switch br0 tunnel_ips=10.2.2.1
vtep-ctl set-manager tcp:<CONTROLLER IP>:6640
# without a controller, simulate one:
vtep-ctl add-ls ls0
vtep-ctl bind-ls br0 p0 0 ls0
vtep-ctl set Logical_Switch ls0 tunnel_key=33
vtep-ctl add-mcast-remote ls0 unknown-dst 10.2.2.2
vtep-ctl add-ucast-remote ls0 00:11:22:33:44:55 10.2.2.3
```
`bind-ls physical-switch port vlan logical-switch` binds a port and VLAN to a logical switch; the controller (for example a network virtualization platform) then manages it over the manager connection.

Verify: `vtep-ctl list-bindings br0 p0` lists the logical switch binding.

Gotcha: ovs-vtep is a Python script that calls vtep-ctl and ovs-vsctl, so ovsdb-server and ovs-vswitchd must already be running. With the openvswitch-vtep Debian package the daemons start automatically and ovs-vtep is in /usr/share/openvswitch/scripts.

## Checked

2026-11-09. Confirmed against the How to Use the VTEP Emulator page and vtep-ctl(8): database creation, single ovsdb-server for both databases, ovs-vtep command, add-ps, tunnel_ips, set-manager, add-ls, bind-ls, tunnel_key, add-mcast-remote, add-ucast-remote, list-bindings. Removed: the vtep-ctl show verify step and the conf.db wording (neither is in the sources). Reworded: the command sequence follows the how-to order.
Method: documentation only; no commands were run.
