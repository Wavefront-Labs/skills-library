---
id: computing-software.cybersecurity-defensive.dex.dex-gitlab-connector
name: dex-gitlab-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [gitlab, connector, groups, scopes]
level: practitioner
status: docs-checked
description: "Configure the Dex GitLab connector: baseURL, groups restriction, useLoginAsID, getGroupsPermission and the read_user and openid scopes."
sources:
  - https://dexidp.io/docs/connectors/gitlab/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The GitLab connector uses the GitLab OAuth2 flow. On refresh, Dex re-queries GitLab to update the ID token, storing a read-only GitLab access token in its storage. Users who reject Dex's access also revoke Dex clients that authenticated them.

The GitLab application must grant the `read_user` and `openid` scopes. `openid` is required only if group membership is wanted as a claim.

```yaml
connectors:
- type: gitlab
  id: gitlab
  name: GitLab
  config:
    baseURL: https://gitlab.com
    clientID: $GITLAB_APPLICATION_ID
    clientSecret: $GITLAB_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    groups:
    - my-group
    useLoginAsID: false
    getGroupsPermission: false
```

- `baseURL`: GitLab instance, `https://gitlab.com` for the hosted service. Change it for self-managed GitLab.
- `groups`: a whitelist for the `groups` claim. A user in none of the listed groups is not authenticated.
- `useLoginAsID`: use the user's handle (@mention) as user id instead of the internal GitLab id.
- `getGroupsPermission`: when enabled, user group permissions are included in the groups. A maintainer of `project/group1` gets both `project/group1` and `project/group1:maintainer`.

Register the callback as `(dex issuer)/callback`.

## Checked

2026-11-03: read against Dex docs, GitLab connector (https://dexidp.io/docs/connectors/gitlab/).

Removed or corrected: The claim of a redirect URI error on mismatch; "numeric id" wording.

Method: documentation only; no commands were run.
