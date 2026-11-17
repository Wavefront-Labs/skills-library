---
id: computing-software.cybersecurity-defensive.authelia.access-control-query-criteria
name: access-control-query-criteria
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, access-control, query, operators, and-or-logic, present, absent, pattern]
level: advanced
status: docs-checked
description: "Build Authelia query criteria with nested lists for OR and AND logic, using key, value and operators such as present, absent and pattern."
sources:
  - https://www.authelia.com/configuration/security/access-control/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `query` criterion matches specific query-string arguments. It is an advanced option; the docs recommend `resources` for basic needs.

The structure is a list of lists. The outer list is OR, the inner list is AND, and neither level has to be written out explicitly.

```yaml
access_control:
  rules:
    - domain: 'app.example.com'
      policy: 'bypass'
      query:
        - - operator: 'present'
            key: 'secure'
          - operator: 'absent'
            key: 'insecure'
        - - operator: 'pattern'
            key: 'token'
            value: '^(abc123|zyx789)$'
```

This rule matches when `secure` is present AND `insecure` is absent, OR when `token` matches the pattern.

Fields:

- `key`: the query argument name to inspect.
- `value`: required unless the operator is `absent` or `present`. Quote it.
- `operator`: one of the operators listed in the rule operators reference (for example `equal`, `present`, `absent`, `pattern`, `not pattern`). If both key and value are given it defaults to `equal`; with only a key it defaults to `present`.

Check: the docs point to the `authelia access-control check-policy` command to evaluate whether your rules match a given request, and why not.

## Checked
2026-11-08. Read in full: the Access Control configuration page. Confirmed the `query` structure, OR/AND logic, `key`, `value`, `operator` defaults and the example. Removed: the secrets-in-logs warning and the test-URL advice with check-policy (not on the page).
Method: documentation only; no commands were run.
