---
id: computing-software.systems-network-administration.coredns.coredns-tsig-plugin
name: coredns-tsig-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, tsig, authentication, zone-transfer, security]
level: advanced
status: docs-checked
description: "Define TSIG secrets, validate signed requests, sign responses and refuse unsigned queries by type or opcode with the tsig plugin."
sources:
  - https://coredns.io/plugins/tsig/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: require authenticated DNS requests.

tsig defines CoreDNS's TSIG keys, validates incoming signed requests and signs the responses. It does not sign outgoing requests; the plugins sending them must use the defined keys.

```
tsig [ZONE...] {
    secret NAME KEY
    secrets FILE
    require [QTYPE...]
    require_opcode [OPCODE...]
}
```

- `secret NAME KEY` defines a key; repeat for more. Secrets are global to the server instance, not only the enclosing zone.
- `secrets FILE` loads keys in named.conf format (`key "example." { secret "..."; };`). An algorithm entry is accepted but currently ignored.
- `require QTYPE...` makes requests of those types REFUSED if unsigned; `require all` and `require none` are valid. Default: nothing required.
- `require_opcode OPCODE...` does the same for QUERY, IQUERY, STATUS, NOTIFY or UPDATE, with `all` and `none`.
- ZONE defaults to the block's zones.

Known gaps: the secondary plugin does not sign its transfer requests, and transfer plugin NOTIFYs from CoreDNS are not TSIG signed. When the request zone matches the tsig zones, the TSIG record is always stripped, and forward proxies the request upstream without TSIG.

Typical use: require signed transfers for a zone, together with the transfer plugin:

```
example.zone {
    tsig {
        secret example.zone.key. <base64-key>
        require AXFR IXFR
    }
    transfer {
        to *
    }
}
```

## Checked

2026-11-08. Checked in full against the tsig plugin README. Syntax, require and require_opcode behaviour match; added the documented gaps (secondary does not sign, transfer NOTIFY unsigned, TSIG stripped, forward without TSIG).

Method: documentation only; no commands were run.
