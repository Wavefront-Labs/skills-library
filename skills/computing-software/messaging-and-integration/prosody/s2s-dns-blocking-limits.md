---
id: computing-software.messaging-and-integration.prosody.s2s-dns-blocking-limits
name: s2s-dns-blocking-limits
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, s2s, srv, dns, anonymous, stanza-size]
level: practitioner
status: docs-checked
description: "Prosody s2s practicalities: port 5269, SRV records for custom ports or delegated hosts, disabling mod_s2s, allow_anonymous_s2s and s2s_stanza_size_limit."
sources:
  - https://prosody.im/doc/s2s
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# s2s DNS, blocking and limits

Port 5269 must be open in the firewall. DNS SRV records are needed when the user-facing domain (example.com) differs from the server host (xmpp.example.com) or when s2s uses a custom port.

Block s2s globally or per host:

```lua
modules_disabled = { "s2s" }
```

When anonymous authentication is enabled, anonymous users are blocked from outgoing s2s. `allow_anonymous_s2s = true` overrides this, but it is off by default and the page recommends leaving it off because of abuse risk.

Limit stanza size (bytes, not lower than 10000):

```lua
s2s_stanza_size_limit = 512 * 1000
```

Verify: `prosodyctl check dns` shows the SRV and address records match your config.

## Checked

2026-11-04. Read the Prosody s2s page and the prosodyctl page: port 5269, SRV records for a different host or custom port, modules_disabled = { "s2s" }, anonymous s2s blocking and allow_anonymous_s2s, s2s_stanza_size_limit in bytes with a 10000 minimum, and check dns matching DNS records to configured domains and ports all match. Nothing removed.

Method: documentation only; no commands were run.
