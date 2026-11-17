---
id: computing-software.cloud-infrastructure-engineering.external-dns.domain-filter-plain-and-regex
name: domain-filter-plain-and-regex
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, domain-filter, exclude-domains, regex-domain-filter, regex-domain-exclusion, credential-boundary]
level: practitioner
status: docs-checked
description: "ExternalDNS domain filtering: plain suffix filters vs regex filters, matching order, which wins, and why credentials, not flags, are the enforcement boundary."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/domain-filter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain filter modes

| Flag | Mode | Meaning |
|---|---|---|
| `--domain-filter` | plain | suffix match: a domain and all subdomains |
| `--exclude-domains` | plain | suffix exclusion from the filter |
| `--regex-domain-filter` | regex | full match; overrides `--domain-filter` |
| `--regex-domain-exclusion` | regex | removes matches; can be used alone |

Setting any regex flag enables regex mode, and the plain list flags are then ignored entirely.

```sh
--domain-filter=example.com
--exclude-domains=staging.example.com
```

**Regex order (exclusion first)**
1. Exclusion matches: rejected.
2. Filter matches: accepted.
3. Only an exclusion is set and the name did not match it: accepted.
4. A filter is set and the name did not match: rejected.

```sh
--regex-domain-filter='(?:foo|bar)\.org$'
--regex-domain-exclusion='^example\.(?:foo|bar)\.org$'
```

Syntax is Go RE2. Matching is case-sensitive; names are lowercased with trailing dots stripped, and converted to Unicode form first.

**Important:** filters express intent; they are not an enforcement boundary. Credentials (IAM policies, token scopes, ACLs) are. Scope them to the managed zones.

Filters apply to record names; providers that partition zones first (such as PowerDNS) also apply them to zone names.

**Testing:** the page suggests validating a regex against real zone names at regex101.com with the Golang flavour.

## Checked

2026-11-04. Confirmed against the ExternalDNS Domain Filter page: flag table, plain and regex modes, matching order, notes on syntax, case and IDN, and the testing advice. Nothing removed.
Method: documentation only; no commands were run.
