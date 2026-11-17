---
id: computing-software.networking-hardware-and-wireless.juniper-junos.netconf
name: netconf
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, netconf, rpc, xml-api, netconf-over-ssh]
level: practitioner
status: draft
description: "Use Junos NETCONF over SSH (port 830) and the display xml rpc CLI filter to discover RPC calls."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NETCONF and the XML API
Goal: send structured RPCs to Junos.

```
set system services netconf ssh
set system services netconf rfc-compliant
```

```
user@host> show interfaces terse | display xml rpc
<rpc><get-interface-information><terse/></get-interface-information></rpc>
```

```
ssh -s -p 830 automation@192.0.2.1 netconf
```

- Any CLI command has an RPC; `| display xml` returns data, `| display xml rpc` shows the RPC name.
- `show configuration | display json` for JSON config; `load merge` with `format json` for JSON input (confirm on release).
- Sessions use `<lock>` on candidate, `<edit-config>`, `<commit>`.

Gotcha: port 830 may be blocked by an lo0 filter or SRX zone host-inbound; also NETCONF output differs when `rfc-compliant` is set. Test with one RPC before large pushes.

Operational tip: for scale, use ncclient or PyEZ rather than raw SSH, set a session timeout, and always release the candidate lock in a finally block to avoid blocking other administrators.

## Verify
- The hello from `ssh -s ... netconf` lists capabilities, and `<get-system-information/>` returns the hostname.
