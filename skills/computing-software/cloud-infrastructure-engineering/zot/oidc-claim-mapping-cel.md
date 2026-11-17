---
id: computing-software.cloud-infrastructure-engineering.zot.oidc-claim-mapping-cel
name: oidc-claim-mapping-cel
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, claim-mapping, cel-expression, oidc-validations, ci-identity, github-actions]
level: advanced
status: docs-checked
description: "Map OIDC token claims to a Zot username and groups with CEL: variables, validations, defaults, and a GitHub Actions example restricting an owner."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Under a `bearer.oidc` entry, `claimMapping` is optional and uses CEL with two variables: `claims` (the token claims map) and `vars` (extracted variables).

| Field | Notes |
|---|---|
| `username` | CEL string. Default `claims.iss + '/' + claims.sub` |
| `groups` | CEL list of strings. Default none |
| `variables` | Ordered `name`/`expression` list; later entries can use `vars.<name>` |
| `validations` | Each has a boolean `expression` and a `message` shown on failure |

Example for GitHub Actions tokens:

```json
"oidc": [ { "issuer": "https://token.actions.githubusercontent.com", "audiences": ["zot"],
  "claimMapping": {
    "variables": [ { "name": "owner", "expression": "claims.repository_owner" },
                   { "name": "repo",  "expression": "claims.repository" } ],
    "validations": [ { "expression": "vars.owner == 'my-org'", "message": "only my-org repositories are allowed" } ],
    "username": "vars.repo",
    "groups": "['github-actions', 'ci']"
  } } ]
```

Then grant the resulting username or group in `accessControl.repositories` policies. A failed validation rejects the token with its message.

## Checked

2026-11-04. Read against the zot authn-authz article (Claim mapping with CEL); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
