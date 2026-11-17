---
id: computing-software.cybersecurity-defensive.pomerium.configure-custom-idp-urls
name: configure-custom-idp-urls
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [authenticate-service-url, oauth2-callback, oidc, identity-provider, redirect-uri]
level: practitioner
status: docs-checked
description: "Set the Pomerium authenticate service URL and register the single OAuth callback redirect URI with a custom OIDC identity provider."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium is not an identity provider; it works with any OIDC-compliant IdP. A custom IdP needs two things.

**Authenticate service URL**
- Public-facing and resolves to Pomerium (or to the authenticate service in split service mode).
- No path or query parameters, e.g. `https://authenticate.corp.example.com`.
- Must differ from every route URL.
- Users are redirected here whenever login is needed.

**IdP client credentials**
- A client ID and client secret, the IdP name, and possibly an IdP-specific URL (see the Identity Provider Settings reference).
- Register the redirect URI as the authenticate service URL plus `/oauth2/callback`, e.g. `https://authenticate.corp.example.com/oauth2/callback`.

Only one redirect URI is registered with the IdP, so adding services never requires changing the IdP client.

After login, Pomerium keeps the IdP tokens in a session in the Databroker. They are never sent to the client or the upstream; instead Pomerium mints its own signed JWT for upstream apps.

## Checked

2026-11-04. Confirmed against the Authentication page: authenticate service URL rules, /oauth2/callback redirect URI, single registered redirect URL, token storage in the Databroker and Pomerium-minted JWT. Nothing removed.

Method: documentation only; no commands were run.
