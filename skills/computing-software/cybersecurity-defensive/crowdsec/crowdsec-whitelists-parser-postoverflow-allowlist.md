---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-whitelists-parser-postoverflow-allowlist
name: crowdsec-whitelists-parser-postoverflow-allowlist
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [whitelist, parser-whitelist, postoverflow, expression-whitelist, cidr, reverse-dns]
level: practitioner
status: docs-checked
description: "Write a CrowdSec parser whitelist file with ip, cidr and expression conditions, and know which enrichers expressions need."
sources: ["https://docs.crowdsec.net/docs/log_processor/whitelist/format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Whitelists are special parsers that discard events: a whitelist file is a normal parser node, so `filter` can restrict its scope. Put parser whitelists in `/etc/crowdsec/parsers/s02-enrich/`.

## Format

```yaml
name: "my/whitelist"
description: "Whitelist events from my ipv4 addresses"
filter: "1 == 1"
whitelist:
  reason: "my ipv4 ranges"
  ip:
    - "127.0.0.1"
  cidr:
    - "192.168.0.0/16"
    - "10.0.0.0/8"
  expression:
    - evt.Enriched.reverse_dns endsWith ".mycoolorg.com."
```

`name` and `description` are mandatory and the `name` must be unique. Reverse DNS conditions need the `crowdsecurity/rdns` enricher; country conditions such as `evt.Enriched.IsoCode == 'FR'` need `crowdsecurity/geoip-enrich`.

## Checked

2026-11-03. Confirmed against the whitelist format page: whitelist file example, mandatory unique name and description, filter, ip/cidr/expression, rdns and geoip-enrich requirements, and the parser stage for whitelists (s02-enrich) on the configuration page. Removed: the postoverflow directory and caveats, the LAPI allowlist recommendation and the whitelist-good-actors reference (the postoverflow and introduction pages returned 404).

Method: documentation only; no commands were run.
