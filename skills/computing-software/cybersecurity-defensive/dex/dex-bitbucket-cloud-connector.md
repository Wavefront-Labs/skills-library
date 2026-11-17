---
id: computing-software.cybersecurity-defensive.dex.dex-bitbucket-cloud-connector
name: dex-bitbucket-cloud-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [bitbucket-cloud, connector, teams, groups]
level: practitioner
status: docs-checked
description: "Configure the Dex Bitbucket Cloud connector: OAuth consumer permissions, a teams whitelist for groups, and includeTeamGroups."
sources:
  - https://dexidp.io/docs/connectors/bitbucketcloud/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `bitbucket-cloud` connector uses the Bitbucket OAuth2 flow. Register an OAuth consumer with callback URL `(dex issuer)/callback`.

Required consumer permissions:

- Account: Read, to extract base information (email, username).
- Workspace membership: Read, only needed to get the user's teams.

```yaml
connectors:
- type: bitbucket-cloud
  id: bitbucket-cloud
  name: Bitbucket Cloud
  config:
    clientID: $BITBUCKET_CLIENT_ID
    clientSecret: $BITBUCKET_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    teams:
    - my-team
    includeTeamGroups: true
```

- `teams`: optional whitelist communicated through the `groups` scope. If omitted, all the user's Bitbucket teams are returned when `groups` is requested. If given, only listed teams enter the groups claim.
- `includeTeamGroups`: when true, the claim also includes team groups, for example `["my_team", "my_team/administrators", "my_team/members"]`.

Dex stores a read-only Bitbucket access token to re-query user data on refresh.

Gotcha: if the user is not in any of the configured `teams`, the user will not be authenticated.

Teams are communicated through the `groups` scope, so request it from the client to see them.

## Checked

2026-11-03: read against Dex docs, Bitbucket Cloud connector (https://dexidp.io/docs/connectors/bitbucketcloud/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
