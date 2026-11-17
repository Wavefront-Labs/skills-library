---
id: computing-software.systems-network-administration.pi-hole.special-domains-bypass-prevention
name: special-domains-bypass-prevention
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [mozilla-canary, icloud-private-relay, designated-resolver]
level: practitioner
status: docs-checked
description: "Keep clients from bypassing Pi-hole using the Firefox canary domain, iCloud Private Relay and Discovery of Designated Resolvers."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Special domains that stop DNS bypass

Under `[dns.specialDomains]`, Pi-hole can answer certain names so clients stay on its DNS. All three default to `true`.

| Option | What it answers | Purpose |
| --- | --- | --- |
| `mozillaCanary` | NXDOMAIN to A and AAAA queries for `use-application-dns.net` | Disables Firefox automatic DNS-over-HTTPS, per Mozilla's guidance |
| `iCloudPrivateRelay` | NXDOMAIN for `mask.icloud.com` and `mask-h2.icloud.com` | Stops Apple devices bypassing Pi-hole via iCloud Private Relay, per Apple's network guidance |
| `designatedResolver` | NODATA for all queries to zone `resolver.arpa` | Prevents bypass using Discovery of Designated Resolvers (RFC 9462, section 4) |

**ESNI.** `dns.blockESNI` (default `true`) also blocks `_esni.` subdomains of blocked domains by replying NXDOMAIN. ESNI is mostly obsolete; ECH is served over the HTTPS record on the same name and is blocked automatically.

**Related**

- `dns.EDNS0ECS` (default `true`) overwrites the query source from EDNS0 client subnet data, helping to see real client IPs behind a NAT router.
- `dns.ignoreLocalhost` (default `false`) hides localhost queries.

**Checklist**

1. All three special domain options default to `true`.

## Checked

2026-11-03. Read the `[dns.specialDomains]`, `dns.blockESNI`, `dns.EDNS0ECS` and `dns.ignoreLocalhost` sections of the FTL configuration reference: names, replies, defaults, the Mozilla and Apple recommendations and RFC 9462 section 4. Removed the unsupported advice, including the claim about DoH servers addressed by IP.

Method: documentation only; no commands were run.
