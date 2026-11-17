---
id: computing-software.networking-hardware-and-wireless.open-vswitch.rspan-and-gre-mirror
name: rspan-and-gre-mirror
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, rspan, output-vlan, select-vlan, gre, mirror, erspan]
level: advanced
status: docs-checked
description: "Send Open vSwitch mirror traffic to a remote analyser: RSPAN with select-vlan and output-vlan, or a GRE tunnel port."
sources:
  - https://docs.openvswitch.org/en/latest/faq/configuration/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rspan and gre mirror
RSPAN: select a source VLAN and output to a target VLAN.
```
ovs-vsctl -- --id=@m create mirror name=m0 select-all=true select-vlan=10 output-vlan=15 -- set bridge br0 mirrors=@m
```
- `select_vlan` takes up to 4096 values in 0 to 4095 (comma-separated list; empty or omitted selects all VLANs); `output_vlan` is 1 to 4095. Mirroring to a VLAN replaces the original tag with `output_vlan`.
- Mirroring to a VLAN can disrupt networks with unmanaged switches. The FAQ says a GRE tunnel has fewer caveats and should generally be preferred.

Mirror to a GRE tunnel port:
```
ovs-vsctl add-port br0 gre0 -- set interface gre0 type=gre options:remote_ip=192.168.1.10 -- --id=@p get port gre0 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge br0 mirrors=@m
```
`output_port` may be any kind of port, for example a physical port (SPAN) or a GRE tunnel; it is reserved exclusively for mirroring and frames received on it are discarded. The FAQ also lists ERSPAN, IPv6 GRE, GTP-U and SRv6 tunnel types (tunnel option details in tunnel-interface-options).

Disable: `ovs-vsctl clear bridge br0 mirrors` (and `ovs-vsctl del-port br0 gre0` to remove the tunnel).

Gotcha: the Mirroring Destination columns (`output_port`, `output_vlan`) are mutually exclusive: exactly one must be non-empty.

## Checked
2026-11-09. Read in full: docs.openvswitch.org faq/configuration (RSPAN example, GRE mirror example, disable and del-port commands, VLAN-mirroring caveat, GRE preferred, ERSPAN/IPv6 GRE/GTP-U/SRv6 entries). Partial read of ovs-vswitchd.conf.db.5 Mirror table: select_vlan range, output_vlan range 1 to 4095, output_port semantics, mutual exclusivity. Removed: the verify step (not in the sources) and the claim that tunnel types are mirror outputs.
Method: documentation only; no commands were run.
