---
id: computing-software.cybersecurity-defensive.dex.dex-oidc-connector-groups-and-userinfo
name: dex-oidc-connector-groups-and-userinfo
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oidc, groups, insecureenablegroups, allowedgroups]
level: advanced
status: docs-checked
description: "Enable group claims in the Dex oidc connector with insecureEnableGroups and restrict logins with allowedGroups, knowing claims go stale."
sources:
  - https://dexidp.io/docs/connectors/oidc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Groups claims, like other OIDC claims through Dex, only refresh when the ID token is refreshed. The regular refresh flow does not update the groups claim. Because of that, the oidc connector does not allow groups claims by default.

If you accept possibly stale groups, enable them per connector:

```yaml
config:
  insecureEnableGroups: true
  allowedGroups:
  - platform-admins
  - developers
  getUserInfo: true
```

- `insecureEnableGroups`: allow groups claims from this connector.
- `allowedGroups`: authentication succeeds only if the user is a member of at least one listed group.
- `getUserInfo`: query the UserInfo endpoint for additional claims; they take priority over ID token claims. Use it when the ID token does not contain the claims requested.
- `claimMapping.groups`: change the claim name that holds groups (default `groups`), for example `cognito:groups`.

The docs' commented `scopes` example lists `groups` among the additional scopes to request.

## Checked

2026-11-03: read against Dex docs, OpenID Connect connector (https://dexidp.io/docs/connectors/oidc/).

Removed or corrected: The eventual-consistency gotcha, the scopes gotcha and the Check step (inferences not on the page).

Method: documentation only; no commands were run.
