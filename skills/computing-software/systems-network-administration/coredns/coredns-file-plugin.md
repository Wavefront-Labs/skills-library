---
id: computing-software.systems-network-administration.coredns.coredns-file-plugin
name: coredns-file-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, file, zone-file, authoritative, dnssec]
level: practitioner
status: docs-checked
description: "Serve an authoritative RFC 1035 master zone file with the file plugin, with reload by SOA serial or mtime and fallthrough."
sources:
  - https://coredns.io/plugins/file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run CoreDNS as an old-style authoritative server.

Syntax:

```
file DBFILE [ZONES...] {
    reload DURATION
    reload_by_mtime
    fallthrough [ZONES...]
}
```

- DBFILE is read once at start. A relative path is prefixed with the root plugin path.
- ZONES defaults to the zones of the server block.
- `reload` is the interval for checking whether the SOA serial changed; default one minute; `0` means never scan.
- `reload_by_mtime` decides on file modification time rather than SOA serial change.
- `fallthrough` passes a zone match without a record to the next plugin.

If the zone file contains DNSSEC signatures, correct DNSSEC answers are returned. Only NSEC is supported, and you are responsible for re-signing the file (see the sign plugin).

Example with outgoing transfers:

```
example.org {
    file db.example.org
    transfer {
        to * 10.240.1.1
    }
}
```

Zone content uses RFC 1035 presentation format: `$ORIGIN example.org.`, an SOA record, NS records, then names such as `www IN A 127.0.0.1`.

For round-robin A and AAAA answers, see loadbalance. For outgoing transfers use the transfer plugin.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/file/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
