---
id: computing-software.networking-hardware-and-wireless.open-vswitch.bridge-and-port-basics
name: bridge-and-port-basics
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, bridge, add-br, add-port, del-br, list-ports, mtu-request]
level: intro
status: docs-checked
description: "Create and remove Open vSwitch bridges and ports with ovs-vsctl: add-br, add-port, del-port, list-ports, port-to-br, idempotent flags, and mtu_request on the internal port."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - https://docs.openvswitch.org/en/latest/faq/issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bridge and port basics
Core commands:
- `ovs-vsctl add-br br0` creates a bridge with no ports other than itself; without `--may-exist` a repeat is an error, with it the command does nothing if the real bridge exists.
- `ovs-vsctl add-port br0 eth0` creates a port from the network device of the same name. Extra `column[:key]=value` arguments set Port columns, for example `tag=9` makes an access port for VLAN 9.
- `ovs-vsctl del-port [br0] eth0` (bridge optional; if omitted the port is removed from whichever bridge holds it), `ovs-vsctl --if-exists del-br br0` (deletes the bridge and all its ports, and any fake bridges with it as parent).
- `ovs-vsctl list-ports br0` and `list-ifaces br0` do not include the local port; `ovs-vsctl port-to-br eth0` prints the bridge that contains the port.

Chain commands in one atomic transaction with `--`:
`ovs-vsctl add-br br0 -- add-port br0 eth0`

Fixed MTU on the bridge's internal port (by default OVS overrides the internal interface MTU to match the bridge minimum):
- `ovs-vsctl set int br0 mtu_request=1450`
- `ovs-vsctl set int br0 mtu_request=[]` restores the default behaviour.

Troubleshoot:
- `ovs-vsctl show` prints a brief overview of the database contents.
- If `ovs-vsctl list port` shows an `ofport` of -1 and `ovs-ofctl show br0` omits the port, OVS could not create it; check the ovs-vswitchd log (`/var/log/openvswitch/ovs-vswitchd.log` with Debian and Red Hat packaging).
- ovs-vsctl waits for ovs-vswitchd to reconfigure; if ovs-vswitchd is not running, use `--no-wait` or it will not exit.
- Two uplinks added to one bridge connected to the same physical switch loop traffic; use a bond or enable STP (FAQ).

## Checked
2026-11-04. Confirmed against ovs-vsctl(8) bridge and port commands and the OVS FAQ (Issues: loops, ofport -1, log path, mtu_request). Removed the "ofport -1 means creation failed" reading via `get Interface` as the FAQ uses `list port`, and tightened the loop warning to what the FAQ says.
Method: documentation only; no commands were run.
