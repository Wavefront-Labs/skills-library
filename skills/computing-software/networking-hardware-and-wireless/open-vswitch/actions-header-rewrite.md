---
id: computing-software.networking-hardware-and-wireless.open-vswitch.actions-header-rewrite
name: actions-header-rewrite
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, set-field, load, move, push-vlan, strip-vlan, mod-vlan-vid, mod-dl-dst, dec-ttl, set-tunnel, set-queue, header-rewrite]
level: practitioner
status: docs-checked
description: "Rewrite packet headers in Open vSwitch flows with set_field, load, move, push_vlan, pop_vlan, mod_dl and mod_nw actions, dec_ttl, set_tunnel and set_queue, and mind action order."
sources:
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/
  - https://docs.openvswitch.org/en/latest/faq/openflow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# actions: header rewrite
Common modify actions:
- `set_field:value[/mask]->dst` writes a field; `load:value->dst` writes a field or sub-range; `move:src->dst` copies between fields.
- `mod_dl_src:mac`, `mod_dl_dst:mac`, `mod_nw_src:ip`, `mod_nw_dst:ip`.
- `push_vlan:0x8100` (or `0x88a8`), `strip_vlan` / `pop_vlan`, `mod_vlan_vid:20`.
- `dec_ttl` decrements the IP TTL.
- `set_tunnel:id` / `set_tunnel64:id` set the tunnel key before output to a tunnel port.
- `set_queue:n` / `pop_queue` pick an egress queue (see linux-htb-qos-queues).
- `check_pkt_larger(1500)->reg0[0]` stores a size test result in a register bit.

Examples:
`ovs-ofctl add-flow br0 in_port=1,actions=mod_vlan_vid:20,output:2`
`ovs-ofctl add-flow br0 actions=mod_nw_src:1.2.3.4`

Verify: `ovs-appctl ofproto/trace` shows how ovs-vswitchd treats a packet.

Gotcha: order matters. Actions run in the order specified, so `output:1,mod_vlan_vid:456` outputs first and the VLAN change has no visible effect. Put header changes before the output.

## Checked
2026-11-04. Confirmed against the ovs-actions(7) page and the OpenFlow FAQ: set_field, load, move, mod_dl and mod_nw actions, push_vlan TPIDs, strip_vlan and pop_vlan as synonyms, dec_ttl, set_tunnel and set_tunnel64, set_queue and pop_queue, check_pkt_larger, and the action-order FAQ. Removed because the pages did not confirm them: the register load and resubmit example and the claim about what ofproto/trace prints.
Method: documentation only; no commands were run.
