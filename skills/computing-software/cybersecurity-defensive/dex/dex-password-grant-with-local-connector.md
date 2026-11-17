---
id: computing-software.cybersecurity-defensive.dex.dex-password-grant-with-local-connector
name: dex-password-grant-with-local-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [password-grant, local-connector, static-passwords, curl]
level: advanced
status: docs-checked
description: "Enable the OAuth2 password grant with passwordConnector: local and request tokens with curl for public and private clients."
sources:
  - https://dexidp.io/docs/connectors/local/
  - https://dexidp.io/docs/configuration/oauth2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The password grant lets a client send a user's credentials to Dex and receive tokens directly. The OAuth 2.0 Security Best Current Practice advises against it, so treat it as a last resort.

Setup with the local connector:

```yaml
enablePasswordDB: true
oauth2:
  passwordConnector: local
staticClients:
  - id: public-client
    public: true
    name: 'Public Client'
    redirectURIs: ['https://example.com/oidc/callback']
  - id: private-client
    secret: app-secret
    name: 'Private Client'
    redirectURIs: ['https://example.com/oidc/callback']
```

Request a token. A public client sends only its id in the Basic header (`public-client:`, base64 encoded):

```bash
curl -L -X POST 'http://localhost:8080/dex/token'   -H 'Authorization: Basic cHVibGljLWNsaWVudDo='   -H 'Content-Type: application/x-www-form-urlencoded'   --data-urlencode 'grant_type=password'   --data-urlencode 'scope=openid profile'   --data-urlencode 'username=admin@example.com'   --data-urlencode 'password=password'
```

A private client sends `client-id:client-secret` base64 encoded instead.

Gotchas: the password grant will not work unless `passwordConnector` names a connector id, and `password` must be in `grantTypes` if you set that list.

The client sends the user's credentials straight to Dex and gets tokens back without an intermediate authorization step, which is the reason the docs warn about serious security concerns.

## Checked

2026-11-03: read against Dex docs, local connector (https://dexidp.io/docs/connectors/local/); Dex docs, OAuth2 configuration (https://dexidp.io/docs/configuration/oauth2/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
