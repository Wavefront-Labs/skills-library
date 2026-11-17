---
id: computing-software.cybersecurity-defensive.dex.dex-github-connector-orgs-and-teams
name: dex-github-connector-orgs-and-teams
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [github, connector, orgs, teams]
level: practitioner
status: docs-checked
description: "Configure the Dex GitHub connector: clientID, redirectURI, orgs and teams restriction, loadAllGroups, teamNameField and useLoginAsID."
sources:
  - https://dexidp.io/docs/connectors/github/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Register an OAuth app in GitHub with callback URL `(dex issuer)/callback`, for example `https://auth.example.com/dex/callback`.

```yaml
connectors:
- type: github
  id: github
  name: GitHub
  config:
    clientID: $GITHUB_CLIENT_ID
    clientSecret: $GITHUB_CLIENT_SECRET
    redirectURI: https://auth.example.com/dex/callback
    orgs:
    - name: my-organization
    - name: my-organization-with-teams
      teams:
      - red-team
      - blue-team
    teamNameField: slug
```

- `org` (legacy) and `orgs` cannot be used together.
- With `orgs`, the user must belong to at least one org (and team, if set) to log in.
- With the `groups` scope, claims are formatted `org:team`, for example `coreos:engineering`. If teams are listed, only those teams are returned.
- `loadAllGroups: true` loads all of the user's orgs and teams, but only works when neither `org` nor `orgs` is set.
- `teamNameField`: `name` (default), `slug` or `both`.
- `useLoginAsID: true` uses the handle instead of the internal id as user id.
- `preferredEmailDomain` picks which email to return; a public email is always returned first.

Caveat: an org must be asked explicitly to grant Dex access, otherwise Dex cannot check membership and the user cannot log in.

Dex stores a read-only GitHub token to re-query on refresh.

## Checked

2026-11-03: read against Dex docs, GitHub connector (https://dexidp.io/docs/connectors/github/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
