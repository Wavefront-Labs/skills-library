---
id: computing-software.systems-network-administration.pi-hole.dns-listening-modes
name: dns-listening-modes
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [listening-mode, open-resolver, dns-interface]
level: practitioner
status: docs-checked
description: "Pick the right dns.listeningMode (LOCAL, SINGLE, BIND, ALL, NONE) and avoid turning Pi-hole into an open resolver."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS listening modes

`dns.listeningMode` controls which interfaces and sources Pi-hole answers. The default is `LOCAL`. Use `dns.interface` (default empty, which auto-detects) to name the interface for DNS and DHCP.

| Mode | Behaviour |
| --- | --- |
| `LOCAL` | Accept queries only from hosts on a local subnet, meaning a subnet for which an interface exists. Safe default against DNS amplification if accidentally exposed |
| `SINGLE` | Permit all origins but accept only on the specified interface; loopback is added automatically. Firewall it |
| `BIND` | Force binding only to the listening interfaces instead of the wildcard address. Can cause issues if an interface goes down; useful when another nameserver runs on the same port, for example libvirt |
| `ALL` | Permit all origins on all interfaces. Dangerous: Pi-hole could become an open resolver, so firewall it |
| `NONE` | Add no listening configuration to dnsmasq, for manual setups in auxiliary files; advanced only |

**When to change it.** The reference says to ask yourself whether `LOCAL` works before using `ALL`.

**Set it**

```bash
sudo pihole-FTL --config dns.listeningMode LOCAL
```

**Checklist**

1. Start from `LOCAL`.
2. `SINGLE` and `ALL` accept any origin: make sure the Pi-hole is properly firewalled.

## Checked

2026-11-03. Read the `dns.listeningMode` and `dns.interface` sections of the FTL configuration reference: all five modes, default `LOCAL`, empty interface auto-detects, the firewall and open resolver warnings. Removed the claim that VPN and Docker bridge setups need ALL or SINGLE (not stated in this page) and the query-log check item.

Method: documentation only; no commands were run.
