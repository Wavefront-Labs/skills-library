---
id: computing-software.collaboration-platform-administration.zulip.saml-authentication
name: saml-authentication
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [saml, saml-idp, social-auth-saml, saml-metadata]
level: advanced
status: docs-checked
description: "Set up SAML login in Zulip: SP entity ID, /complete/saml/ ACS URL, SOCIAL_AUTH_SAML_ENABLED_IDPS, certificates under /etc/zulip/saml and SAMLAuthBackend."
sources: ["https://zulip.readthedocs.io/en/latest/production/authentication-methods.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SAML authentication

1. Tell the IdP about Zulip. The SP Entity ID is `https://yourzulipdomain.example.com` and must match `SOCIAL_AUTH_SAML_SP_ENTITY_ID`; check it with `scripts/get-django-setting SOCIAL_AUTH_SAML_SP_ENTITY_ID`. The SSO (ACS) URL is `https://yourzulipdomain.example.com/complete/saml/`. With multiple organisations, use the `SOCIAL_AUTH_SUBDOMAIN` host instead.
2. In the "SAML Authentication" section of `/etc/zulip/settings.py`, set `SOCIAL_AUTH_SAML_ORG_INFO` and fill `SOCIAL_AUTH_SAML_ENABLED_IDPS`:
   - The outer key is an `idp_name` such as `okta`; it appears in URLs.
   - Take `url` and `entity_id` from the IdP.
   - Map the `attr_` fields to email and name; set `attr_user_permanent_id` to a stable unique identifier.
   - `display_name` and `display_icon` style the login button; `auto_signup` controls first-time logins.
3. Install the IdP certificate as `/etc/zulip/saml/idps/{idp_name}.crt`. Optionally add a Zulip certificate `zulip-cert.crt` (single X.509, not a chain) and an unencrypted `zulip-private-key.key` in `/etc/zulip/saml/`. Chown the tree to zulip, mode 644 for files and 640 for the key.
4. With the optional pair, `"authnRequestsSigned": True` in `SOCIAL_AUTH_SAML_SECURITY_CONFIG` signs requests, and some IdPs can encrypt assertions.
5. Add `zproject.backends.SAMLAuthBackend` to `AUTHENTICATION_BACKENDS` and restart.

The server metadata is served at `/saml/metadata.xml`, handy for verifying setup or handing to the IdP.

## Checked

Confirmed against the SAML section of the authentication-methods page: SP entity ID, the ACS URL and SOCIAL_AUTH_SUBDOMAIN variant, settings.py keys, certificate locations and permissions, authnRequestsSigned, the backend name and the metadata URL. Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/authentication-methods.md in the zulip/zulip repository (main), the source of the cited page.
