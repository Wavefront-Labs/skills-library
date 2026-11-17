---
id: computing-software.systems-network-administration.apache-guacamole.openid-connect-sso
name: openid-connect-sso
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, openid-connect, oidc, sso, single-sign-on, openid-authorization-endpoint, openid-jwks-endpoint, openid-issuer, openid-client-id, openid-redirect-uri, implicit-flow]
level: practitioner
status: docs-checked
description: "Configure OpenID Connect SSO in Guacamole: required endpoint/issuer/client-id/redirect properties, claim types, scope, clock skew and validity defaults, implicit flow."
sources:
  - https://guacamole.apache.org/doc/gug/openid-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenID Connect SSO

Install: `openid/guacamole-auth-sso-openid-1.6.0.jar` from the SSO tarball into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `OPENID_ENABLED=true`.

Required (Docker uppercase, e.g. `OPENID_CLIENT_ID`):
- `openid-authorization-endpoint` (discovery `authorization_endpoint`)
- `openid-jwks-endpoint` (`jwks_uri`)
- `openid-issuer` (`issuer`)
- `openid-client-id`
- `openid-redirect-uri`: full Guacamole URL as typed in a browser; register it with the IdP

Optional (default):
- `openid-username-claim-type` (`email`), `openid-groups-claim-type` (`groups`)
- `openid-attributes-claim-type` (empty): comma-separated claims exposed as `OIDC_` tokens
- `openid-scope` (`openid email profile`; must include at least `openid profile`)
- `openid-allowed-clock-skew` (30 s), `openid-max-token-validity` (300 min), `openid-max-nonce-validity` (10 min)

The extension implements the implicit flow; the manual does not document the authorization-code flow, so the IdP client must allow implicit/ID-token responses.

Login behaviour: `extension-priority: openid` redirects immediately; `*, openid` shows the form with an SSO option.

Authentication only: layer it on a database or another extension for connection data (apache-guacamole.database-auth-overview).

Verify: login redirects to the IdP and returns with the username from the configured claim.

## Checked

2026-11-04. Confirmed against the Guacamole manual page openid-auth: implicit flow, layering on another extension, OPENID_ENABLED, the five required properties and their discovery-document sources, optional claim properties with defaults (email, groups, empty attributes), scope default and the openid profile minimum, clock skew 30 seconds, token validity 300 minutes, nonce validity 10 minutes, and the two extension-priority forms. Nothing removed.

Method: documentation only; no commands were run.
