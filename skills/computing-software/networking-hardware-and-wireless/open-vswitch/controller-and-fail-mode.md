---
id: computing-software.networking-hardware-and-wireless.open-vswitch.controller-and-fail-mode
name: controller-and-fail-mode
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, set-controller, fail-mode, controller, in-band, out-of-band, datapath-id]
level: practitioner
status: docs-checked
description: "Point a bridge at an OpenFlow controller with set-controller, choose standalone or secure fail mode, set out-of-band mode, disable in-band rules and fix the datapath ID."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - https://docs.openvswitch.org/en/latest/faq/openflow/
  - https://docs.openvswitch.org/en/latest/tutorials/faucet/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# controller and fail mode
- `ovs-vsctl set-controller br0 tcp:127.0.0.1:6653` (targets: `ssl:host[:port]`, `tcp:host[:port]`, `unix:file`, `pssl:`, `ptcp:`, `punix:`; the port defaults to 6653; `ssl` and `pssl` need `--private-key`, `--certificate` and `--ca-cert`). `get-controller` and `del-controller` print or remove it.
- `ovs-vsctl set-fail-mode br0 secure|standalone`
  - `standalone` (also the behaviour if unset): when no message has come from the controller for three times the inactivity probe interval, ovs-vswitchd takes over flow setup and acts as an ordinary MAC-learning switch, and keeps retrying the controller.
  - `secure`: ovs-vswitchd does not set up flows on its own when the controller connection fails.
  - `get-fail-mode` / `del-fail-mode`.

In-band control: by default OVS assumes controllers are in-band and sets up hidden flows with priorities greater than 65535 so traffic can reach them. For controllers on localhost (127.0.0.1) or a separate network, configure out-of-band mode:
- `ovs-vsctl set controller br0 connection-mode=out-of-band` (column `connection_mode`: `in-band` or `out-of-band`)
- A configured manager (`set-manager`) also gets in-band rules by default; `ovs-vsctl set bridge br0 other-config:disable-in-band=true` disables in-band control entirely for the bridge.
- Show hidden flows: `ovs-appctl bridge/dump-flows br0`

Datapath ID: `ovs-vsctl set bridge br0 other-config:datapath-id=0123456789abcdef` (a `0x` prefix or exactly 16 hex digits; may not be all zero).

Controller columns: `inactivity_probe` (ms; 0 disables), `max_backoff` (at least 1000 ms), `controller_rate_limit` (at least 100 packets per second; unset means no limit), `role` (`master`, `other`, `slave`).

`ovs-appctl bridge/reconnect br0` makes the bridge drop all its controller connections and reconnect.

## Checked
2026-11-04. Confirmed against ovs-vsctl(8) (controller and fail-mode commands), ovs-vswitchd.conf.db(5) (Bridge and Controller tables), ovs-vswitchd(8) (`bridge/reconnect`, `bridge/dump-flows`) and the OVS FAQ (OpenFlow: in-band, hidden flows, disable-in-band). Removed the rationale about controllers seeing a new switch when ports change and the `ovs-ofctl show` verify step (not on the pages).
Method: documentation only; no commands were run.
