---
id: computing-software.networking-hardware-and-wireless.open-vswitch.sflow-setup
name: sflow-setup
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, sflow, sflow-collector, sampling, polling, header, agent]
level: practitioner
status: docs-checked
description: "Export Open vSwitch sFlow samples to a collector: create an sFlow record with agent, target, header, sampling and polling, attach it to a bridge, verify and remove it."
sources:
  - https://docs.openvswitch.org/en/latest/howto/sflow/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sflow setup
Variables, then create and attach in one transaction:
```
COLLECTOR_IP=10.0.0.1 COLLECTOR_PORT=6343 AGENT_IP=eth1 HEADER_BYTES=128 SAMPLING_N=64 POLLING_SECS=10
ovs-vsctl -- --id=@sflow create sflow agent=${AGENT_IP} target="\"${COLLECTOR_IP}:${COLLECTOR_PORT}\"" header=${HEADER_BYTES} sampling=${SAMPLING_N} polling=${POLLING_SECS} -- set bridge br0 sflow=@sflow
```
Record the printed UUID: removal is `ovs-vsctl remove bridge br0 sflow <UUID>`. For another bridge, repeat with its name.

sFlow table columns and defaults:
- `targets`: one or more `ip:port` strings (required).
- `agent`: IP or device name; derived from the first target and routing table if unset. If none can be determined, sFlow is disabled.
- `header`: bytes of each sampled packet, default 128.
- `sampling`: 1 in N packets, default 400.
- `polling`: seconds between port statistics, default 30.

Verify:
- `ovs-vsctl list sflow`
- `tcpdump -ni eth1 udp port 6343` should show datagrams leaving toward the collector.

Gotcha: the how-to passes the target with inner quotes (`"\"ip:port\""`); copy that form. The agent device (eth1 here) must be on the management network that reaches the collector; also check no firewall blocks UDP 6343 at the collector.

## Checked

2026-11-09. Confirmed against the Monitoring VM Traffic Using sFlow how-to and the sFlow table of ovs-vswitchd.conf.db(5): variables, create and attach command, UUID needed for removal, list sflow, tcpdump check, header default 128, sampling default 400, polling default 30, agent derivation and disabled case, targets as ip:port. Removed: the out-of-date cookbook remark and the string-set parsing explanation (not on the pages).
Method: documentation only; no commands were run.
