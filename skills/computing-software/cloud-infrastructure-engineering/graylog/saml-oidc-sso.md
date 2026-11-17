---
id: computing-software.cloud-infrastructure-engineering.graylog.saml-oidc-sso
name: saml-oidc-sso
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [saml, oidc, single-sign-on, authentication-services, identity-provider]
level: practitioner
status: docs-checked
description: "Configure SAML or OIDC single sign-on in Graylog at System > Authentication, including tested providers and required OIDC claims."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/saml_authentication.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/oidc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# saml oidc sso

Administrator task at **System > Authentication > Create service**. You need credentials from the identity provider and access to both consoles.

**SAML** tested providers: Auth0, Entra ID, Keycloak, Okta. Create the SSO integration in the IdP (an enterprise application in Entra ID, an app integration in Okta), then enter its details in Graylog. SAML group members can sync to Graylog teams.

**OIDC** tested providers: Auth0, Entra ID, Google, Keycloak, Ping, OneLogin. The page lists `openid`, `profile` and `email` as required parameters. Graylog reads the ID token or UserInfo endpoint and requires the claim `preferred_username` or `email`. Fields include Title, optional Description and OIDC base URL. With multiple Graylog instances, create a separate application in the IdP for each.

Group sync to teams is a Graylog Enterprise feature, as are the SAML and OIDC pages themselves. OIDC group sync reads a claim named `graylog_teams` unless you set another claim name.

After saving, click Activate on the Authentication Services page; only one authentication service can be active per Graylog instance. If the IdP blocks you, use Login with default method to sign in with the default administrator credentials. Synced users get the Reader role by default.

Provider specifics: with Google OIDC, add an `hd` claim matching your domain, or anyone with an authenticated Google account can sign in. With Entra ID, add the `email` optional claim to the ID token. For SAML, the Entity ID must be identical in Graylog and the IdP, and the page recommends adding Graylog's certificate to the IdP.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/setting_up_graylog/saml_authentication.htm and https://go2docs.graylog.org/current/setting_up_graylog/oidc.html (both read in full, Graylog 7.2 docs). Reworded "scopes" to "parameters" as the page words it.
