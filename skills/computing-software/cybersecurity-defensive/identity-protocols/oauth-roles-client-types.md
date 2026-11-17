---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-roles-client-types
name: oauth-roles-client-types
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-roles-client-types, oauth-core-framework, oauth2, roles, confidential-client, public-client, rfc6749, identity-protocols]
level: intro
status: docs-checked
description: "Distinguish resource owner, client, authorization server and resource server, and classify clients as confidential or public with web, native or SPA profiles."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
  - https://www.rfc-editor.org/rfc/rfc8252
  - https://www.rfc-editor.org/rfc/rfc10017
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth roles and client types

Goal: model an OAuth deployment correctly before choosing a flow.

- Roles (RFC 6749 Section 1.1): resource owner (the user), client (the app), authorization server (issues tokens) and resource server (hosts the protected resources).
- Client types (Section 2.1): confidential clients can keep their credentials confidential (for example a client on a secure server) or can authenticate securely by other means; public clients cannot (for example an installed native app or a browser-based app). The AS SHOULD NOT make assumptions about the client type.
- Client profiles: a web application is a confidential client running on a web server; tokens and credentials are not exposed to the resource owner.
- Endpoints: authorization endpoint and token endpoint at the AS, and the redirection endpoint at the client.
- Confidential clients, and clients issued credentials, MUST authenticate when they call the token endpoint (Section 3.2.1).

Gotchas:
- Native apps are public clients and MUST be registered as such, except where per-instance secrets are provisioned (RFC 8252 Section 8.4).
- A browser-based app that uses a backend-for-frontend can have the BFF act as the confidential OAuth client (RFC 10017 Section 6.1).
- The client identifier is not a secret; it is exposed to the resource owner and MUST NOT be used alone for client authentication (RFC 6749 Section 2.2).

Verify: draw the four parties and mark which hop goes through the user agent.

## Checked

Date: 2026-11-02. Confirmed in RFC 6749 Sections 1.1, 2.1, 2.2, 3.2.1, RFC 8252 Section 8.4 and RFC 10017 Section 6.1. Removed as not stated there: the front-channel/back-channel wording, "public clients rely on PKCE and redirect URI", and the embedded-secret extraction claim.

Method: documentation only; no commands were run.
