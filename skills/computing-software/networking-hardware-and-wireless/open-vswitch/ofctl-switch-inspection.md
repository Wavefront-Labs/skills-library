---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-switch-inspection
name: ofctl-switch-inspection
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, dump-ports, dump-tables, ofport, ofport-request, dump-aggregate, ovs-ofctl, show]
level: intro
status: docs-checked
description: "Inspect an Open vSwitch bridge with ovs-ofctl show, dump-ports, dump-ports-desc, dump-tables, dump-aggregate, queue-stats, and pin port numbers with ofport_request."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - https://docs.openvswitch.org/en/latest/faq/openflow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl switch inspection
Commands (each takes the bridge as `switch`; ovs-ofctl(8)):
```
ovs-ofctl show switch
ovs-ofctl dump-tables switch
ovs-ofctl dump-ports switch [netdev]
ovs-ofctl dump-ports-desc switch [port]
ovs-ofctl dump-aggregate switch [flows]
ovs-ofctl queue-stats switch [port [queue]]
```
- `show`: information on the switch, including its flow tables and ports (also the fragment handling mode and the configuration `mod-port` changes).
- `dump-tables`: statistics for each flow table. `dump-table-features` and `dump-table-desc` (OpenFlow 1.4+) show features and configuration.
- `dump-ports`: statistics for network devices; `netdev` can be an OpenFlow port number or a device name such as eth0.
- `dump-ports-desc`: detailed port information, a subset of `show`. Only OpenFlow 1.5 and later can dump a specific port; earlier versions always dump all.
- `dump-aggregate`: aggregate statistics for flows matching `flows` (all flows if omitted).
- `queue-stats`: port can be a port number or name, `LOCAL` or `ALL`; queue and port may be omitted.
- `mod-port switch port action`: `up`/`down`, `stp`/`no-stp`, `receive`/`no-receive`, `forward`/`no-forward`, `flood`/`no-flood`, `packet-in`/`no-packet-in`.

OpenFlow port numbers: `ovs-vsctl get Interface eth0 ofport` returns one (the FAQ also shows `ovs-vsctl -- --columns=name,ofport list Interface`, which mixes all bridges). In the database `-1` means the interface could not be created (the Interface `error` column and the log say why); `[]` means it has not been created yet, normally intermittent unless ovs-vswitchd is not running.

Stable port numbers for flow rules: `ovs-vsctl add-port br0 p1 -- set interface p1 ofport_request=1`. `ofport_request` is 1 to 65279; if the number is taken or unset, OVS assigns a free one, limiting automatic assignment to 1 through 32767, so controllers can use 32768 and up. The OpenFlow local port is 65534. Setting `ofport_request` later changes the number, shown over OpenFlow as a port deletion followed by an addition.

Names: `--names` / `--no-names` control whether ports and tables are accepted and displayed by name (default: names shown only on an interactive console); names with special characters may be double-quoted; OpenFlow limits port names to 15 bytes and table names to 32 bytes.

By default only OpenFlow 1.0 is enabled in ovs-ofctl; use `-O` (for example `-O OpenFlow13`) for later versions, and note that commands such as dump-table-desc and group or meter commands need them.

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (OpenFlow Switch Management Commands, `--names`, `-O`), ovs-vswitchd.conf.db(5) (OpenFlow Port Number, `ofport`, `ofport_request`) and the OpenFlow FAQ (ofport values). Removed the unsourced "extended port statistics need OpenFlow 1.4" line and the Verify line.
Method: documentation only; no commands were run.
