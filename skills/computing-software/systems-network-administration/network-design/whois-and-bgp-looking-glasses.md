---
id: computing-software.systems-network-administration.network-design.whois-and-bgp-looking-glasses
name: whois-and-bgp-looking-glasses
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, whois, looking-glass, rdap, bgp-tools, irr]
level: practitioner
status: docs-checked
description: "Use whois/RDAP and BGP looking glasses to troubleshoot internet routing: who owns an IP or ASN, what prefixes are announced, AS paths seen from outside, and IRR/RPKI status."
sources:
  - https://www.rfc-editor.org/rfc/rfc3912
  - https://www.rfc-editor.org/rfc/rfc9083
  - https://bgp.tools/
  - https://lg.he.net/
  - https://stat.ripe.net/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# whois and BGP looking glasses

## whois / RDAP
- WHOIS (RFC 3912) is a simple query protocol: a server listens on TCP port 43 and answers text queries.
- RDAP (RFC 9083) is the structured successor: responses are JSON, and registries expose it over HTTPS (for example the
  ARIN RDAP service at `rdap.arin.net/registry/ip/<address>`). Use RDAP when you want to parse results in scripts.
- Regional registries (ARIN, RIPE NCC, APNIC, LACNIC, AFRINIC) hold the data; use the abuse contact in the record for
  incident reports.

```
whois 203.0.113.10
whois AS64500
curl -s https://rdap.arin.net/registry/ip/203.0.113.10
```

## Looking glasses
A looking glass runs read-only routing queries from another network's router. Hurricane Electric publishes one at
`lg.he.net`; carriers publish their own.

## Route analytics
- **bgp.tools**: search by ASN, prefix, DNS name or MAC address.
- **RIPEstat**: an information service with Internet-related data and analytics for prefixes and ASNs.
- Check RPKI validity (ROAs, max length) with your RIR's tooling or `rpki-client`; the RIPE validator URL previously
  listed returned no readable content in this review.

## Troubleshooting uses
- A new prefix is unreachable from some places: looking glasses show whether it is seen and with what AS path; if it is
  missing in some regions, suspect upstream filters (missing IRR objects) or RPKI invalid status.
- Traffic takes a strange path: compare AS paths from several looking glasses; check prepends and communities.
- Suspected hijack or leak: look for an unexpected origin AS for your prefix.

## Verify
- [ ] Your prefixes are visible from multiple looking glasses with the expected origin AS and valid RPKI; IRR route
  objects match announcements.

## Checked
2026-10-28. Confirmed in RFC 3912 (TCP port 43), RFC 9083 (JSON RDAP responses), the ARIN RDAP endpoint response, the
bgp.tools, RIPEstat and lg.he.net landing pages. Removed as unconfirmed: RADB and Team Cymru whois server syntax,
the NLNOG RING and RIPE Atlas descriptions, bgp.he.net, named carrier looking glasses, `jq` pipe.
Method: documentation only; no commands were run.
