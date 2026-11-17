---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-packet-out-and-monitor
name: ofctl-packet-out-and-monitor
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, packet-out, snoop, flow-monitor, monitor, ovs-ofctl, probe, ping]
level: advanced
status: docs-checked
description: "Inject packets with ovs-ofctl packet-out, watch OpenFlow messages with snoop, stream flow changes with monitor watch:, and test controller reachability with probe and ping."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl packet out and monitor
Synopsis (ovs-ofctl(8)):
```
ovs-ofctl packet-out switch packet-out
ovs-ofctl snoop switch
ovs-ofctl monitor switch [miss-len] [invalid_ttl] [watch:[spec...]]
ovs-ofctl probe target
ovs-ofctl ping target [n]
ovs-ofctl benchmark target n count
```
packet-out spec (field=value pairs separated by commas or white space; only the last instance of a field is honoured):
- `in_port=` required: any valid OpenFlow port number, or LOCAL, CONTROLLER, NONE.
- `packet=` required: hex string of the packet bytes.
- `actions=` optional, same syntax as flow actions, and must be last; omitted means drop.
- `pipeline_field=value` optional: tunnel fields and register fields from ovs-fields(7).

`bundle` files may also contain packet-out lines (see ofctl-bundle-transactions).

snoop: prints all OpenFlow messages sent to or received from the bridge's configured controller, by connecting to the bridge's `switch.snoop` Unix socket. With several controllers it follows one (a primary if there is one); if no controller is configured or it is disconnected, no traffic is sent and nothing is shown.

monitor: connects to the switch and prints all OpenFlow messages received. Without a nonzero `miss-len`, OVS does not send asynchronous messages to the client, so very little is printed. `invalid_ttl` requests packet-ins when TTL reaches zero on `dec_ttl`.

`watch:[spec...]` sends a Nicira flow monitor request so the switch reports flow table changes. Comma-separated spec: `!initial`, `!add`, `!delete`, `!modify`, `!own`, `!actions`, `table=` (0 to 254, or name), `out_port=`, `out_group=` (needs OpenFlow 1.4, `-OOpenFlow14`), and `field=value` (any dump-flows match syntax). Useful for observing how a controller updates flow tables.

probe: sends one OpenFlow echo request to `target` and waits; with `-t`/`--timeout` it tests whether a switch or controller is up. `ping target [n]` sends 10 echo requests with n bytes of random payload (default 64) and times each reply. `benchmark target n count` reports total round-trip time.

Runtime commands (sent with ovs-appctl to a running ovs-ofctl): `exit` and `ofctl/set-output-file file` (monitor or snoop only), `ofctl/send ofmsg...`, `ofctl/packet-out packet-out`, `ofctl/barrier` (useful only for monitor).

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (monitor, snoop, probe/ping/benchmark, Packet-Out Syntax, runtime management commands). Removed the Verify line and the sentence claiming the flow monitor needs OpenFlow 1.4 on the bridge (only `out_group=` is documented as needing 1.4), and the "Example shape" command that is not on the page.
Method: documentation only; no commands were run.
