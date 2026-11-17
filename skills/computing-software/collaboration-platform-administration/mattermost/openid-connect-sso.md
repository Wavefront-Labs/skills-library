---
id: computing-software.collaboration-platform-administration.mattermost.openid-connect-sso
name: openid-connect-sso
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [openid-connect, oidc, sso, discovery-endpoint]
level: practitioner
status: docs-checked
description: "Configure a generic OpenID Connect provider in Mattermost: redirect URI, discovery endpoint, client credentials, button, preferred_username and limits."
sources: ["https://docs.mattermost.com/administration-guide/onboard/sso-openidconnect.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenID Connect single sign-on

Mattermost has OpenID Connect support for GitLab, Google Apps and Entra ID, plus a generic option for any other compliant provider.

Step 1, at the provider: create an OpenID Connect application. Most providers require every redirect URI to be authorised, so register {your-mattermost-url}/signup/openid/complete (for example http://domain.com/signup/openid/complete). Copy the Discovery Endpoint, Client ID and Client Secret.

Step 2, in Mattermost: System Console > Authentication > OpenID Connect, choose OpenID Connect (Other), enter the Discovery Endpoint, Client ID and Client Secret, set a Button Name and Button Color for the login page, Save, and restart the server for the change to show.

Notes:
- With OpenID Connect as the authentication source, first name, last name and username cannot be changed through the Mattermost API; the provider must be authoritative.
- An option called Use preferred username (in the provider's settings) makes Mattermost use the preferred_username claim of the token as the username.
- The Discovery Endpoint setting can be used to probe the connectivity and availability of arbitrary hosts, so admins concerned about that can limit who may edit the setting using custom admin roles.
- LDAP data is not compatible with OpenID: users who log in via OpenID cannot automatically get teams, channels, groups or attributes from LDAP.

Use the provider-specific pages (Google, Entra ID, GitLab) when one exists, and this generic path for other OIDC providers. Keep secrets out of shared notes with placeholders like <CLIENT_SECRET>.

## Checked

Confirmed against the OpenID Connect Single Sign-On page: supported providers, redirect URI path, the three values to copy, console steps and restart, the three notes (API-immutable attributes, preferred_username, Discovery Endpoint probing) and the LDAP FAQ. Removed the claim that provider pages prefill endpoints.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/sso-openidconnect page (source rst from the mattermost/docs repo).
