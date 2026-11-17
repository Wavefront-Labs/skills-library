---
id: computing-software.networking-hardware-and-wireless.bind9.server-block
name: server-block
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, server-block, bogus, edns]
level: practitioner
status: docs-checked
description: "Use the BIND 9 server block to set per-remote-server behaviour: bogus, edns, tcp-only, padding, keys, transfers."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# server block
A `server` block overrides behaviour for one remote address or prefix.

```
server 192.0.2.1 {
    bogus no;
    edns no;
    keys { host1-host2.; };
};
```

Options: `bogus` (never query this server), `edns`, `edns-version`, `padding`, `tcp-only`, `tcp-keepalive`, `transfers` (per-server cap that overrides `transfers-per-ns`), `request-ixfr`, and `keys` (a TSIG key for traffic with that server; only one key). Per-server settings override `options` and `view` values.

## Checked

2026-11-04. Read the server Block Definition in the Administrator Reference Manual: option list, bogus, edns, edns-version, padding, tcp-only, tcp-keepalive, transfers, keys (single key) and the override list confirmed. Nothing was removed.

Method: documentation only; no commands were run.
