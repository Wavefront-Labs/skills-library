---
id: computing-software.cloud-infrastructure-engineering.openbao.password-policies
name: password-policies
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, password-policy, charset, min-chars, credential-generation]
level: practitioner
status: docs-checked
description: "Write OpenBao password policies: length bounds, charset rules with min-chars, the 256-character limit and the default policy."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/password-policies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password policies

Used to generate credentials for external systems such as databases and LDAP. Unrelated to ACL policies despite the name.

```hcl
length = 12
rule "charset" {
  charset = "abcdefghijklmnopqrstuvwxyz"
  min-chars = 1
}
rule "charset" {
  charset = "0123456789"
}
```

## Fields

- `length` (required): between 4 and 100. Not a rule, so not checked by the guess-and-check process.
- `rule "charset"`: `charset` (required, printable UTF-8) and `min-chars` (default 0; 0 or unset means the set is drawn from but not required).
- At least one charset is required; a policy with only `length` is invalid.
- Charsets from all rules are combined and de-duplicated; each `min-chars` is still enforced.

## Limits and gotchas

- The combined charset must be at most 256 characters.
- Very restrictive policies can make generation much slower; use the `generate` endpoint to time a policy.
- Not every secrets engine supports password policies.
- Default policy when none is assigned: 20 characters with at least one uppercase, lowercase, numeric and special (`-`) character.

Save and read policies via the Password policies API.

## Checked

2026-11-04. Confirmed against the Password policies page: purpose and unrelated to ACL policies, length 4 to 100, charset and min-chars rules, de-duplicated combined charset capped at 256 characters, at least one charset required, the generate endpoint for timing, engine support varying and the default policy of 20 characters with a dash as the special character. Nothing removed.

Method: documentation only; no commands were run.
