---
id: computing-software.cybersecurity-defensive.dex.dex-google-connector-groups-service-account
name: dex-google-connector-groups-service-account
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [google, workspace, groups, service-account]
level: advanced
status: docs-checked
description: "Read Google Workspace groups in Dex with serviceAccountFilePath and domainToAdminEmail, delegating only admin.directory.group.readonly."
sources:
  - https://dexidp.io/docs/connectors/google/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex can return Google Workspace groups with a service account that has Domain-Wide Delegation.

Steps from the docs:

1. Create a service account with Domain-Wide Delegation. Creation produces a JSON key file; store it where Dex can read it.
2. Delegate the `https://www.googleapis.com/auth/admin.directory.group.readonly` scope and only that one. If you delegate more scopes, the service account will not be able to access the API.
3. Enable the Admin SDK.
4. Add the options to the connector config:

```yaml
config:
  clientID: $GOOGLE_CLIENT_ID
  clientSecret: $GOOGLE_CLIENT_SECRET
  redirectURI: http://127.0.0.1:5556/dex/callback
  serviceAccountFilePath: /path/to/service-account.json
  domainToAdminEmail:
    example.com: admin@example.com
```

- `serviceAccountFilePath`: location of the JSON key file.
- `domainToAdminEmail`: maps the base domain to the email of a Workspace user holding at least the Groups Reader (BETA) role. The service account impersonates that user to read groups.

Gotcha: the key file is a high-value secret, so restrict who can read it.

Check: log in with `scope=openid email groups` and confirm group emails appear in the `groups` claim.

## Checked

2026-11-03: read against Dex docs, Google connector (https://dexidp.io/docs/connectors/google/).

Removed or corrected: The claim that extra delegated scopes make the connector refuse to work (page says the account cannot access the API).

Method: documentation only; no commands were run.
