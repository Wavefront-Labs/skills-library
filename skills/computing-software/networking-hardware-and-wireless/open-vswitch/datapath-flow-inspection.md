---
id: computing-software.networking-hardware-and-wireless.open-vswitch.datapath-flow-inspection
name: datapath-flow-inspection
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, datapath, dpctl, dump-flows, dpif, ovs-dpctl, ufid, megaflow, offloaded]
level: practitioner
status: docs-checked
description: "Inspect datapath flows in Open vSwitch with ovs-appctl dpif/show, dpif/dump-flows and dpctl/dump-flows filters, manage datapath flows with dpctl, and use ovs-dpctl directly."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-dpctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# datapath flow inspection
Datapath flows are not OpenFlow flow entries: they are different, considerably simpler flows maintained by the datapath module (kernel module for the Linux datapath). Use `ovs-ofctl dump-flows` for OpenFlow entries. Do not add, remove or modify datapath flows or datapaths while ovs-vswitchd is running, as it interferes with its own management; the dump commands are for debugging.

ovs-appctl (ovs-vswitchd(8)):
- `dpif/show`: summary of datapaths with statistics and connected ports, including OpenFlow port number, datapath port number and type (local port is OpenFlow port 65534). `dpctl/show [-s | --statistics] [dp...]` is the same without OpenFlow port numbers; `dpif/dump-dps` lists datapath names. The other dpif/ commands are redundant with dpctl/ and will be removed in a future release.
- `dpif/dump-flows [-m] dp` and `dpctl/dump-flows [-m | --more] [--names | --no-names] [dp] [filter=filter] [type=type] [pmd=pmd]`: without `-m` output omits entirely wildcarded match fields; with it all are shown.
  - `filter=` takes a flow in the form of ovs-ofctl add-flow (no wildcards); it also matches wildcarded datapath fields, for example `filter='tcp,tp_src=100'` matches the datapath flow `tcp(src=80/0xff00,dst=8080/0xff)`.
  - `pmd=` restricts to one PMD thread (`pmd=-1` is the main thread); userspace datapath only.
  - `type=` (only for `ovs-appctl dpctl/dump-flows`) is a comma-separated list of `ovs`, `tc`, `dpdk` (flows fully offloaded by dpdk), `offloaded` (to hardware), `non-offloaded`, `partially-offloaded`, `all`. Default is all types; ovs-dpctl always acts as type `ovs`.
- `dpctl/add-flow [dp] flow actions`, `dpctl/mod-flow [--clear] [--may-create] [-s | --statistics] [dp] flow actions`, `dpctl/del-flows [dp]` (all flows), `dpctl/add-flows | mod-flows | del-flows [dp] file`, `dpctl/get-flow [dp] ufid:ufid [-m | --more] [--names | --no-names]` (ufid is 32 hex characters). `dpif/del-flows dp` also deletes all flows.
- The flow and actions syntax for add-flow and mod-flow does not match ovs-ofctl; ovs-dpctl(8) examples: `ovs-dpctl add-flow myDP "in_port(1),eth(),eth_type(0x0806),arp()" 2`. `add-flow` succeeds only if the flow does not exist; `mod-flow` without `--may-create` only modifies an existing flow; `--clear` zeros statistics.
- `dp` is optional when exactly one datapath exists.

ovs-dpctl (ovs-dpctl(8)), run directly and not while ovs-vswitchd is in use (use ovs-vsctl then): datapath names are `[type@]name` (default provider `system`).
- `ovs-dpctl show [-s] [dp...]` prints datapaths and ports (local port is port 0) and, with `-s`, packet and byte counters. The "lookups" row gives hit, missed (needs userspace processing) and lost; "flows" is the flow count; "masks" gives megaflow mask stats (omitted if the datapath has no megaflow).
- `dump-dps`, `add-dp dp [netdev[,option]...]`, `del-dp dp` (removes its network devices), `add-if`, `set-if`, `del-if`, `dump-flows`, and the other flow commands above.

Typical use: compare `ovs-appctl ofproto/trace` (what should happen; see ofproto-trace) with datapath dumps (what is cached).

## Checked
2026-11-04. Confirmed against ovs-vswitchd(8) (DATAPATH DEBUGGING COMMANDS, dpctl/ commands) and ovs-dpctl(8) (datapath and flow commands, type values). Removed the `rmmod` advice, the `ovs-dpctl del-dp system@ovs-system` example and the idle-expiry gotcha (none on the pages), the Verify line, and corrected `-m` to show wildcarded fields rather than "more detail".
Method: documentation only; no commands were run.
