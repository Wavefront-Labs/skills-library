---
id: computing-software.networking-hardware-and-wireless.open-vswitch.openflow-versions
name: openflow-versions
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, openflow, protocols, openflow13, openflow14, openflow15, ovs-ofctl]
level: practitioner
status: docs-checked
description: "Select OpenFlow versions in Open vSwitch: the bridge protocols column, ovs-ofctl -O, default OpenFlow 1.0 behaviour, and what 1.1 to 1.5 add."
sources:
  - https://docs.openvswitch.org/en/latest/topics/openflow/
  - https://docs.openvswitch.org/en/latest/faq/openflow/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openflow versions
Bridge side: the `protocols` column is a set of `OpenFlow10`, `OpenFlow11`, `OpenFlow12`, `OpenFlow13`, `OpenFlow14`, `OpenFlow15`; it lists the versions that may be used when negotiating a connection with a controller, and 1.0 to 1.5 are all enabled if the column is empty (ovs-vswitchd.conf.db(5)). FAQ examples:
```
ovs-vsctl set bridge br0 protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
ovs-vsctl set bridge br0 protocols=OpenFlow10
```
Client side: all current versions of ovs-ofctl enable only OpenFlow 1.0 by default; use `-O` (long form `--protocols=`) to allow later versions, which are generally supported but off by default for compatibility with older Open vSwitch (ovs-ofctl(8)):
`ovs-ofctl -O OpenFlow13 dump-flows br0`

Version support by release (FAQ table): 1.0 is always supported and enabled; 1.1 to 1.3 are enabled by default from OVS 2.3; 1.4 from 2.8; 1.5 is supported and enabled from 2.12. OVS 2.2 had an experimental, unsafe OpenFlow 1.4 that could cause crashes and should not be enabled.

OpenFlow topic page (a list of remaining work, not a feature matrix):
- 1.1 and 1.2 support is complete.
- 1.3 needs 1.2 plus optional items: IPv6 extension header handling, auxiliary connections, Provider Backbone Bridge tagging, on-demand flow counters.
- 1.4 and ONF 1.3.X Pack1 items still to do include flow entry notifications, flow entry eviction (table_mod eviction, flow_mod importance), vacancy events, table synchronisation, group and meter change notifications, the PBB UCA header field; optical port properties are 1.4 only.
- 1.5 and Pack2: time scheduled bundles; egress tables are 1.5 only.
- Port numbers: OpenFlow 1.0 has 16-bit and later versions 32-bit port numbers, but OVS support for later versions needs all port numbers in the 16-bit range.

Version-dependent commands and options (ovs-ofctl(8), ovs-actions(7)):
- Meter commands need OpenFlow 1.3 or later (see ofctl-meters).
- Dumping a single port with `dump-ports-desc` needs 1.5 or later; `importance` in flow_mod and table-full eviction via mod-table need 1.4 or later; table renaming with mod-table needs 1.3 or later and OVS 2.11.
- The `enqueue` action exists in OpenFlow 1.0 and was removed in OpenFlow 1.1.

## Checked
2026-11-04. Confirmed against the OpenFlow FAQ (version table, `protocols`, `-O`), the OpenFlow topic page, ovs-vswitchd.conf.db(5) and ovs-ofctl(8) (-O, version-gated options). Rewrote the support summary: the topic page lists unfinished work, so the earlier statements that 1.4 provides bundles and notifications and that 1.5 provides port properties were wrong. Removed the unsourced "DPDK extended stats need 1.4" claim and the Verify line.
Method: documentation only; no commands were run.
