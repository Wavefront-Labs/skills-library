---
id: computing-software.cybersecurity-defensive.zeek.netcontrol-active-response
name: netcontrol-active-response
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, netcontrol, drop-address, shunt-flow, catch-and-release]
level: advanced
status: docs-checked
description: "NetControl active response: activate a backend, high-level drop, shunt, redirect, quarantine and whitelist calls, catch and release, netcontrol.log."
sources: ["https://docs.zeek.org/en/current/frameworks/netcontrol.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# netcontrol active response

NetControl gives Zeek a unified, task-oriented API to switches and firewalls. Rules go to one or more backends, each talking to one device, and their lifecycle (success, failure, timeout) is reported back to scripts. At least one backend must be active; the debug plugin prints actions to stdout:

```
event NetControl::init()
    {
    local debug_plugin = NetControl::create_debug(T);
    NetControl::activate(debug_plugin, 0);
    }

event connection_established(c: connection)
    {
    NetControl::drop_connection(c$id, 20 secs);
    }
```

High-level calls:

- `NetControl::drop_address`: block all packets for an IP.
- `NetControl::drop_connection`: block one connection by 5-tuple.
- `NetControl::drop_address_catch_release`: block briefly, then re-block longer when the address reappears, saving hardware rule space (see `policy/frameworks/netcontrol/catch-and-release.zeek`).
- `NetControl::shunt_flow`: stop forwarding a unidirectional flow to Zeek.
- `NetControl::redirect_flow`: redirect a unidirectional flow to another port.
- `NetControl::quarantine_host`: steer DNS to a special server that resolves everything to itself and shows a warning.
- `NetControl::whitelist_address` and `NetControl::whitelist_subnet`.

All actions are recorded in `netcontrol.log`, including NetControl::MESSAGE entries and rule states such as REQUESTED and SUCCEEDED.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
