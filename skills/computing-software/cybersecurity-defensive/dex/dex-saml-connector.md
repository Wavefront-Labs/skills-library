---
id: computing-software.cybersecurity-defensive.dex.dex-saml-connector
name: dex-saml-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [saml, connector, nameid, groups]
level: advanced
status: docs-checked
description: "Configure the Dex SAML connector: ssoURL, ca, entityIssuer, usernameAttr, emailAttr, groupsAttr, nameIDPolicyFormat and its limits."
sources:
  - https://dexidp.io/docs/connectors/saml/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The SAML connector authenticates through a SAML 2.0 identity provider using the HTTP POST binding.

Warning from the docs: the SAML connector is unmaintained, likely vulnerable to authentication bypass vulnerabilities, and under consideration for deprecation. Prefer OpenID Connect, OAuth2 or LDAP where the identity provider supports them.

```yaml
connectors:
- type: saml
  id: okta
  name: Okta
  config:
    ssoURL: https://dev-111102.oktapreview.com/app/foo/exk91cb99lKkKSYoy0h7/sso/saml
    ca: /etc/dex/saml-ca.pem
    redirectURI: http://127.0.0.1:5556/dex/callback
    usernameAttr: name
    emailAttr: email
    groupsAttr: groups
```

More options: `entityIssuer`, `ssoIssuer`, `groupsDelim: ", "` (groups held in one attribute are split on this delimiter), `nameIDPolicyFormat: persistent`, `allowedGroups` and `filterGroups`.

Points from the docs:

- The `NameID` element is the user's unique identifier, assumed unique and permanent. Use `nameIDPolicyFormat` so the IdP returns a value that satisfies this.
- Dex must send the initial AuthnRequest and validates the response's `InResponseTo`. Unprompted AuthnResponses are not processed.
- Signed AuthnRequests and encrypted attributes are not supported.
- If `filterGroups: true`, groups not in `allowedGroups` are excluded.
- The SAML connector ignores the `offline_access` scope, so no refresh tokens come from it.

`redirectURI` is Dex's callback URL; a `Destination` in the response must match it exactly, and it is the expected audience unless `entityIssuer` is set.

## Checked

2026-11-03: read against Dex docs, SAML connector (https://dexidp.io/docs/connectors/saml/).

Removed or corrected: The unconfirmed "assertion consumer endpoint" claim. Added the page warning that the connector is unmaintained.

Method: documentation only; no commands were run.
