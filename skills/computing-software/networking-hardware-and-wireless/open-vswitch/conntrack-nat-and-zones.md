---
id: computing-software.networking-hardware-and-wireless.open-vswitch.conntrack-nat-and-zones
name: conntrack-nat-and-zones
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, nat, conntrack, ct-zone, ct-mark, ct-label, snat, dnat, alg, ct-clear]
level: advanced
status: docs-checked
description: "Use NAT, zones, marks, labels and ALGs with the Open vSwitch ct() action: nat(src|dst), zone=, exec(set_field ct_mark), alg=ftp, ct_clear, and matching ct_zone and ct_mark."
sources:
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# conntrack NAT and zones
Syntax (ovs-actions(7)): `ct([argument]...)` or `ct(commit[,argument]...)`.

Arguments valid in both modes:
- `zone=value`: a 16-bit id that isolates connections into separate domains, allowing overlapping addresses in different zones; default 0. The value is a 16-bit literal or a field or subfield (the tutorial also shows `zone=src[start..end]`).

Without `commit` the packet is sent through the connection tracker and the pipeline forks: one fork reinjects the packet with ct_state, ct_zone, ct_mark, ct_label and the original-direction tuple fields initialised (ct_mark and ct_label are zero for a new connection); the other fork continues with all connection tracking metadata cleared. Extra arguments in this mode: `table=` (0 to 254 or a table name; if absent the packet is not reinjected) and `nat`.

`nat(type=addrs[:ports][,flag]...)`: `type` is `src` (SNAT) or `dst` (DNAT). `addrs` is one address or a range `addr1-addr2` (IPv6 must be bracketed if a port range is also given); `ports` is a port or `port1-port2` range (with a range there is no fallback to ephemeral ports). Flags: `random` (fresh random port; exclusive with `hash`), `hash` (port from a datapath-specific hash), `persistent` (address selection stable across restarts). Setting up translation for a new connection takes effect only if the connection is later committed with `ct(commit ...)`. A bare `nat` only translates the packet the way the connection was set up by an earlier committed ct; `nat(src|dst)` on an established connection behaves like bare `nat`. Special case: `nat(src=0.0.0.0)` translates the source port to an ephemeral port only if a collision is detected, and otherwise does no SNAT. Introduced in OVS 2.6; Linux 4.6 was the first upstream kernel with ct nat support.

Options with `commit` (commit stores the connection beyond the packet's lifetime and should be used from the first fork of ct without commit):
- `force`: if a committed connection is in the wrong direction for the current packet, terminate it and start a new one in the current direction.
- `exec(action...)`: only actions modifying ct_mark or ct_label are accepted: `set_field:value[/mask]->ct_mark` (32-bit) and `set_field:value[/mask]->ct_label` (128-bit). Later lookups populate ct_mark and ct_label for the connection.
- `alg=ftp` or `alg=tftp`: track negotiation of data connections for control connections; related connections get the `rel` ct_state flag and inherit ct_mark. With the Linux datapath, if sysctl `net.netfilter.nf_conntrack_helper` is enabled (the default until Linux 4.7), helpers may run even without `alg`; the netfilter team recommends disabling it. With `alg` and `nat(src|dst)` the datapath tries to make the helper NAT-aware, which is datapath specific. The FAQ advises setting `alg` anyway for FTP.

`ct_clear` (OVS 2.7): clears connection tracking state from the flow, zeroing ct_state, ct_zone, ct_mark and ct_label.

Match fields (tutorial): ct_state, ct_zone (set by the most recent ct action), ct_mark, ct_label, and the original-direction tuple ct_nw_src/ct_nw_dst, ct_ipv6_src/ct_ipv6_dst, ct_tp_src/ct_tp_dst. ct_state flags are written +flag or -flag, for example `ct_state=+trk+new`; the tutorial lists snat and dnat among the flags.

Example shape (composed from the syntax above, not a page example): source NAT on egress `ip,in_port=1 actions=ct(commit,nat(src=192.0.2.1),zone=1),output:2`, and return traffic through `ct(nat,table=1,zone=1)`. IP fragments passed to ct are reassembled within the zone, so fragments in different zones are not joined.

## Checked
2026-11-04. Confirmed against ovs-actions(7) (ct, nat, ct_clear) and the conntrack tutorial (fields, ct arguments). Corrected the claim that NAT needs commit on the first packet (it takes effect only when later committed), added `hash`/`random` meaning and the 0.0.0.0 special case, and removed the Verify line and the "same zone on both directions" gotcha, which the page does not state. The example is marked as composed.
Method: documentation only; no commands were run.
