---
id: computing-software.cybersecurity-defensive.keycloak.saml-client-setup
name: saml-client-setup
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, saml-client, client-id, assertion-consumer, signing]
level: practitioner
status: docs-checked
description: "Create a SAML 2.0 client in Keycloak, matching the issuer to the Client ID, and configure redirect URLs, bindings and signature options."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/saml/proc-creating-saml-client.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# saml client setup
Keycloak supports SAML 2.0 for registered applications with POST and Redirect bindings. You can require client signature validation and have the server sign and/or encrypt responses.

Create: *Clients* > *Create client*, set *Client type* to SAML, enter the *Client ID* (often a URL; the expected issuer value in SAML requests from the application), *Save*, then configure the Settings tab.

Key settings:
- **Client ID** must match the issuer sent with AuthnRequests; Keycloak pulls the issuer from the request and matches it to a client by this value.
- **Valid Redirect URIs**: wildcards only at the end of a URL. Used when exact SAML endpoints are not registered and Keycloak takes the Assertion Consumer URL from the request.
- **IDP-Initiated SSO URL name**: leaving it empty disables IdP-initiated SSO; otherwise the URL is `server-root/realms/<realm>/protocol/saml/clients/<client-url-name>`. *IDP Initiated SSO Relay State* sets the relay state.
- **Master SAML Processing URL**: used for all SAML requests and responses to the SP, as Assertion Consumer Service URL and Single Logout Service URL. Login requests that contain an ACS URL take precedence; this URL must be validated by a registered Valid Redirect URI pattern.
- **Name ID Format** (used when the request has no name ID policy, or **Force Name ID Format** is on), **Force POST Binding**, **Include AuthnStatement** (on by default; turning it off stops clients determining the maximum session length, which can create sessions that do not expire).

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/saml/proc-creating-saml-client.adoc (settings tab). Removed (not on the page): the metadata descriptor path, the signing/certificate steps, the issuer-mismatch and wildcard gotchas, and the Verify step.
Method: documentation only; no commands were run.
