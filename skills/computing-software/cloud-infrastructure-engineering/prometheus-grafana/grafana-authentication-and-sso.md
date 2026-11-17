---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-authentication-and-sso
name: grafana-authentication-and-sso
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, grafana-sso, grafana-oauth, grafana-oidc, grafana-saml, grafana-ldap, generic-oauth, azure-ad, entra-id, okta, github-oauth, google-oauth, keycloak, role-attribute-path, jmespath, team-sync, auth-proxy, anonymous-access, disable-login-form, sso-settings-api, pkce, refresh-tokens, login-security]
level: advanced
status: docs-checked
description: "Configure Grafana login against your IdP: generic OAuth/OIDC with JMESPath role mapping, Entra ID specifics, SAML, LDAP, team sync, auth proxy, and locking out local access."
sources: ["https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/generic-oauth/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/saml/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/saml/saml-configuration-options/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/ldap/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/azuread/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/auth-proxy/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/anonymous-auth/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/", "https://grafana.com/docs/grafana/latest/administration/cli/"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Authentication and SSO

**Goal:** users log in with the company IdP, land in the right org with the right basic
role and teams automatically, and no one can bypass it with a local account.

## 1. Generic OAuth / OIDC (Keycloak, Entra ID, Okta, Auth0…)
```ini
[server]
root_url = https://grafana.example.com    # must match the IdP redirect URI exactly: <root_url>/login/generic_oauth

[auth.generic_oauth]
enabled = true
name = Company SSO
allow_sign_up = true
auto_login = true                          # skip the login page
client_id = grafana
client_secret = $__file{/etc/grafana/secrets/oauth-client-secret}
scopes = openid profile email groups
auth_url  = https://idp.example.com/realms/corp/protocol/openid-connect/auth
token_url = https://idp.example.com/realms/corp/protocol/openid-connect/token
api_url   = https://idp.example.com/realms/corp/protocol/openid-connect/userinfo
use_pkce = true
use_refresh_token = true
login_attribute_path = preferred_username
email_attribute_path = email
name_attribute_path = name
groups_attribute_path = groups
role_attribute_path = contains(groups[*], 'grafana-admins') && 'Admin' || contains(groups[*], 'grafana-editors') && 'Editor' || 'Viewer'
role_attribute_strict = true               # deny login if no role maps
allow_assign_grafana_admin = false
allowed_domains = example.com
allowed_groups = grafana-users grafana-admins grafana-editors
tls_skip_verify_insecure = false
```
- `role_attribute_path` is a **JMESPath** expression evaluated against the user info; test it against a sample token JSON.
  Org-specific mapping: `org_mapping` takes a comma- or space-separated list of `<ExternalName>:<OrgIdOrName>:<Role>`
  (`*` matches all users). If both `org_mapping` and `role_attribute_path` are set, the user gets the highest mapped role.
  `role_attribute_strict = true` also applies to `org_mapping` results.
- Groups claims must actually be in the token: Entra ID needs `groupMembershipClaims` in the app manifest and
  references groups by object id (use the id in the JMESPath and in `allowed_groups`). Configure the equivalent
  groups claim in other IdPs.
- Roles are synced from the provider at every login unless `skip_org_role_sync = true` is set for that provider (then admins
  manage org roles in Grafana). The global `[auth] oauth_skip_org_role_update_sync` is deprecated; use the per-provider setting.

### Provider shortcuts
Dedicated sections exist for `[auth.azuread]` (Entra ID), `[auth.github]`, `[auth.gitlab]`, `[auth.google]` and `[auth.okta]`;
`allowed_organizations`, `allowed_domains` and `team_ids` gate who may log in.
SSO settings can be stored in the Grafana database (UI, SSO settings API, Terraform). Settings stored in the database
take precedence over the configuration file, which surprises people during credential rotation; if a file change has
no effect, check for stored settings.

## 2. SAML (Enterprise / Cloud)
```ini
[auth.saml]
enabled = true
certificate_path = /etc/grafana/saml/sp.crt
private_key_path = /etc/grafana/saml/sp.key
idp_metadata_url = https://idp/metadata.xml       # or idp_metadata_path
assertion_attribute_name = displayName
assertion_attribute_login = login
assertion_attribute_email = email
assertion_attribute_groups = groups
assertion_attribute_role = role
role_values_admin = grafana-admins
role_values_editor = grafana-editors
role_values_none = guests
allow_idp_initiated = false
single_logout = true
```
Grafana exposes SP metadata at `/saml/metadata` and receives the ACS callback at `/saml/acs`. The IdP metadata
setting takes a suffix: none means base64-encoded XML, `_path` a file path, `_url` a URL.

## 3. LDAP / Active Directory
```ini
[auth.ldap]
enabled = true
config_file = /etc/grafana/ldap.toml
allow_sign_up = true
```
```toml
[[servers]]
host = "ldap.example.com"
port = 636
use_ssl = true
root_ca_cert = "/etc/grafana/ldap-ca.pem"
bind_dn = "cn=grafana,ou=svc,dc=example,dc=com"
bind_password = "$__file{/etc/grafana/secrets/ldap}"
search_filter = "(sAMAccountName=%s)"
search_base_dns = ["ou=people,dc=example,dc=com"]
group_search_filter = "(member:1.2.840.113556.1.4.1941:=%s)"   # AD nested groups
group_search_base_dns = ["ou=groups,dc=example,dc=com"]
group_search_filter_user_attribute = "distinguishedName"
[servers.attributes]
name = "givenName"
surname = "sn"
username = "sAMAccountName"
member_of = "memberOf"
email = "mail"
[[servers.group_mappings]]
group_dn = "cn=grafana-admins,ou=groups,dc=example,dc=com"
org_role = "Admin"
grafana_admin = true
[[servers.group_mappings]]
group_dn = "*"
org_role = "Viewer"
```
Debug at *Administration → Authentication → LDAP* (test a username, see mapped groups).

## 4. Team sync and auth proxy
- **Team Sync** (Enterprise/Cloud): on a team, map external group ids (`groups` claim value,
  SAML group, LDAP DN); membership is reconciled at login. OSS alternative: provision team
  membership via API from your IdP export.
- **Auth proxy** (`[auth.proxy] enabled=true header_name=X-WEBAUTH-USER headers=Email:X-WEBAUTH-EMAIL,Groups:X-WEBAUTH-GROUPS whitelist=10.0.0.0/8`)
  trusts a header set by an upstream SSO proxy (oauth2-proxy, Pomerium). Set `whitelist` (IPs or CIDRs) to
  prevent users spoofing the header; it ships empty, and without it anyone who can reach Grafana can forge the header.

## 5. Lock the doors
```ini
[auth]
disable_login_form = true        # hide user/pass (keep false until SSO is proven)
disable_signout_menu = false
login_maximum_inactive_lifetime_duration = 7d
login_maximum_lifetime_duration = 30d
[auth.anonymous]
enabled = false                  # or true with org_role = Viewer + org_name for a public kiosk org only
[auth.basic]
enabled = false
[security]
admin_user = admin
admin_password = $__file{/etc/grafana/secrets/admin}   # keep a break-glass local admin; store it in the vault
cookie_secure = true
cookie_samesite = lax
```
Break-glass: `/login?disableAutoLogin=true` bypasses `auto_login` so you can reach the login screen and fix a
misconfiguration (documented for OAuth and SAML); or `grafana cli admin reset-admin-password <new password>`.

## Gotchas
- Redirect URI mismatch (`http` vs `https`, trailing slash, wrong `root_url` behind a proxy)
  is the top failure; set `[server] root_url` and, behind a reverse proxy, `serve_from_sub_path`.
- With `allow_sign_up = false` only existing Grafana users can log in through that provider; decide sign-up policy first.
- Role sync resets users who were manually promoted unless `skip_org_role_sync` is set; tell them.
- Email is required for sign-up with Generic OAuth even when login maps from another claim; use the `email` scope or `email_attribute_path`.
- Entra ID does not emit the groups claim for users in more than 200 groups (it emits an overage claim instead); Grafana
  then fetches groups from the Microsoft Graph API (`force_use_graph_api` always does).

## Verify
- [ ] A new user from the IdP lands in the correct org with the expected role and teams, with no manual steps.
- [ ] Removing the user from the IdP group demotes them on next login.
- [ ] `/login` shows only the SSO button (or auto-redirects); basic auth is disabled for API calls.
- [ ] Break-glass admin login works and its password is in the vault, not in a wiki.

## Checked

2026-11-08. Confirmed against the Grafana docs pages in sources: generic OAuth options, JMESPath role mapping, org_mapping and role_attribute_strict; Entra ID group object ids, the 200-group overage and force_use_graph_api; SAML endpoints, IdP metadata suffixes and option names; LDAP option names; auth proxy header and whitelist settings; disable_login_form, session lifetimes, anonymous org_name and org_role; disableAutoLogin; the grafana cli reset command; stored SSO settings precedence. Removed or reworded unsupported claims (Keycloak and Okta group claim setup, mandatory whitelist, login_attribute_path creating new users, 401 from basic auth, clock sync). LDAP example values were matched by option name only.

Method: documentation only; no commands were run.
