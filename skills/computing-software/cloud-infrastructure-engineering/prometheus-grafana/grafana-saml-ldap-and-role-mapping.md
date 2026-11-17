---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-saml-ldap-and-role-mapping
name: grafana-saml-ldap-and-role-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-sso, grafana-saml, saml-configuration, saml-role-mapping, grafana-ldap, ldap-configuration, ldap-toml, ldap-group-mapping, role-mapping-jmespath, org-mapping]
level: advanced
status: docs-checked
description: "Configure Grafana SAML (assertion attributes, role and org mapping) and LDAP (ldap.toml, group mappings), plus JMESPath role mapping for OAuth providers."
sources: ["https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/saml/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/saml/saml-configuration-options/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/saml/configure-saml-org-mapping/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/saml/configure-saml-team-role-mapping/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/saml/troubleshoot-saml/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/ldap/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-access/configure-authentication/generic-oauth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML, LDAP and role mapping

## SAML (Enterprise and Cloud)
SAML is available in Grafana Enterprise and Grafana Cloud. Settings can come from the config file (not on Cloud), the
SSO Settings API, the SAML UI or the Terraform provider; settings stored through the API or UI take precedence over the
file, so a file change that "does nothing" usually means stored settings exist.
```ini
[auth.saml]
enabled = true
certificate_path = /etc/grafana/saml/sp.crt
private_key_path = /etc/grafana/saml/sp.key
idp_metadata_url = https://idp.example.com/app/xyz/sso/saml/metadata
assertion_attribute_name = displayName
assertion_attribute_login = mail
assertion_attribute_email = mail
assertion_attribute_groups = groups      # team sync: one AttributeValue per group
assertion_attribute_role = role          # IdP attribute holding role values
role_values_editor = grafana-editors
role_values_admin = grafana-admins
role_values_grafana_admin = grafana-superadmins
assertion_attribute_org = groups
org_mapping = sre-team:1:Editor, customer-a:2:Viewer
allow_idp_initiated = false
```
- Register Grafana with the IdP using `/saml/metadata` (SP metadata, also called Identifier or Entity ID) and
  `/saml/acs` (the ACS callback, also called SSO URL or Reply URL).
- `idp_metadata` is base64 XML, `idp_metadata_path` a file path, `idp_metadata_url` a URL.
- Defaults: `assertion_attribute_name` displayName, `assertion_attribute_login` and `_email` mail,
  `allow_idp_initiated` false, `max_issue_delay` 90s, `metadata_valid_duration` 48h.
- The private key must be PKCS#8; `asn1: structure error: tags don't match` means another format. A base64-encoded
  value can be given in `certificate` and `private_key`.
- `org_mapping` entries are `Organization:OrgId:Role`; `*` matches all users or all Grafana orgs (`Engineering:*`).
  Since Grafana 11.5 an org name can replace the id; with spaces use the JSON form
  `["Org 1:2:Editor", "ExternalOrg:ACME Corp.:Admin"]`.
- Role sync overwrites manual role and org changes at next login; `skip_org_role_sync = true` turns it off. A user
  matching no `role_values_*` gets `auto_assign_org_role` (Viewer if unset).
- Team sync needs teams created in Grafana first; each group must be its own AttributeValue, not a delimited list.
- Redirect loop after IdP login: `security.cookie_samesite = lax`. "origin not allowed" behind a proxy:
  `csrf_trusted_origins` or `csrf_additional_headers`. Debug log: `[log] filters = saml.auth:debug`.

## LDAP
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
bind_dn = "cn=grafana,ou=svc,dc=example,dc=com"
bind_password = "${LDAP_BIND_PASSWORD}"
search_filter = "(sAMAccountName=%s)"
search_base_dns = ["dc=example,dc=com"]
[servers.attributes]
username = "sAMAccountName"
email = "mail"
member_of = "memberOf"
[[servers.group_mappings]]
group_dn = "cn=grafana-admins,ou=groups,dc=example,dc=com"
org_role = "Admin"
[[servers.group_mappings]]
group_dn = "*"
org_role = "Viewer"
```
- Restart Grafana after editing `ldap.toml`. The bind user should be read-only; a second bind then uses the user's
  own credentials. `skip_org_role_sync = true` under `[auth.ldap]` keeps roles manual.
- Group mappings sync at every login with LDAP authoritative. The first mapping a user matches is used, so order
  specific to general. `org_role` (case-sensitive Admin, Editor or Viewer) and `group_dn` are required; `org_id`
  defaults to 1; `grafana_admin = true` grants server admin.
- If the server has no `memberOf`, use `group_search_filter`, `group_search_base_dns` and
  `group_search_filter_user_attribute`. Nested AD groups use the `1.2.840.113556.1.4.1941` matching rule.
- Debug: `[log] filters = ldap:debug`. LDAP can also be configured under Administration > Authentication > LDAP.

## Role mapping for OAuth/OIDC (JMESPath)
```ini
role_attribute_path = contains(groups[*], 'grafana-admins') && 'Admin' || contains(groups[*], 'grafana-editors') && 'Editor' || 'Viewer'
role_attribute_strict = true          # deny login if no role resolves
org_attribute_path = groups
org_mapping = sre:1:Editor payments:2:Viewer
skip_org_role_sync = false            # true stops syncing so roles are set in Grafana
```
- Grafana evaluates `role_attribute_path` on the ID token, then the UserInfo data, then the access token. The result
  must be None, Viewer, Editor, Admin or GrafanaAdmin; GrafanaAdmin takes effect only with
  `allow_assign_grafana_admin = true`.
- With no valid role the user gets `auto_assign_org_role`; `role_attribute_strict = true` denies login instead.
- `org_attribute_path` must return an array. If both `org_mapping` and `role_attribute_path` apply, the user gets the
  higher role. Org mapping is not supported on Cloud.

## Verify
- [ ] Users in each IdP group land with the expected role/org on first login.
- [ ] Removing a group membership downgrades the role at next login.

## Checked
Checked 2026-11-08 against the Grafana docs pages listed in sources (SAML overview, configuration options, org mapping,
team and role sync, troubleshooting, LDAP, Generic OAuth). Removed: the "assertion expired" clock-skew remark, the
"Test LDAP mapping" admin menu path and the "sign requests with the SP key" remark (none stated on those pages);
fixed the LDAP mapping rule and added documented defaults. The Okta, Entra ID and SCIM steps were not reviewed.
Method: documentation only; no commands were run.
