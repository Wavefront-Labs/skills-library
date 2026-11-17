---
id: computing-software.systems-network-administration.pi-hole.local-dns-record-order
name: local-dns-record-order
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [local-dns-records, hosts-precedence, custom-list]
level: practitioner
status: docs-checked
description: "Know where local DNS records come from and which source wins when the same name is defined in several places."
sources: ["https://docs.pi-hole.net/main/faq/", "https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Order of locally defined DNS records

Pi-hole can answer for local names from several sources. The documented order is:

1. The device's host name and `pi.hole`
2. A config file in `/etc/dnsmasq.d/`
3. `/etc/hosts`
4. The "Local (custom) DNS" list, stored in `/etc/pihole/custom.list`

Only the first matching record triggers an address-to-name (PTR) association.

**Config keys that create records**

| Key | Form |
| --- | --- |
| `dns.hosts` | `"IP HOSTNAME [HOSTNAME ...]"`, for example `"192.168.0.1 therouter"` |
| `dns.cnameRecords` | `"<cname>,<target>[,<TTL>]"` |
| `dns.hostRecord` | `"<name>[,<name>...],[<IPv4>],[<IPv6>][,<TTL>]"` |

Example setting through the CLI:

```bash
sudo pihole-FTL --config dns.hosts '["192.168.0.1 therouter"]'
```

Files in `/etc/dnsmasq.d/` are read only when `misc.etc_dnsmasq_d` is `true` (default `false`).

**Checklist**

1. Search the four sources for the name before adding a record.
2. Remove duplicates so the intended record wins.
3. Test with `dig name @pi-hole-address`.
4. Run `pihole reloaddns` if a change does not appear, which flushes and reloads the DNS cache.
5. Remember that `reloaddns` does not re-read `*.conf` files.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FAQ (main/faq); FTL Configuration Reference (ftldns/configfile); The pihole Command (main/pihole-command). Nothing needed removing.
Method: documentation only; no commands were run.
