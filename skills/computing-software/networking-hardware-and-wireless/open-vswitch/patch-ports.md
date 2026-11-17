---
id: computing-software.networking-hardware-and-wireless.open-vswitch.patch-ports
name: patch-ports
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, patch-port, peer, bridge, interface-type]
level: practitioner
status: docs-checked
description: "Connect two Open vSwitch bridges directly with a pair of patch interfaces using type=patch and options:peer, with the requirement that each side names the other."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# patch ports
Patch ports are mainly a way to connect otherwise independent bridges, like a patch cable between two physical switches. The effect is conceptually similar to plugging the two ends of a Linux veth device into the switches, but patch ports are much more efficient.

Interface `type=patch` takes `options:peer`, the name of the Interface on the other side. The peer's own `peer` option must name this interface: the two patch interfaces must have reversed name and peer values. Create both in one command:
```
ovs-vsctl add-port br0 patch-to-int -- set Interface patch-to-int type=patch options:peer=patch-to-phy
ovs-vsctl add-port br-int patch-to-phy -- set Interface patch-to-phy type=patch options:peer=patch-to-int
```
Chaining with `--` puts both ends in one transaction (see vsctl-transactions-and-create); the page's own example does it as a single command.

Limits:
- Patch ports may connect two different bridges (the usual case) or the same bridge; in the latter case take special care to avoid loops, for example with OpenFlow flows.
- Patch ports do not work if the ends are on bridges in different datapaths, for example system and netdev.
- `ofport_request` on an Interface (1 to 65279) asks for a specific OpenFlow port number.

## Checked
2026-11-04. Confirmed against ovs-vswitchd.conf.db(5) (Interface table: Patch Options, `options:peer`, `ofport_request` range). Removed the Verify claims that `ofport` is not -1 once the peer exists and that the link does not come up without the reverse peer (page only states the reversed-values requirement).
Method: documentation only; no commands were run.
