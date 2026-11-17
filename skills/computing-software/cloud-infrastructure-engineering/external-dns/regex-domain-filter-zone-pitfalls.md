---
id: computing-software.cloud-infrastructure-engineering.external-dns.regex-domain-filter-zone-pitfalls
name: regex-domain-filter-zone-pitfalls
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, regex-pitfall, ignoring-endpoint, apex-zone, multi-region-filter, re2]
level: advanced
status: docs-checked
description: "Debug ExternalDNS 'Ignoring Endpoint' logs caused by regex domain filters that miss apex or multi-label zones, plus the multi-region example."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/domain-filter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex domain filter pitfalls

**The `+` versus `*` mistake.** When filtering zones, a label-prefix group written `[\w-]+` requires at least one repetition, so:
- the apex zone (`example.com`) never matches;
- multi-label zones (`long.sub.example.com`) never match, because `[\w-]+` cannot span dots.

Both zones go unmanaged, and ExternalDNS logs `Ignoring Endpoint` for every record in them with no other hint.

| Regex | Matches | Misses |
|---|---|---|
| `^[\w-]+\.example\.com$` | `sub.example.com` | `example.com`, `long.sub.example.com` |
| `^([\w-]+\.)*example\.com$` | all three | none |

Always use `*` so the apex matches on zero repetitions.

**Multi-region example**
```sh
--regex-domain-filter='^([\w-]+\.)*(?:us-east-1|eu-central-1)\.example\.com$'
--regex-domain-exclusion='^staging\.'
```
`us-east-1.example.com`, `prod.us-east-1.example.com` and `eu-central-1.example.com` are managed; `staging.us-east-1.example.com` is excluded and `other.com` is not managed.

**Debugging:** search logs for `Ignoring Endpoint`, which means no managed zone matched the record. To isolate the filter, temporarily switch to `--domain-filter` with the plain suffix; if records reappear, the regex is the problem.

Escape dots (`\.`) and anchor with `^` and `$` where precision matters.

## Checked

2026-11-04. Confirmed against the ExternalDNS Domain Filter page (zone-partitioning pitfall, regex table, multi-region example, notes and debugging). Nothing removed.
Method: documentation only; no commands were run.
