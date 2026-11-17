---
id: computing-software.messaging-and-integration.prosody.changing-ports-interfaces
name: changing-ports-interfaces
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, ports, interfaces, local-interfaces, network-settings]
level: practitioner
status: docs-checked
description: "Override Prosody listening ports and addresses with *_ports, *_interfaces, interfaces, local_interfaces and network_settings, in the global section."
sources:
  - https://prosody.im/doc/ports
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing ports and interfaces

Replace `*` with the service name: `*_ports` and `*_interfaces`.

```lua
c2s_ports = { 5222, 5322 }  -- also listen on 5322
```

- Global `interfaces` restricts listening addresses; default is all.
- Private services use `local_interfaces`, default `::1` and `127.0.0.1`. A service-specific option such as `console_interfaces` wins over it.
- Network options are global-section only; they do not apply per virtual host.
- Multiplexing (several services on one port) disables the individual port options.
- Low-level tuning such as `read_timeout` and `tcp_backlog` goes in `network_settings`.

Verify: after `prosodyctl restart`, the new port accepts connections and the old one does not.

## Checked

2026-11-04. Read the Prosody port and network configuration page: global-section-only network options, *_ports and *_interfaces with the c2s_ports 5222, 5322 example, the global interfaces option, local_interfaces defaulting to ::1 and 127.0.0.1 with service options such as console_interfaces taking priority, multiplexing disabling the individual port options, and network_settings with read_timeout and tcp_backlog all match. Nothing removed.

Method: documentation only; no commands were run.
