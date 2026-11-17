---
id: computing-software.cybersecurity-defensive.pomerium.ppl-evaluation-and-operators
name: ppl-evaluation-and-operators
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [ppl, deny-overrides-allow, logical-operators, policy-language, criteria]
level: practitioner
status: docs-checked
description: "Write Pomerium Policy Language rules with allow and deny blocks and the and, or, not, nor operators, and list the standard criteria."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PPL is YAML. Top-level actions are `allow` and `deny`. Access requires at least one matching allow rule and no matching deny rule, so deny wins. A policy can be one rule or an array of rules.

Operators: `and` (A and B), `or`, `not` (neither condition, ie NOR), `nor` (at least one unmet, ie NAND). Several operators in one rule are valid, but one per rule is recommended.

Each criterion is one key/value pair; some take a sub-path such as `claim/family_name`.

Standard criteria: `accept`, `authenticated_user`, `claim`, `client_certificate`, `cors_preflight`, `device`, `domain` (email domain), `email`, `http_method`, `http_path`, `mcp_tool`, `invalid_client_certificate`, `pomerium_routes`, `reject`, `source_ip` (IP or CIDR list), `user` (format depends on the IdP).

Zero or Enterprise: `date`, `day_of_week`, `time_of_day`. Enterprise Console only: `groups` (exact group ID, needs directory sync) and `record`.

```yaml
allow:
  and:
    - domain:
        is: example.com
deny:
  or:
    - email:
        is: someone@example.com
```

Note: downstream mTLS adds a default deny via `invalid_client_certificate`; `pomerium_routes` has a default allow.

## Checked

2026-11-04. Read the Pomerium Policy Language page: deny precedence, the four logical operators and their truth tables, one-operator-per-rule recommendation, the criteria tables and tiers all confirmed. Nothing removed.

Method: documentation only; no commands were run.
