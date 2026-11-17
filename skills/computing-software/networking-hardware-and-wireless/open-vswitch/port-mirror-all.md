---
id: computing-software.networking-hardware-and-wireless.open-vswitch.port-mirror-all
name: port-mirror-all
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, port-mirror, mirror-select-all, mirror, span, select-src-port, select-dst-port, snaplen]
level: practitioner
status: docs-checked
description: "Mirror Open vSwitch traffic to a monitoring port by creating a Mirror record: select-all, select-src/dst ports, output-port, snaplen, and disabling the mirror."
sources:
  - https://docs.openvswitch.org/en/latest/faq/configuration/
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# port mirror all
FAQ SPAN example: br0 with eth0 and tap0 as trunk ports; all traffic in or out of eth0 or tap0 is also mirrored to tap1, and any traffic arriving on tap1 is dropped:
```
ovs-vsctl add-br br0
ovs-vsctl add-port br0 eth0
ovs-vsctl add-port br0 tap0
ovs-vsctl add-port br0 tap1 -- --id=@p get port tap1 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge br0 mirrors=@m
```
Select specific ports (ovs-vsctl(8) example; all ports exist on br0, and packets received on eth2 are ignored):
`ovs-vsctl -- set Bridge br0 mirrors=@m -- --id=@eth0 get Port eth0 -- --id=@eth1 get Port eth1 -- --id=@eth2 get Port eth2 -- --id=@m create Mirror name=mymirror select-dst-port=@eth0,@eth1 select-src-port=@eth0,@eth1 output-port=@eth2`

Mirror columns (a packet must enter or leave through a selected port and be in a selected VLAN):
- `select_all` (true = every packet arriving or departing on any port); `select_src_port` (arriving packets) and `select_dst_port` (departing packets); `select_vlan` (0 to 4095; empty = all VLANs).
- `filter`: ovs-fields(7) syntax, applied after the select columns; `in_port` is not supported (use `select_src_port`).
- Destination, exactly one non-empty: `output_port` (reserves that port exclusively for mirroring; frames received on it are discarded; may be a physical port or a GRE tunnel) or `output_vlan` (1 to 4095, RSPAN; mirroring to a VLAN can disrupt networks with unmanaged switches, and a GRE tunnel is generally preferred).
- `snaplen`: 14 to 65535; larger packets are truncated in the datapath; no truncation if omitted.
- A packet is mirrored to a given destination only once even if selected several ways.
- `statistics:tx_packets` and `tx_bytes` count mirrored traffic.

GRE destination (FAQ): create the tunnel port and use it as `output-port`, for example `set interface gre0 type=gre options:remote_ip=192.168.1.10`.

Disable: `ovs-vsctl clear bridge br0 mirrors`.

## Checked
2026-11-04. Confirmed against the configuration FAQ (SPAN, RSPAN, GRE mirror), ovs-vsctl(8) (Port Mirroring example) and ovs-vswitchd.conf.db(5) Mirror table. Removed the Verify line (`tcpdump`, `list mirror`) and the Gotcha, whose substance is now covered by the exclusive-output-port note; corrected `output_port`/`output_vlan` to exactly-one-must-be-set.
Method: documentation only; no commands were run.
