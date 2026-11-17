---
id: computing-software.networking-hardware-and-wireless.open-vswitch.vsctl-database-commands
name: vsctl-database-commands
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, vsctl-set, vsctl-find, vsctl-list, ovs-vsctl, database, columns]
level: practitioner
status: docs-checked
description: "Read and edit the Open vSwitch configuration database with ovs-vsctl list, find, get, set, add, remove and clear, including map keys, set values and find operators."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vsctl database commands
Value syntax:
- Table and column names are not case-sensitive and `-` and `_` are interchangeable; unique abbreviations are accepted (for example `n` identifies the NetFlow table). Record names need full names and correct capitalization.
- UUIDs can be abbreviated to their first 4 or more hex digits if unique within the table.
- Sets: values separated by spaces or a single comma; `[]` is the empty set. Maps: `key=value` pairs; `{}` is the empty map. Quote `other-config={0=x,1=y}` so the shell does not expand it.
- Integer ranges are inclusive and have a maximum size of 4096 elements.

Commands:
- `ovs-vsctl [--if-exists] [--columns=col,...] list Bridge [br0]` lists all records if none is given; columns are alphabetical unless `--columns` is used.
- `ovs-vsctl [--columns=col,...] find Port tag=9` (operators `=`, `!=`, `<`, `>`, `<=`, `>=`; set operators `{=}`, `{!=}`, `{<=}`, `{<}`, `{>=}`, `{>}`, plus `{in}` and `{not-in}` in OVS 2.16 and later; escape `<` and `>` from the shell)
- `ovs-vsctl get Interface eth0 ofport` (`column:key` selects a map key)
- `ovs-vsctl set Bridge br0 stp_enable=true`; `set Interface eth0 cfm_mpid=1`; map keys individually: `set Open_vSwitch . other_config:pmd-cpu-mask=0xc`
- `ovs-vsctl add Port eth1 trunks 10 20` (for a map column a key is required; an existing key is not replaced, use `set` for that)
- `ovs-vsctl remove Port eth1 trunks 20` (not an error if the value is absent)
- `ovs-vsctl clear Bridge br0 mirrors` (empty set or map; only for columns allowed to be empty)

`--if-exists` on `set`, `add`, `remove` and `clear` does nothing for a missing record; on `list` it ignores missing records; on `get` a missing record gives no output and a missing key a blank line. `--id` and `--if-exists` cannot be used together on `get`.

## Checked
2026-11-04. Confirmed against ovs-vsctl(8) Database Commands (Identifying Tables, Database Values, list, find, get, set, add, remove, clear). Removed the generic Verify line and reworded the `--if-exists` summary to match the page.
Method: documentation only; no commands were run.
