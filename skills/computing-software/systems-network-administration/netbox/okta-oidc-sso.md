---
id: computing-software.systems-network-administration.netbox.okta-oidc-sso
name: okta-oidc-sso
category: computing-software
field: systems-network-administration
product: netbox
tags: [okta, oidc, social-auth]
level: advanced
status: docs-checked
description: "Register an OIDC app in Okta and set the social_core backend in configuration.py."
sources: ["https://netboxlabs.com/docs/netbox/administration/authentication/okta/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Okta SSO

Goal: sign users in to NetBox with Okta.

**Okta side**

1. Optionally create a test user.
2. In the admin dashboard go to Applications > Applications and choose Create App Integration.
3. Select **OIDC** as the sign-in method and **Web application** as the type.
4. Name it (for example "NetBox") and set the URIs:
   - Sign-in: `https://{netbox}/oauth/complete/okta-openidconnect/`
   - Sign-out: `https://{netbox}/oauth/disconnect/okta-openidconnect/`
5. Under Assignments choose the access control that fits your organisation, then save.
6. Note the Client ID, Client secret and Okta domain.

**NetBox side** (`configuration.py`):

```python
REMOTE_AUTH_BACKEND = 'social_core.backends.okta_openidconnect.OktaOpenIdConnect'
SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY = '{Client ID}'
SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET = '{Client secret}'
```

The guide also sets `SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL` from your Okta domain; copy that line from the official page.

Keep the client secret out of version control, for example by reading it from the environment.

**Checklist**

1. Redirect URIs match exactly.
2. Backend set as shown.
3. Test with a non-admin user.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Okta authentication page: OIDC web application steps, redirect URIs with okta-openidconnect, backend path and SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY/SECRET. Removed: Nothing.

Method: documentation only; no commands were run.
