---
id: computing-software.cybersecurity-defensive.dex.dex-oidc-connector-claim-mapping
name: dex-oidc-connector-claim-mapping
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oidc, claimmapping, overrideclaimmapping, userinfo]
level: advanced
status: docs-checked
description: "Map non-standard upstream claims in the Dex oidc connector with claimMapping, userIDKey, userNameKey and overrideClaimMapping."
sources:
  - https://dexidp.io/docs/connectors/oidc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some providers return non-standard claims such as `mail`. Map them to standard claims with `claimMapping`:

```yaml
config:
  userIDKey: nickname
  userNameKey: nickname
  claimMapping:
    preferred_username: other_user_name
    email: mail
    groups: "cognito:groups"
  overrideClaimMapping: false
```

- `userIDKey`: claim used as user id. Default `sub`.
- `userNameKey`: claim used as user name. Default `name`.
- `claimMapping.preferred_username`: default `preferred_username`.
- `claimMapping.email`: default `email`.
- `claimMapping.groups`: default `groups`.

Rules and gotchas:

- `claimMapping` can only map a non-standard claim to a standard one if the standard one is not returned in the ID token.
- `overrideClaimMapping: true` forces your mappings even when the standard claim exists. By default, if both `email` and `preferred_email` are available, Dex uses `email` regardless of `claimMapping.email`.
- `getUserInfo: true` makes Dex query the UserInfo endpoint for extra claims. UserInfo claims take priority over ID token claims. Use it when the ID token lacks requested claims.
- `acrValues` passes Authentication Context Class values in the authorization request.

The `providerDiscoveryOverrides` block can replace discovered `tokenURL` and `authURL` values.

Check: decode the Dex ID token and confirm the mapped fields.

## Checked

2026-11-03: read against Dex docs, OpenID Connect connector (https://dexidp.io/docs/connectors/oidc/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
