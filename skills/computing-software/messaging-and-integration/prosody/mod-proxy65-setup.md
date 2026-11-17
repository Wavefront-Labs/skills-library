---
id: computing-software.messaging-and-integration.prosody.mod-proxy65-setup
name: mod-proxy65-setup
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, proxy65, xep-0065, file-transfer, component]
level: practitioner
status: docs-checked
description: "Set up mod_proxy65 in Prosody: the proxy Component, proxy65_address DNS requirement, proxy65_acl, and proxy65_ports 5000 plus proxy65_interfaces."
sources:
  - https://prosody.im/doc/modules/mod_proxy65
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_proxy65

XEP-0065 relay for file transfers between clients behind NAT or firewalls.

```lua
Component "proxy.example.com" "proxy65"
    proxy65_address = "xmpp.example.com"
    proxy65_acl = { "example.com", "theadmin@anotherdomain.com" }
    modules_disabled = { "s2s"; }
```

- `proxy65_address` (default nil, uses the component hostname) must resolve by A/AAAA record or be an IP; an existing server record works.
- `proxy65_acl` (default `{ }`): when set, only listed domains, bare JIDs or full JIDs may use it.
- Global only: `proxy65_ports` (default `{ 5000 }`), `proxy65_interfaces` (default `{ "*", "::" }`).

Clients find the proxy automatically if mod_disco is enabled.

Verify: a file transfer between two NATed clients completes through port 5000.

## Checked

2026-11-04. Read the mod_proxy65 page: XEP-0065 purpose, the Component line, proxy65_address (default nil, DNS A/AAAA or IP), proxy65_acl (default empty, domains, bare or full JIDs), proxy65_ports { 5000 } and proxy65_interfaces { "*", "::" } as global-only options, disabling s2s on the component, and automatic discovery with mod_disco all match. Nothing removed.

Method: documentation only; no commands were run.
