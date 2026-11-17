---
id: computing-software.networking-hardware-and-wireless.open-vswitch.conntrack-inspect-and-limits
name: conntrack-inspect-and-limits
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, conntrack, dump-conntrack, flush-conntrack, ct-limits, ct-set-maxconns, ct-timeout-policy, ct-stats-show, ct-zone]
level: advanced
status: docs-checked
description: "Inspect and limit Open vSwitch conntrack: dpctl/dump-conntrack, flush-conntrack, ovs-ofctl ct-flush, ct-set-maxconns, ct-set-limits, ct-stats-show and CT_Zone timeouts."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# conntrack inspect and limits
Inspect and flush (ovs-appctl, ovs-vswitchd(8); each takes an optional `dp`):
- `dpctl/dump-conntrack [-m | --more] [-s | --statistics] [dp] [zone=zone]`: prints the connection entries in the tracker used by dp; `zone=` restricts to a zone, `--more` adds implementation-specific details, `--statistics` adds timeouts and timestamps. `dpctl/dump-conntrack-exp [dp] [zone=zone]` prints expectation entries (userspace datapath only).
- `dpctl/flush-conntrack [dp] [zone=zone] [ct-origin-tuple [ct-reply-tuple]]`: with no tuple, flushes all entries (or the zone's). With a tuple, flushes the matching entries in the zone (default zone 0); the tuple may be partial, and to give only a reply tuple pass an empty string as the origin tuple. The userspace tracker needs the original pre-NATed tuple, or a warning is logged. For ICMP, a partial tuple must include a source or destination IP. Example tuple: `"ct_nw_src=10.1.1.1,ct_nw_dst=10.1.1.2,ct_nw_proto=1,icmp_type=8,icmp_code=0,icmp_id=10"`.
- `ovs-ofctl ct-flush switch [zone=N] [mark=X[/M]] [labels=Y[/N]] [ct-orig-tuple [ct-reply-tuple]]` flushes through OpenFlow (mark and labels default to 0/0); `ct-flush-zone switch zone` flushes a zone (OVS 2.6+).
- `dpctl/ct-stats-show [dp] [zone=zone] [-m | --more]`: number of connections grouped by protocol (by state with `--more`). `dpctl/ct-bkts [dp] [gt=threshold]`: connections per conntrack bucket, only buckets over the threshold if given.

Limits (userspace datapath only unless noted):
- `dpctl/ct-set-maxconns [dp] maxconns` sets the maximum number of tracker entries; if already over, the limit is enforced once connections expire. `ct-get-maxconns` and `ct-get-nconns` print the limit and the current count.
- `dpctl/ct-set-limits [dp] [default=default_limit] [zone=zone,limit=limit]...` sets per-zone connection limits; the initial default is unlimited and 0 means unlimited. `ct-del-limits [dp] zone=zone[,zone]...` removes them; `ct-get-limits [dp] [zone=zone[,zone]...]` shows limits and current counts (always the default limit).
- `dpctl/ct-enable-tcp-seq-chk` / `ct-disable-tcp-seq-chk` (checking is on by default; disabling, including for TCP resets, is only for hardware offload), `ct-get-tcp-seq-chk`, `ct-set-sweep-interval [dp] ms` / `ct-get-sweep-interval`.
- `dpctl/ipf-set-enabled` / `ipf-set-disabled [dp] v4|v6` control fragment reassembly for the userspace tracker (both on by default); related `ipf-set-min-frag`, `ipf-set-max-nfrags`, `ipf-get-status`.

Database (ovs-vswitchd.conf.db(5)): the Datapath table's `ct_zones` column maps zone ids 0 to 65535 to `CT_Zone` rows (zone 0 is the default zone). A `CT_Zone` has `timeout_policy` (a `CT_Timeout_Policy`; default is the system policy) and `limit` (0 means unlimited; unset uses `ct_zone_default_limit`). `CT_Timeout_Policy.timeouts` maps keys such as icmp_first, icmp_reply, tcp_established, tcp_syn_sent, tcp_time_wait, udp_first, udp_single, udp_multiple to seconds-style integers (0 to 4,294,967,295).

Example from the page syntax: `ovs-appctl dpctl/ct-set-limits default=100000 zone=5,limit=2000`

Linux note: the kernel (system) datapaths share a single connection tracking table, also used by iptables, nftables and the host stack, so the dump and flush commands do not apply to one datapath specifically.

## Checked
2026-11-04. Confirmed against ovs-vswitchd(8) (conntrack dpctl commands), ovs-ofctl(8) (ct-flush, ct-flush-zone) and ovs-vswitchd.conf.db(5) (Datapath ct_zones, CT_Zone, CT_Timeout_Policy). Corrected `-m` (implementation details, not marks and labels), added the page's userspace-only scope and tuple rules, and removed the Verify line (it used wc, and nothing on the page says what ct-get-limits echoes beyond limits and counts).
Method: documentation only; no commands were run.
