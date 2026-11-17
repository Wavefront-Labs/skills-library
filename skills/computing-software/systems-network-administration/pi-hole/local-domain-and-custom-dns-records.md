---
id: computing-software.systems-network-administration.pi-hole.local-domain-and-custom-dns-records
name: local-domain-and-custom-dns-records
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [dns-domain, custom-dns-hosts, cname-records]
level: practitioner
status: docs-checked
description: "Define local DNS records in Pi-hole with dns.hosts, dns.cnameRecords and dns.hostRecord, and set the local domain."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local domain and custom records

**Local domain.** `dns.domain.name` (default `lan`) is purely local. With `dns.domain.local` true (default), FTL answers from its cache and configuration and never forwards the domain upstream, unless a reverse server is set for exactly that domain. For DHCP it is returned to clients and limits which domain suffix DHCP-configured hosts may claim, so an untrusted host cannot advertise itself as `google.com`. With domain `mylab.com`, a host named `laptop` is reachable as `laptop` and `laptop.mylab.com`. An empty string disables setting a domain.

**Records**

| Option | Form | Example |
| --- | --- | --- |
| `dns.hosts` | `"IP HOSTNAME [HOSTNAME ...]"` | `"192.168.0.1 therouter"` |
| `dns.cnameRecords` | `"<cname>,<target>[,<TTL>]"` | CNAME to a target |
| `dns.hostRecord` | `"<name>[,<name>...],[<IPv4>],[<IPv6>][,<TTL>]"` | `"laptop,laptop.lan,192.168.0.1,1234::100"` |

A TTL on a CNAME overrides the `local-ttl` value.

**Related**

- `dns.domainNeeded` (default `false`): never forward plain names without dots upstream.
- `dns.expandHosts` (default `false`): add the domain to simple names in `/etc/hosts`.

**Checklist**

1. Set a domain that your DHCP clients should use.
2. Add records via the web interface or `pihole-FTL --config dns.hosts`.
3. Query with `dig laptop.lan @pi.hole` to confirm.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile). Nothing needed removing.
Method: documentation only; no commands were run.
