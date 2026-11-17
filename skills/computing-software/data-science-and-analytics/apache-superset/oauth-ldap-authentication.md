---
id: computing-software.data-science-and-analytics.apache-superset.oauth-ldap-authentication
name: oauth-ldap-authentication
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [oauth, ldap, auth-type, role-mapping, auth-roles-sync]
level: practitioner
status: docs-checked
description: "Configure external login for Superset: AUTH_TYPE, OAUTH_PROVIDERS, PKCE, LDAP, AUTH_ROLES_MAPPING and AUTH_ROLES_SYNC_AT_LOGIN behaviour."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/configuring-superset.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/oauth.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate Superset users against an identity provider.

Superset is built on Flask-AppBuilder (FAB), which supplies authentication. OAuth2 needs the `Authlib` package on the web server. Set `AUTH_TYPE = AUTH_OAUTH` (from `flask_appbuilder.security.manager`).

OpenID Connect provider with a discovery document:

```python
OAUTH_PROVIDERS = [{
    "name": "myProvider",
    "token_key": "access_token",
    "icon": "fa-address-card",
    "remote_app": {
        "client_id": "myClientId",
        "client_secret": "MySecret",
        "server_metadata_url": "https://myAuthorizationServer/.well-known/openid-configuration",
        "code_challenge_method": "S256",
    },
}]
```

- With `server_metadata_url` you do not need `api_base_url`, `access_token_url`, `authorize_url` or the user info and JWKS endpoints. Otherwise give those explicitly (plus `client_kwargs` scope).
- `code_challenge_method: "S256"` enables PKCE; the docs recommend it for all OAuth2 flows, even with a client secret. In the Keycloak example it sits in `client_kwargs`; see the Keycloak skill.
- Redirect URL to register: `https://<superset-webserver>/oauth-authorized/<provider-name>`.
- For providers that return a non-standard user payload, subclass `SupersetSecurityManager`, override `oauth_user_info` and set `CUSTOM_SECURITY_MANAGER` (module placed next to `superset_config.py`).

Self-registration and roles:
- `AUTH_USER_REGISTRATION = True` creates users from authorised users; `AUTH_USER_REGISTRATION_ROLE` (example `"Public"`) is the default role. If a new Admin cannot list users, re-run `superset init`.
- `AUTH_ROLES_MAPPING` maps provider group names (OAuth) or group DNs (LDAP, for example `"cn=superset_users,ou=groups,dc=example,dc=com"`) to lists of roles, e.g. `{"superset_users": ["Gamma", "Alpha"], "superset_admins": ["Admin"]}`.
- `AUTH_ROLES_SYNC_AT_LOGIN = True` syncs roles on every login; `False` syncs only at first registration.

LDAP: FAB can authenticate against an LDAP server; install the `python-ldap` package. LDAP group mapping requires `AUTH_LDAP_SEARCH` to be set; the rest of the LDAP settings are in the FAB security docs.

Behind a TLS proxy set `ENABLE_PROXY_FIX = True` (see the Gunicorn and proxy skill).

## Checked

2026-11-08. Confirmed against the Configuring Superset page (Custom OAuth2, PKCE, LDAP and role mapping sections read) and the OAuth Configuration page (read in full). Removed: the Keycloak-specific provider example with `fa-key`, `AUTH_LDAP_*` as a settings family (only `AUTH_LDAP_SEARCH` is named), and the claim that removing a group at the provider removes the role (the page only says roles are synced at login).
Method: documentation only; no commands were run.
