---
id: computing-software.systems-network-administration.dns-dhcp.bind-stub-mirror-and-forward-zones
name: bind-stub-mirror-and-forward-zones
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, bind-zone-types, mirror-zone, stub-zone, forward-zone]
level: practitioner
status: verified
description: "Choose among BIND zone types beyond primary/secondary: stub, static-stub, forward and mirror zones, with config, behaviour differences and pitfalls."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://www.rfc-editor.org/rfc/rfc8806
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Stub/mirror/forward zone types

| Type | What it holds | Used for |
|------|---------------|----------|
| `primary` / `secondary` | the full zone | authoritative service |
| `stub` | NS records of the zone, refreshed from the listed primaries; overrides parent delegation (ARM: not recommended, prefer real delegation) | work around missing or broken delegations |
| `static-stub` | NS names/addresses configured statically (`server-addresses`, `server-names`), overrides parent and server NS | force specific servers; no refresh; ARM: not recommended |
| `forward` | nothing; forwards queries for the domain | conditional forwarding |
| `mirror` | a DNSSEC-validated copy of a zone (typically the root) | local root (RFC 8806) |
| `redirect` | answers when resolution would return NXDOMAIN (tagged deprecated in the ARM) | NXDOMAIN rewriting |

## Examples
```
zone "corp.internal" { type stub; primaries { 10.0.0.53; }; file "stub/corp.internal"; };

zone "partner.example" { type static-stub; server-addresses { 203.0.113.53; }; };

zone "ad.example.com" { type forward; forward only; forwarders { 10.1.1.10; 10.1.1.11; }; };

zone "." { type mirror; };          // built-in list of root primaries
```

## Choosing stub vs forward
- Stub/static-stub: named uses the listed servers as the name servers for the zone and resolves from them itself. Non-recursive queries (RD bit off) to a static-stub zone get REFUSED, and a NOTIFY to it is rejected with NOTAUTH.
- Forward: sends queries to the `forwarders`; the target must offer recursion to you. `forward only` queries only the forwarders; `forward first` (default) falls back to resolving the name itself (can leak internal names to the internet). A forward zone without `forwarders` disables forwarding for that domain.

## Mirror zone notes
- Validation applies to the whole zone at transfer and again when the file is loaded; a failing new version schedules a retransfer while the last good version is used until it expires, after which normal recursion is used.
- The AA bit is not set and AD is set on mirror answers; mirror zones cannot be used in a view without recursion.
- Use the `file` option to keep mirror contents across restarts; `request-ixfr no;` forces AXFR. Mirroring a zone other than root needs an explicit `primaries` list and a trust anchor.

## Gotchas
- Stub/forward zones under a signed parent with no DS for an internal name: validation can fail
  (bogus). Add `validate-except { "corp.internal"; };` for private namespaces (a permanent exemption, unlike an expiring NTA).
- A parent primary that has child stub zones configured needs the same stub zones on all its secondaries.

## Verify
- [ ] `dig @resolver host.corp.internal` resolves.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch notes and grammar), read on 2026-10-26. Confirmed in reference.rst: type stub, static-stub, forward, mirror and redirect semantics, the not-recommended warnings, mirror validation behaviour and recursion requirement, forward first default, validate-except. Removed the unconfirmed version gate and the claim that stub and forward zones work only on recursive views (documented only for mirror).

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30, two named instances, authoritative one on the container address): stub zone resolving through the NS data it fetched (the stub file holds the SOA, NS and glue), static-stub resolving and answering REFUSED to a non-recursive query, forward only to a dead forwarder giving SERVFAIL, forward zone resolving, `validate-except` and a mirror zone parsed by named-checkconf. Not run: mirror transfer and validation, NOTIFY to a static-stub zone, validate-except effect against a signed parent.
