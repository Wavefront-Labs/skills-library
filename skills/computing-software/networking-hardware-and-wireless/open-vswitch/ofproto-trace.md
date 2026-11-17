---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofproto-trace
name: ofproto-trace
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ofproto-trace, trace, debugging, ovs-appctl, packet-trace, troubleshooting, ct-next]
level: practitioner
status: docs-checked
description: "Trace how a bridge would process a packet with ovs-appctl ofproto/trace: flow syntax, reading the output, --generate for learn, --ct-next for conntrack, and trace-packet-out."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/
  - https://docs.openvswitch.org/en/latest/topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofproto/trace
Traces the path of an imaginary packet through the switch and reports the path it took (ovs-vswitchd(8), OFPROTO COMMANDS):
```
ovs-appctl ofproto/trace [options] [dpname] odp_flow [packet]
ovs-appctl ofproto/trace [options] bridge br_flow [packet]
ovs-appctl ofproto/trace-packet-out [options] [dpname] odp_flow [packet] actions
ovs-appctl ofproto/trace-packet-out [options] bridge br_flow [packet] actions
```
- `ofproto/trace` looks the packet up in the OpenFlow flow table as if it had arrived on an OpenFlow port; `ofproto/trace-packet-out` applies the given OpenFlow actions as if in an OpenFlow packet-out request.
- `bridge br_flow`: flow in a form similar to ovs-ofctl add-flow (never with wildcards); `bridge` names the bridge. `ofproto/list` lists valid ofproto names.
- `dpname odp_flow`: flow in the form printed by `ovs-dpctl dump-flows`; `dpname` can be omitted unless bridges have different types (such as ovs-netdev and ovs-system). `in_port` is the kernel datapath port number in this form and the OpenFlow port number in the bridge form; the two numberings usually differ.

Example from the advanced tutorial: `ovs-appctl ofproto/trace br0 in_port=1,dl_dst=01:80:c2:00:00:05`. The output has the traced `Flow:`, then a `bridge("br0")` block listing for each table the matching flow with its priority and actions (a `resubmit(,1)` shows a second table lookup, and `No match.` is shown when nothing matches), then `Final flow`, `Megaflow` and `Datapath actions` lines. Unspecified fields default to zero.

Options:
- `--generate`: internally generate a packet from the flow and trace it. Generated packets for protocols with arbitrary L7 payloads carry 64 bytes of payload by default; `--l7-len length` changes this and `--l7 payload` sets it exactly (both accepted only with `--generate`).
- `--ct-next flags`: when the traced flow triggers conntrack actions, the forked pipeline is traced with these ct_state flags (comma- or space-separated: trk, new, est, rel, rpl, inv, dnat, snat). Unspecified, or fewer options than ct actions, the flags default to `trk,new`.
- `--consistent` (trace-packet-out only): reject actions inconsistent with the packet; automatically enabled when actions include something only OpenFlow 1.1+ supports (such as push_vlan).

Side effects: actions such as `normal` (MAC learning) and `learn` (changing OpenFlow tables) only take effect when a packet is specified, either with `--generate` or as an explicit hex `packet` (at least 28 hex digits; ovs-pcap(1) and ovs-tcpundump(1) help). Output actions are never executed. With an explicit packet, headers come from the packet and the flow should give only metadata: skb_priority, pkt_mark, ct_state, ct_zone, ct_mark, ct_label, tun_id, in_port.

If a trace needs parts of the packet not in the flow, it says it needs a packet; `--generate` does not fill this in, since it only builds the packet from the flow.

More page examples: `ofproto/trace br in_port=1,icmp,icmp_type=8,dl_dst=00:00:5E:00:53:01` (ICMP echo request), `ofproto/trace br in_port=1,arp,arp_op=1` (ARP request).

## Checked
2026-11-04. Confirmed against ovs-vswitchd(8) (ofproto/trace, trace-packet-out, options, side effects) and the advanced tutorial (output layout). Replaced the invented tcp/nw_src example with page examples, corrected `--l7 hex` to a payload accepted only with `--generate`, corrected the side-effects note (a packet is needed, not only `--generate`), and removed the Verify line and the "Resubmitted" wording, which are not on the page.
Method: documentation only; no commands were run.
