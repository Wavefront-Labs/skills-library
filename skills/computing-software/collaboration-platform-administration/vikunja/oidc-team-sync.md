---
id: computing-software.collaboration-platform-administration.vikunja.oidc-team-sync
name: oidc-team-sync
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, vikunja-groups-claim, oidcid, team-sync, vikunja-scope, authentik-mapping]
level: advanced
status: docs-checked
description: "Automatically create and populate Vikunja teams from the vikunja_groups ID token claim, the oidcID rules, sign-out behaviour and the Authentik setup."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/openid.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From 0.24.0 Vikunja syncs teams from the ID token. The token must carry `vikunja_groups`:

```
{"vikunja_groups": [{"name": "team 1", "oidcID": 33349, "description": "optional", "isPublic": false}]}
```

`name` and `oidcID` are required; `oidcID` is any unique string under 250 characters. Missing `oidcID` gives a "Custom Scope malformed" error. Without the claim nothing happens.

Request it with a custom scope such as `vikunja_scope`: `scope: openid profile email vikunja_scope`. The config reference also allows the `groups` scope, using each group name as the team's unique id.

Behaviour: OIDC teams show "(OIDC)" in the UI and cannot be edited in Vikunja. The `oidcID` uniquely identifies a team. Teams you joined locally (empty oidcID) are left alone. If you are in an OIDC team missing from the token you are removed from it, and a team losing its last member is deleted.

Authentik: create a scope property mapping named `vikunja_scope` returning `vikunja_groups` built from `request.user.ak_groups.all()` (name and `num_pk` as oidcID), then add it under the provider's advanced protocol settings Scopes. Keycloak: see Makerspace Darmstadt's mapper project.

## Checked

2026-11-04: checked against the OpenID page (automatic team assignment, use cases, Authentik setup) and config-raw.json (scope option, `groups` scope). Replaced "matched by oidcID, not name", which the page's use cases do not support.

Method: documentation only; no commands were run.
