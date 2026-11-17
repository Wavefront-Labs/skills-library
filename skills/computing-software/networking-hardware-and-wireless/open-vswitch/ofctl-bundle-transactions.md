---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-bundle-transactions
name: ofctl-bundle-transactions
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, bundle, replace-flows, diff-flows, atomic, ovs-ofctl, readd]
level: advanced
status: docs-checked
description: "Apply flow, group and packet-out changes atomically with ovs-ofctl bundle and --bundle, reload a flow file with replace-flows, and compare tables with diff-flows."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - https://docs.openvswitch.org/en/latest/tutorials/faucet/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl bundle transactions
Syntax (ovs-ofctl(8)):
```
ovs-ofctl bundle switch file
ovs-ofctl [--bundle] add-flow switch - < file
ovs-ofctl [--bundle] [--readd] replace-flows switch file
ovs-ofctl diff-flows source1 source2
```
`bundle switch file` executes all flow and group mods in the file as a single atomic transaction against the switch's tables, in the order listed. Each line is a flow mod, group mod or packet-out preceded by the keyword `flow`, `group` or `packet-out`.
- `flow` may be followed by `add`, `modify`, `modify_strict`, `delete`, `delete_strict` (add if bare).
- `group` may be followed by `add`, `modify`, `add_or_mod`, `delete`, `insert_bucket`, `remove_bucket` (add if bare).
- Packet-out lines use the Packet-Out Syntax (`in_port` and `packet` required, `actions` optional; omitted actions mean drop).

The `--bundle` option (OpenFlow 1.4 atomic bundle) can be put on the flow and group table commands (add-flow, add-flows, mod-flows, del-flows, replace-flows, add-group and the other group commands). If one flow mod fails, none are applied, and each packet sees the tables either before or after the whole bundle. Bundles require OpenFlow 1.4 or higher; an explicit `-O OpenFlow14` is not needed, but you may need to enable OpenFlow 1.4 in the bridge `protocols` column (see openflow-versions).

`replace-flows switch file` (file or `-` for stdin) reads flows, queries the switch, then adds missing flows, deletes flows not in the file and updates flows whose actions, cookie or timeouts differ. With `--readd` it adds all flows from the file even if identical; in OpenFlow 1.0 and 1.1 a re-add always resets counters, and in 1.2 and later only with the `reset_counts` flag.

`diff-flows source1 source2` prints a flow only in source1 preceded by `-`, one only in source2 preceded by `+`, and both versions of a flow whose actions, cookie or timeouts differ. Each source is a file or a switch: a name beginning with `/` or `.` is a file, a name containing `:` is a switch, otherwise it is a file if one exists, else a switch. Exit status 0 means no differences, 1 an error, 2 differences found.

The Faucet tutorial defines helper functions that snapshot with `ovs-ofctl -OOpenFlow13 --no-names --sort dump-flows br0 > flows1` style output and then run `ovs-ofctl -OOpenFlow13 diff-flows flows1 br0`.

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (OpenFlow Switch Bundle Command, flow table commands, `diff-flows`, `--bundle`, Packet-Out Syntax) and the Faucet tutorial helpers. Removed the Verify line and extended `diff-flows` and `replace-flows` details from the page; the Faucet snapshot command is described as the tutorial's helper rather than the exact command.
Method: documentation only; no commands were run.
