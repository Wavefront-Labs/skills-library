---
id: computing-software.messaging-and-integration.prosody.external-component-network
name: external-component-network
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, components, component-ports, security, tunnel]
level: practitioner
status: docs-checked
description: "Network settings for external Prosody components: component_ports 5347, component_interfaces local-only default, no encryption in XEP-0114, and tunnelling remote components."
sources:
  - https://prosody.im/doc/components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External component networking

Global options:

- `component_ports`: where Prosody accepts component connections. Default 5347; several components can share one port.
- `component_interfaces`: interfaces to listen on. Default is local only (127.0.0.1). Note the plural name.

```lua
component_ports = { 8888 }
component_interfaces = { "192.168.0.10" }
```

XEP-0114 defines no encryption for component connections, so `require_encryption` does not apply to them. If the component runs on a different machine, tunnel the connection with WireGuard, stunnel or spiped instead of widening `component_interfaces` to the internet.

Each external component authenticates with its `component_secret`; use a unique secret per component.

Verify: the external component connects on the configured port and its domain answers service discovery; from another host without a tunnel, the port is unreachable.

## Checked

2026-11-04. Read the Prosody components page: component_ports default 5347 with several components sharing a port, component_interfaces defaulting to local only (127.0.0.1), the 8888 and 192.168.0.10 example, no XEP-0114 encryption so require_encryption does not apply, and Wireguard, stunnel or spiped as the secure layer all match. component_secret per component is shown in the page's external component example; the unique-secret advice is practice, not a documented claim.

Method: documentation only; no commands were run.
