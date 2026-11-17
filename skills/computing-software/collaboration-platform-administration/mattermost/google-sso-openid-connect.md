---
id: computing-software.collaboration-platform-administration.mattermost.google-sso-openid-connect
name: google-sso-openid-connect
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [google-sso, openid-connect, oauth-client, people-api]
level: practitioner
status: docs-checked
description: "Configure Google as a Mattermost SSO provider through OpenID Connect: OAuth client, redirect URI, People API, console and config.json settings."
sources: ["https://docs.mattermost.com/administration-guide/onboard/sso-google.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Google single sign-on

Step 1, in Google Cloud Platform, Credentials: Create Credentials > OAuth client ID, application type Web application, name it Mattermost-<your-company-name>, and under Authorized redirect URIs add {your-mattermost-url}/signup/google/complete (for a local test, http://localhost:8065/signup/google/complete). Create it and copy the Client ID and Client Secret somewhere temporary.

Step 2: enable the Google People API (it replaced the deprecated Google+ API); propagation can take a few minutes.

Step 3, in Mattermost: System Console > Authentication > OpenID Connect, choose Google Apps as the service provider. The Discovery Endpoint is prepopulated with Google's well-known openid-configuration URL. Paste the Client ID and Client Secret and Save.

Alternative: edit the GoogleSettings block in config.json (usually under /opt/mattermost/config, edited as root). Fields: Enable, Secret, Id, Scope ("profile openid email"), AuthEndpoint, TokenEndpoint, UserApiEndpoint, DiscoveryEndpoint, ButtonText and ButtonColor. Use <API_KEY>-style placeholders for the secret in any shared notes, save, and restart; users must then change their sign-in method before they can log in with Google.

Limits: with OpenID Connect or OAuth 2.0 authentication, first name, last name and username cannot be changed through the Mattermost API, and username or email changes made in Google Workspace are not synced into Mattermost automatically. LDAP attributes and groups are not compatible with OpenID, so team and channel membership driven by LDAP will not apply to those users automatically.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/onboard/sso-google (steps, GoogleSettings, FAQ). Nothing removed.

Method: documentation only; no commands were run.
