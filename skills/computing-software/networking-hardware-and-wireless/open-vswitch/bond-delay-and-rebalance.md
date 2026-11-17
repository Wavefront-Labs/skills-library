---
id: computing-software.networking-hardware-and-wireless.open-vswitch.bond-delay-and-rebalance
name: bond-delay-and-rebalance
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, bond-updelay, bond-downdelay, rebalance, bond-rebalance-interval, bonding]
level: advanced
status: docs-checked
description: "Tune Open vSwitch bond member enable/disable timing with bond_updelay and bond_downdelay and the SLB rebalance interval, and understand the rebalancing thresholds."
sources:
  - https://docs.openvswitch.org/en/latest/topics/bonding/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bond delay and rebalance
Port columns (milliseconds):
- `ovs-vsctl set port bond0 bond_updelay=1000`
- `ovs-vsctl set port bond0 bond_downdelay=200`

Semantics: a member is disabled if its carrier is down longer than `bond_downdelay`, and enabled if carrier is up longer than `bond_updelay`. If no members are enabled, the first member to regain carrier is enabled immediately. If STP is enabled on the physical switch, set updelay above its forwarding delay.

Rebalancing (SLB):
- `ovs-vsctl set port bond0 other_config:bond-rebalance-interval=10000`
- vswitchd rebalances every 10 seconds using bytes sent over roughly the past minute, weighting recent data more.
- A member is significantly more loaded only if it carries at least 1 Mbps more and at least 3% more than the least loaded.
- A hash moves only if the source member holds at least two hashes and the move reduces the load ratio by at least 0.1.

Gotchas:
- On disabling a member vswitchd sends RARP gratuitous learning packets for learned MACs.
- SLB learning delay can last up to 60 seconds if no gratuitous ARP arrives; a locked MAC entry ignores gratuitous ARP from an SLB bond for 5 seconds.

## Checked
2026-11-04. Confirmed against the Bonding topic page: updelay and downdelay semantics, immediate enable when no member is enabled, the STP forwarding delay advice, the 10 second rebalance, the 1 Mbps and 3% thresholds, the 0.1 ratio rule, RARP learning packets, the 60 second and 5 second timings. Removed because the page text did not confirm them: the 0 to 2147483647 range, the balance-tcp claim, the bond/show verify line and the bond/migrate gotcha.
Method: documentation only; no commands were run.
