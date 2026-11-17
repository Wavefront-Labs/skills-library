---
id: computing-software.cybersecurity-defensive.dex.dex-atlassian-crowd-connector
name: dex-atlassian-crowd-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [atlassian-crowd, connector, groups, rest-api]
level: practitioner
status: docs-checked
description: "Configure the Dex Atlassian Crowd connector: baseURL, application credentials, groups whitelist, usernamePrompt and preferredUsernameField."
sources:
  - https://dexidp.io/docs/connectors/atlassian-crowd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Atlassian Crowd connector authenticates users against Crowd's REST API. It calls `/user` to get user info and `/session` to authenticate the user. Offline access is supported through a new request to the authentication and user info endpoints.

First register Dex as an application in Crowd, then:

```yaml
connectors:
- type: atlassian-crowd
  id: crowd
  name: Crowd
  config:
    baseURL: https://crowd.example.com/crowd
    clientID: $ATLASSIAN_CROWD_APPLICATION_ID
    clientSecret: $ATLASSIAN_CROWD_CLIENT_SECRET
    groups:
    - my-group
    usernamePrompt: Login
    preferredUsernameField: name
```

- `baseURL`: required, the Crowd URL.
- `groups`: optional whitelist communicated through the `groups` scope. If omitted, all the user's Crowd groups are returned when `groups` is requested. If given, only listed groups enter the claim, and a user in none of them is not authenticated.
- `usernamePrompt`: label for the username field.
- `preferredUsernameField`: sets the `preferred_username` claim to a Crowd attribute: `key`, `name` or `email`. If omitted or invalid the claim is empty.

Gotcha: a `groups` list both filters the claim and gates login, so users outside the list cannot sign in at all.

## Checked

2026-11-03: read against Dex docs, Atlassian Crowd connector (https://dexidp.io/docs/connectors/atlassian-crowd/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
