---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-modify-delete-flows
name: ofctl-modify-delete-flows
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, mod-flows, del-flows, strict, cookie, ovs-ofctl, replace-flows]
level: practitioner
status: docs-checked
description: "Modify and delete OpenFlow flows with ovs-ofctl mod-flows and del-flows, the --strict flag, cookie/mask selection, and out_port/out_group/table filters."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl modify and delete flows
Syntax (ovs-ofctl(8)):
```
ovs-ofctl [--bundle] [--strict] mod-flows switch flow
ovs-ofctl [--bundle] [--strict] mod-flows switch - < file
ovs-ofctl [--bundle] del-flows switch
ovs-ofctl [--bundle] [--strict] del-flows switch [flow]
ovs-ofctl [--bundle] [--readd] replace-flows switch file
```
`mod-flows` modifies the actions of matching flows. With `--strict`, wildcards are not treated as active for matching purposes; for mod-flows and del-flows the priority must then match along with the rest of the flow. Without `--strict`, priority is only used if mod-flows creates a new flow: non-strict mod-flows does not match on priority and will not change the priority of existing flows.

`del-flows switch` with no flow deletes all flows; with a flow it deletes the matching ones.

Select by cookie with a mask (`cookie=value/mask`; a 1-bit must match exactly, a 0-bit is wildcarded; mask -1 matches exactly):
- `ovs-ofctl mod-flows br0 cookie=1,actions=normal` changes all flows' cookies to 1 and their actions to normal.
- `ovs-ofctl mod-flows br0 cookie=1/-1,cookie=2,actions=normal` updates cookies with value 1 to 2 and changes their actions to normal (the cookie field is given twice: once with a mask for matching, once without for the new value).
Cookie masks are accepted by del-flows, mod-flows, dump-flows and dump-aggregate.

Extra filters for dump-flows, dump-aggregate, del-flow and del-flows: `out_port=port` (matching flow must output to that port) and `out_group=group` (must name that group; OVS 2.5+, OpenFlow 1.1+). Use `table=N` to limit to one table, for example `ovs-ofctl del-flows br0 table=1`. Per the page, with OpenFlow 1.0 and no table given, non-strict commands apply to matching flows in all tables; OpenFlow 1.2 and later let only deletion commands operate on all tables.

Timeouts and flags (`idle_timeout`, `hard_timeout`, `importance`, `send_flow_rem`, `check_overlap`, `reset_counts`, `no_packet_counts`, `no_byte_counts`) affect only new flows; for mod-flows they matter only if it creates a flow.

`replace-flows` reads flows from a file (or stdin if `-`), then adds missing flows, deletes flows not in the file and updates flows whose actions, cookie or timeouts differ. `--readd` re-adds all of them.

`--bundle` executes the flow mods as an OpenFlow 1.4 atomic bundle transaction: if one fails, none is applied, and packets see the tables either before or after the whole bundle. Bundles require OpenFlow 1.4 or higher, which may need enabling through the bridge `protocols` column.

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (flow table commands, Flow Syntax, cookie, priority, options, `--strict`, `--bundle`). Removed the Verify line and the "everything including flows you did not install" gotcha (the page only says a bare `del-flows switch` deletes all flows), and corrected the `--strict` description, which the page states as wildcards not being active.
Method: documentation only; no commands were run.
