---
id: computing-software.cybersecurity-defensive.suricata.ip-reputation-concepts
name: ip-reputation-concepts
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [ip-reputation, iprep, reputation-feeds]
level: intro
status: docs-checked
description: "Understand Suricata IP reputation: hub and spoke model, feeds, weights, aggregated scores, and where the config, keyword and format are documented."
sources: ["https://docs.suricata.io/en/latest/reputation/ipreputation/ip-reputation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IP reputation

Treat this page as an overview only. Syntax details for the config, the `iprep` keyword and the file format are on separate pages that were not verified here.

The Suricata docs describe a component that ranks IP addresses:
- Hub and spoke: a central database (separate module and system) feeds user-side sensor databases.
- The admin chooses external feeds, supplies credentials and assigns weights, overall or per category.
- Feeds may accept feedback; sensors can opt out but still report that.
- The hub averages scores per IP or block and redistributes them. An API supports external analysis.
- Intelligence is classified positive or negative in categories.

Related pages named in the overview: IP Reputation Config, IP Reputation Keyword and IP Reputation Format.

## Checked

Method: docs-checked 2026-11-09 against https://docs.suricata.io/en/latest/reputation/ipreputation/ip-reputation.html (read in full); dropped the iprep keyword match-detail claim, which the page does not state.
