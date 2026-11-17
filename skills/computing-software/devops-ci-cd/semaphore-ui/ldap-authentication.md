---
id: computing-software.devops-ci-cd.semaphore-ui.ldap-authentication
name: ldap-authentication
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [ldap, active-directory, authentication, ldap-search-filter, semaphore-ui]
level: practitioner
status: docs-checked
description: "Configure LDAP or Active Directory sign-in with ldap_* options, search filter, mappings and claim expressions."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/ldap
  - https://semaphoreui.com/docs/reference/configuration
  - https://semaphoreui.com/docs/faq/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LDAP and Active Directory authentication

Goal: let directory users sign in to Semaphore.

```json
{
  "ldap_binddn": "cn=admin,dc=example,dc=org",
  "ldap_bindpassword": "admin_password",
  "ldap_server": "localhost:389",
  "ldap_searchdn": "ou=users,dc=example,dc=org",
  "ldap_searchfilter": "(&(objectClass=inetOrgPerson)(uid=%s))",
  "ldap_mappings": { "dn": "", "mail": "uid", "uid": "uid", "cn": "cn" },
  "ldap_enable": true,
  "ldap_needtls": false
}
```

These flat `ldap_*` options are the legacy single-directory configuration; the configuration reference adds `ldap_providers` (`SEMAPHORE_LDAP_PROVIDERS`) for several directories and `ldap_tls_skip_verify`. Mapping defaults are `dn`, `mail`, `uid` and `cn`.

Variables: `SEMAPHORE_LDAP_BIND_DN`, `SEMAPHORE_LDAP_BIND_PASSWORD`, `SEMAPHORE_LDAP_SERVER`, `SEMAPHORE_LDAP_SEARCH_DN`, `SEMAPHORE_LDAP_SEARCH_FILTER`, `SEMAPHORE_LDAP_MAPPING_DN`, `..._MAIL`, `..._UID`, `..._CN`, `SEMAPHORE_LDAP_ENABLE=yes`.

`%s` in the search filter is replaced by the login typed by the user. The default filter is `(&(objectClass=inetOrgPerson)(uid=%s))`.

Mappings accept claim expressions: `email | {{ .username }}@your-domain.com` tries the email attribute and falls back to the template when empty. The expression `|` for `uid` generates a random username per user.

Example for a test OpenLDAP (bitnami image on port 1389) uses `"mail": "{{ .cn }}@ldap.your-domain.com"`, `"uid": "|"`, `"cn": "cn"`.

Check the bind account with `ldapwhoami -H ldap://ldap.com:389 -D "CN=binddn" -x -W`; it should exit 0 and echo the DN. If you see `unable to read LDAP response packet: unexpected EOF`, you are probably connecting insecurely to a TLS-only server; the troubleshooting page's fix is setting `ldap_needtls` to true when the server expects TLS. For LDAP result code 49 check the password and bind DN; for code 32 check `ldap_searchdn` (a wrong search base) with `ldapsearch -s base`, and if that returns 0 the `ldap_searchfilter` matches nothing.

Verify: sign in with a directory user and confirm the account appears in the user list.

## Checked

2026-11-04: checked against the LDAP page, configuration reference and troubleshooting page. Noted that flat ldap_* options are the legacy single-directory form, listed the mapping defaults, and replaced an awkward cross-reference with the documented result code 49 and 32 fixes.

Method: documentation only; no commands were run.
