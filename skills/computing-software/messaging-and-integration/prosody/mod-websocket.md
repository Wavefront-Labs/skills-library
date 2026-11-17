---
id: computing-software.messaging-and-integration.prosody.mod-websocket
name: mod-websocket
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, websocket, web-clients, reverse-proxy, cors]
level: practitioner
status: docs-checked
description: "mod_websocket in Prosody: enabling it, default ws and wss endpoints on 5280/5281, cross_domain_websocket, and consider_websocket_secure behind a TLS proxy."
sources:
  - https://prosody.im/doc/modules/mod_websocket
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_websocket

Add `"websocket"` to `modules_enabled`. Default endpoints:

- `wss://example.com:5281/xmpp-websocket`
- `ws://example.com:5280/xmpp-websocket`

The path can be changed through the HTTP path configuration.

Options:

- `c2s_close_timeout` default 5.
- `cross_domain_websocket`: `true` allows all sites, or a list of origins.
- `consider_websocket_secure`: set true (global section) when a reverse proxy terminates TLS.

```lua
cross_domain_websocket = { "http://jabber.org", "http://prosody.im" }
consider_websocket_secure = true
```

Without `consider_websocket_secure`, Prosody sees a proxied connection as unencrypted and may disable some authentication mechanisms.

Verify: a web client connects to the wss URL, authenticates, and works through the proxy.

## Checked

2026-11-04. Read the mod_websocket page: the default ws and wss endpoints on 5280 and 5281 at /xmpp-websocket, cross_domain_websocket as true or a list, consider_websocket_secure in the global section, c2s_close_timeout default 5, and the insecure-connection reasoning all match. Nothing removed.

Method: documentation only; no commands were run.
