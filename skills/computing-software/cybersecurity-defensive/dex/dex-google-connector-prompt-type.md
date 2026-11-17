---
id: computing-software.cybersecurity-defensive.dex.dex-google-connector-prompt-type
name: dex-google-connector-prompt-type
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [google, prompttype, consent, oidc]
level: practitioner
status: docs-checked
description: "Change the Google consent behaviour in Dex with promptType, including the empty string to restore Google default behaviour."
sources:
  - https://dexidp.io/docs/connectors/google/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the Google connector asks Google for a consent prompt, so users see the consent screen every time they log in.

To change that, set `promptType` in the connector config to any OIDC-supported value:

```yaml
connectors:
- type: google
  id: google
  name: Google
  config:
    clientID: $GOOGLE_CLIENT_ID
    clientSecret: $GOOGLE_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    promptType: ""
```

Setting `promptType` to an empty string makes Google fall back to its default behaviour, which skips the consent screen for every authorization request.

Related OIDC context: the generic OIDC connector has the same field. For `offline_access` the prompt parameter defaults to `prompt=consent`, which not all OIDC providers support, and some use `prompt=login` or `prompt=none`.

The default value is `consent` when `promptType` is not set.

The field sits in the connector `config` block beside `clientID`, `clientSecret` and `redirectURI`.

## Checked

2026-11-03: read against Dex docs, Google connector (https://dexidp.io/docs/connectors/google/); Dex docs, OpenID Connect connector (https://dexidp.io/docs/connectors/oidc/).

Removed or corrected: The claim that an empty string removes the parameter, and the Check step.

Method: documentation only; no commands were run.
