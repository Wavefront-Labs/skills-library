---
id: computing-software.cybersecurity-defensive.zeek.netcontrol-rules-and-plugins
name: netcontrol-rules-and-plugins
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, netcontrol-rule, netcontrol-plugins, openflow, rule-target]
level: advanced
status: docs-checked
description: "Build NetControl rules with NetControl::Rule, Entity, target and expiry, then pick a backend plugin: OpenFlow, Broker, acld, PacketFilter or debug."
sources: ["https://docs.zeek.org/en/current/frameworks/netcontrol.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# netcontrol rules and plugins

The high-level functions are built on the rule API: they convert arguments into a `NetControl::Rule` and call `NetControl::add_rule`. Types are defined in `base/frameworks/netcontrol/types.zeek`.

A rule has:

- a type: drop, modify, redirect or whitelist;
- a target: `NetControl::FORWARD` (affects packets traversing the network) or the monitor path (only packets sent to Zeek);
- an entity: address, connection, etc.;
- an optional timeout, a priority (higher overrides lower), and a location string;
- extra fields for some types, such as the port for redirects.

```
function our_drop_connection(c: conn_id, t: interval)
    {
    local e = NetControl::Entity($ty=NetControl::CONNECTION, $conn=c);
    local r = NetControl::Rule($ty=NetControl::DROP,
        $target=NetControl::FORWARD, $entity=e, $expire=t);
    NetControl::add_rule(r);
    }
```

Plugins shipped:

- **OpenFlow**: the most fully featured, for OpenFlow switches (`openflow.zeek`).
- **Broker**: sends commands over Broker so external programs can act (`broker.zeek`).
- **acld**: supports the acld daemon for several switches and routers.
- **PacketFilter**: uses Zeek's process-level packet filter; mostly a demonstration.
- **Debug**: prints actions.

Backends are Zeek scripts using a plugin API, so you can write your own.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
