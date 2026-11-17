---
id: computing-software.cybersecurity-defensive.keycloak.saml-idp-initiated-login
name: saml-idp-initiated-login
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, idp-initiated, saml-binding, acs-url, relay-state]
level: practitioner
status: docs-checked
description: "Set up SAML IdP-initiated login and understand which binding and ACS URL Keycloak selects (POST preferred over Redirect)."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/saml/idp-initiated-login.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# saml idp initiated login
In the client's *Settings* tab set *IDP Initiated SSO URL Name* (a simple string with no whitespace). The client is then reachable at `<root>/realms/<realm>/protocol/saml/clients/<url-name>`; leaving the name empty disables IdP-initiated SSO.

The implementation prefers POST over REDIRECT binding; the binding and SP URL are chosen as follows:
1. If the *Assertion Consumer Service POST Binding URL* is defined (in *Fine Grain SAML Endpoint Configuration*), POST binding is used through that URL.
2. Otherwise, if the general *Master SAML Processing URL* is specified, POST binding is used through it.
3. As a last resort, if the *Assertion Consumer Service Redirect Binding URL* is configured there, REDIRECT binding is used.

For a special relay state, set *IDP Initiated SSO Relay State* on the Settings tab, or pass a `RelayState` query parameter: `<root>/realms/<realm>/protocol/saml/clients/<url-name>?RelayState=thestate`.

With identity brokering, an external IdP can start a login for a client defined at the broker: in the external IdP's client set *IDP Initiated SSO URL Name* and set the *Assertion Consumer Service POST Binding URL* to `broker-root/realms/<broker-realm>/broker/<idp-name>/endpoint/clients/<client-id>`, where `<client-id>` is the IDP Initiated SSO URL Name of the SAML client at the broker. Basic client settings can be imported from the SP Descriptor of the identity provider at the broker, adding `clients/<client-id>` to the endpoint URL.

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/saml/idp-initiated-login.adoc. Removed (not on the page): the "security reviews prefer SP-initiated" remark and the Verify step; added the documented `RelayState` parameter and brokering variant.
Method: documentation only; no commands were run.
