---
id: computing-software.cybersecurity-defensive.dex.dex-oidc-connector-claim-modifications
name: dex-oidc-connector-claim-modifications
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oidc, claimmodifications, groups, regex]
level: advanced
status: docs-checked
description: "Rewrite upstream group claims in Dex with claimModifications: newGroupFromClaims, filterGroupClaims and modifyGroupNames."
sources:
  - https://dexidp.io/docs/connectors/oidc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`claimModifications` changes claims during login in the oidc connector. It has three tools.

```yaml
claimModifications:
  newGroupFromClaims:
  - prefix: example
    delimiter: "::"
    clearDelimiter: false
    claims:
    - organization
    - email
  filterGroupClaims:
    groupsFilter: "^k8s-.*"
  modifyGroupNames:
    prefix: example-prefix-
    suffix: -example-suffix
```

- `newGroupFromClaims`: builds a new group from other claims, joined with the delimiter. The example yields the group `example::organization::email`. Only string claims are supported; others are skipped. The new group is added to the groups claim.
- `filterGroupClaims.groupsFilter`: keeps only groups matching an RE2 regex (Go `regexp` syntax). Groups made by `newGroupFromClaims` are not passed through this filter.
- `modifyGroupNames`: adds a prefix and/or suffix to all groups as given by the issuer. It applies to all groups, not only filtered ones, and runs before `newGroupFromClaims` groups are created. A group `regular-users` becomes `example-prefix-regular-users` plus the suffix.

Gotchas: include the delimiter in the prefix yourself, since it is appended directly. `modifyGroupNames` runs before `newGroupFromClaims` groups are created.

## Checked

2026-11-03: read against Dex docs, OpenID Connect connector (https://dexidp.io/docs/connectors/oidc/).

Removed or corrected: The unconfirmed ordering "modify, then filter, then new groups".

Method: documentation only; no commands were run.
