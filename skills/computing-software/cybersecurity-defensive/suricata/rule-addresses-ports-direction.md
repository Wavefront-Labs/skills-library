---
id: computing-software.cybersecurity-defensive.suricata.rule-addresses-ports-direction
name: rule-addresses-ports-direction
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [source-destination, ports, negation, direction]
level: intro
status: docs-checked
description: "Write rule headers: CIDR, negation and grouping for addresses and ports, port ranges, and the ->, => and <> direction operators."
sources: ["https://docs.suricata.io/en/latest/rules/intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Addresses, ports and direction

## Addresses (IPv4 or IPv6)
`/` for CIDR, `!` to negate, `[ ]` to group: `!1.1.1.1`, `[$EXTERNAL_NET, !$HOME_NET]`, `[10.0.0.0/24, !10.0.0.5]`. Variables come from suricata.yaml.

## Ports
`:` for ranges, `!` negation, `[ ]` grouping: `[80, 81, 82]`, `[80:82]`, `[1024:]`, `!80`, `[80:100,!99]`, `[1:80,![2,4]]`.

## Direction
- `->`: only the stated direction.
- `=>`: directional but allows bidirectional transaction matching, using keywords for each direction.
- `<>`: either direction; Suricata duplicates the rule.

There is no `<-`.

Transactional rules have limits: no fast_pattern or prefilter for to-client when a to-server streaming buffer exists, and without an explicit fast_pattern they default to a to-server one.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/intro) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
