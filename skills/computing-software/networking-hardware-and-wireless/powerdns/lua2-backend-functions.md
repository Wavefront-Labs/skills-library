---
id: computing-software.networking-hardware-and-wireless.powerdns.lua2-backend-functions
name: lua2-backend-functions
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lua2, backend, dns-lookup, dnssec, dnsname, scripting]
level: advanced
status: docs-checked
description: "Write a PowerDNS lua2 backend: dns_lookup, optional list, domain info, metadata and key functions, DNSSEC needs, DNSName caveats."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/lua2.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua2 backend functions

Launch name `lua2`. Native and primary, DNSSEC capable, no secondary, DNS update or views. API is read-only. Set `bool dns_dnssec` true to enable DNSSEC.

Functions:
- `dns_lookup(qtype, qname, domain_id, ctx)` (required): array of tables with `name`, `type`, `content`, `ttl`, `domain_id` (-1), `auth` (true), `last_modified`, `scope_mask`; empty array when nothing matches. It may return a type other than the one asked.
- `dns_list(target, domain_id)`: same shape; false if not found.
- `dns_get_domaininfo(domain)`: false, or `account`, `kind` ("NATIVE"), `id`, `last_check`, `masters`, `notified_serial`, `serial`. Without it the SOA is used.
- `dns_get_all_domains()`: false, or `{[DNSName] = domaininfo}`. Needed for zone caching, search, and primary function; unlisted zones are unknown.
- `dns_get_domain_metadata(domain, kind)`: required for DNSSEC; array of strings.
- `dns_get_all_domain_metadata(domain)`: optional.
- `dns_get_domain_keys(domain)`: array of `id`, `flags`, `active`, `published`, `content`. Without it, live signing is unavailable.
- `dns_get_before_and_after_names_absolute(id, qname)`: required for DNSSEC; returns `unhashed`, `before`, `after`.
- `dns_set_notified(id, serial)`: without it primary functionality may break.

Caveats:
- Names are `DNSName` objects; compare via `tostring()` or `newDN()`, and sort with `DNSName#canonCompare`.
- `before` and `after` must wrap around, so the last record's `after` is the apex. NSEC3 requires hashing in that function.
- There is no API version 1; use the old Luabackend for that.

## Checked

2026-11-08. Read in full: PowerDNS docs backends/lua2.rst. Confirmed the feature list (native, primary, DNSSEC, read-only API), every function name with its required or optional status, the return keys and defaults, the DNSName comparison warning, the wrap-around rule for before and after, and the missing API version 1. Nothing removed.

Method: documentation only; no commands were run.
