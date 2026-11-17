---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-expr-helpers-and-event-model
name: crowdsec-expr-helpers-and-event-model
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [expr, expr-helpers, ip-helpers, iprange, geoip, lookuphost, event-object]
level: advanced
status: docs-checked
description: "Use the expression language helpers available in filters, whitelists and profiles, with IP helpers and when LookupHost is safe."
sources: ["https://docs.crowdsec.net/docs/expr/ip_helpers", "https://docs.crowdsec.net/docs/expr/intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CrowdSec filters (parsers, scenarios, profiles), statics and whitelists are written in the expr language. Expressions see the current event as `evt`; in profiles the alert is available as `Alert`.

## IP helpers

- `IpInRange(IPStr, RangeStr) bool`: true if the IP is in the CIDR range.
- `IpToRange(IPStr, MaskStr)`: returns the subnet of the IP at the given CIDR size, useful for scenarios acting on a range instead of one IP.
- `IsIP(ip)`, `IsIPV4(ip)`, `IsIPV6(ip)`: validity checks.
- `LookupHost(host) []string`: resolve a hostname to addresses.
- `GeoIPEnrich(ip)` and `GeoIPASNEnrich(ip)`: return GeoIP2 city and ASN objects.

## LookupHost cautions

Use it only in postoverflows because it can be very slow. If you whitelist a domain behind a CDN provider, every domain on that CDN is whitelisted too. Never pass variables derived from log content, since that is untrusted user input. Lookups, including failed ones, go through a DNS cache and a hostname is only resolved again after its cache entry expires.

Example whitelist condition (useful with a dynamic IP and a dynamic DNS provider): `evt.Overflow.Alert.Source.IP in LookupHost('mydomain.tld')`.

## Checked
2026-11-08. Confirmed against the Expr introduction and IP helpers pages: where expr is used, `evt` and `Alert`, `IpInRange`, `IpToRange`, `IsIP`, `IsIPV4`, `IsIPV6`, `LookupHost` and its warnings, DNS cache behaviour, `GeoIPEnrich`, `GeoIPASNEnrich`. Removed: the `evt.Parsed/Meta/Enriched/Line.Raw` field list and the reverse_dns example (not on these pages).
Method: documentation only; no commands were run.
