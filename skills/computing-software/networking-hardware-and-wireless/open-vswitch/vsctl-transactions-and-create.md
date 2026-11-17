---
id: computing-software.networking-hardware-and-wireless.open-vswitch.vsctl-transactions-and-create
name: vsctl-transactions-and-create
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, transactions, create-record, destroy, wait-until, ovs-vsctl, id]
level: practitioner
status: docs-checked
description: "Chain ovs-vsctl commands atomically with --, create records with --id=@name, wire them to parents, destroy QoS and Queue records, and wait-until a record exists."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vsctl transactions and create
All commands joined by `--` run as one atomic transaction. The first `--` is optional; per-command options go before the command name.

`ovs-vsctl add-br br0 -- add-port br0 eth0`

Creating records:
- `[--id=(@name|uuid)] create table column[:key]=value...` creates a record and prints its UUID.
- `@name` refers to a record created earlier in the same invocation.
- Records that nothing references are auto-deleted, except QoS and Queue. So a `create` needs a reference from the Open_vSwitch tree in the same invocation.

Example (QoS attached to a port):
`ovs-vsctl -- set port eth0 qos=@newqos -- --id=@newqos create qos type=linux-htb other-config:max-rate=1000000`

Removing:
- `ovs-vsctl [--if-exists] destroy table record...`; `--all destroy table` removes every record. Without `--if-exists` each record must exist.
- Destroy is only useful for QoS and Queue records; for other tables it is silently ignored because unreachable records are deleted automatically.

Synchronising: `wait-until table record [column[:key]=value]...` waits until the record exists and all conditions match. Place it at the start of the chain (`wait-until bridge br0 -- get bridge br0 datapath_id`) and add `--timeout=0` so ovs-vsctl does not give up after the default wait.

Gotcha: `--id` and `--if-exists` cannot be used together on `get`.

## Checked
2026-11-04. Confirmed against ovs-vsctl(8): atomic transaction with the optional first `--`, create syntax and @name references, the unreachable-record deletion rule and the QoS and Queue exception, the QoS attach example, destroy semantics and wait-until placement and timeout advice. Removed because the page did not confirm them: the mirror example with `get`, the `clear Port eth1 qos` detach step and the exact wording of the `--id` restriction beyond the `get` command.
Method: documentation only; no commands were run.
