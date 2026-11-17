---
id: computing-software.web-development.directus.policy-ip-allowlist-combining
name: policy-ip-allowlist-combining
category: computing-software
field: web-development
product: directus
tags: [ip-allowlist, policy-combining, additive-permissions, subtractive-ip]
level: advanced
status: docs-checked
description: "Restrict Directus policies to IP addresses, ranges or CIDR blocks and predict how multiple policies combine for fields, item rules and IP access."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/2.access-control.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Allowlist entry formats** (per policy, empty means all IPs): a single IPv4/IPv6 address (`192.168.1.10`), a full range (`10.0.0.1-10.0.0.50`), or CIDR (`10.0.0.0/24`). Rejected: wildcards, netmasks, short ranges (`10.0.0.1-50`), malformed prefixes. List both IPv4 and IPv6 to avoid lockouts.

**Combining rules for a request:**
1. IP check first, **subtractive**: any policy whose allowlist does not match is dropped entirely for that request. This also applies to Require 2FA, which is only enforced when the user's IP is on that policy's allowlist.
2. Field permissions, **additive**: union of fields across remaining policies; duplicates removed.
3. Item rules, **additive**: filters from the same collection are merged with logical OR.

Gotcha: more policies can only widen field and item access, never narrow it. A policy with an IP restriction that fails removes its grants, so keep essential baseline access in a policy without IP limits.

## Checked

2026-11-04: allowlist entry formats and rejected forms, the IPv4 and IPv6 advice, subtractive IP check including Require 2FA, additive field permissions and OR-merged item rules, and the baseline-policy advice confirmed against the Directus Access Control page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
