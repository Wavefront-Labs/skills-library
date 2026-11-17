---
id: computing-software.networking-hardware-and-wireless.open-vswitch.conntrack-stateful-firewall
name: conntrack-stateful-firewall
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, conntrack, ct, ct-state, stateful-firewall, firewall, commit, connection-tracking]
level: advanced
status: docs-checked
description: "Build a stateful firewall in Open vSwitch with ct() and ct_state matching: send packets through conntrack, commit new connections, and allow established traffic only."
sources:
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# conntrack stateful firewall
The `ct` action (OVS 2.5+) is the recommended way to build firewalls for new deployments (ovs-actions(7)). Pattern: send untracked packets through `ct(table=N)`, which forks the pipeline and reinjects the tracked copy in table N with ct_state set; commit selected traffic; then match `ct_state` to allow established connections and deny new ones.

Firewall example from ovs-actions(7): allow new connections from port 1 to port 2, and only established traffic from port 2 to port 1:
```
table=0,priority=1,action=drop
table=0,priority=10,arp,action=normal
table=0,priority=100,ip,ct_state=-trk,action=ct(table=1)
table=1,in_port=1,ip,ct_state=+trk+new,action=ct(commit),2
table=1,in_port=1,ip,ct_state=+trk+est,action=2
table=1,in_port=2,ip,ct_state=+trk+new,action=drop
table=1,in_port=2,ip,ct_state=+trk+est,action=1
```

Tutorial flows (ports `veth_l0` and `veth_r0`, TCP only, all in table 0):
```
priority=50,ct_state=-trk,tcp,in_port=veth_l0 actions=ct(table=0)
priority=50,ct_state=+trk+new,tcp,in_port=veth_l0 actions=ct(commit),veth_r0
priority=50,ct_state=-trk,tcp,in_port=veth_r0 actions=ct(table=0)
priority=50,ct_state=+trk+est,tcp,in_port=veth_r0 actions=veth_l0
priority=50,ct_state=+trk+est,tcp,in_port=veth_l0 actions=veth_r0
```
The tutorial also has two priority-10 forwarding flows (`in_port=veth_l0 actions=veth_r0` and the reverse), which only apply to packets the priority-50 flows do not match. The `ct` action must be told where to resume (`table=`), otherwise the tracked copy is not reinjected. Key `ct()` arguments: `table=`, `commit`, `zone=`, `nat(...)` (see conntrack-nat-and-zones).

Behaviour notes from the tutorial: conntrack reports `est` once it sees bidirectional traffic, even before the third ACK of the handshake; packets that tear down the connection still match `+est`, since a connection that is or was established keeps matching `+est`. `ovs-appctl dpctl/dump-conntrack` is what the tutorial uses to show tracked entries after each packet.

## Checked
2026-11-04. Confirmed against the conntrack tutorial (flows, ct_state behaviour, dump-conntrack use) and ovs-actions(7) (ct action and firewall example). Replaced the unsourced `add-flows br0 flows.txt` instruction and the `priority=0,actions=drop` advice with the page's own firewall example, and removed the Verify and Gotcha lines.
Method: documentation only; no commands were run.
