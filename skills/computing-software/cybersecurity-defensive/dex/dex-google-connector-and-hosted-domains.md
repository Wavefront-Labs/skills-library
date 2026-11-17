---
id: computing-software.cybersecurity-defensive.dex.dex-google-connector-and-hosted-domains
name: dex-google-connector-and-hosted-domains
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [google, connector, oidc, hosted-domain]
level: practitioner
status: docs-checked
description: "Configure the Dex Google connector, which reuses the OIDC flow and adds hosted domain support and group reading via a service account."
sources:
  - https://dexidp.io/docs/connectors/google/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Google connector uses the same authentication flow as the OIDC connector, plus Google features: hosted domain support and group reading through a service account.

Minimal config:

```yaml
connectors:
- type: google
  id: google
  name: Google
  config:
    clientID: $GOOGLE_CLIENT_ID
    clientSecret: $GOOGLE_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
```

The `redirectURI` is Dex's issuer URL plus `/callback`.

Google does not support the OpenID Connect groups claim and only supports fetching a user's group membership with a service account.

Notes:

- The `groups` scope only returns data once the service account setup in the next skill is done.
- `hostedDomains` is a list of G Suite domains that may log in, for example `- example.com`.
- `groups` is a list of group emails that may log in, for example `- admins@example.com`.

Gotcha: the connector page notes users are shown the consent screen on every login by default. See the `promptType` skill to change that.

## Checked

2026-11-03: read against Dex docs, Google connector (https://dexidp.io/docs/connectors/google/).

Removed or corrected: The Google Cloud console instruction, the email_verified Check, and the advice to prefer this connector over OIDC.

Method: documentation only; no commands were run.
