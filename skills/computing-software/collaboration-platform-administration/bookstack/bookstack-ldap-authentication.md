---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-ldap-authentication
name: bookstack-ldap-authentication
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, ldap, active-directory, auth-method, ldap-user-filter, group-sync, memberof, start-tls, ldaps]
level: advanced
status: docs-checked
description: "Authenticate BookStack against LDAP or Active Directory: .env settings, user filter and ID attribute, TLS options, group-to-role sync rules and lockout recovery."
sources: ["https://www.bookstackapp.com/docs/admin/ldap-auth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack LDAP authentication

Core `.env`: `AUTH_METHOD=ldap`, `LDAP_SERVER=example.com:389` (or `ldaps://example.com:636`), `LDAP_BASE_DN="ou=People,dc=example,dc=com"`, `LDAP_DN`/`LDAP_PASS` (both `false` for anonymous bind), `LDAP_VERSION=3`, `LDAP_USER_FILTER=(&(uid={user}))`, `LDAP_ID_ATTRIBUTE=uid` (prefix `BIN;` for binary), `LDAP_EMAIL_ATTRIBUTE=mail`, `LDAP_DISPLAY_NAME_ATTRIBUTE=cn` (join several with `|`), `LDAP_THUMBNAIL_ATTRIBUTE=jpegphoto`.

TLS: `LDAP_START_TLS=true`, `LDAP_TLS_CA_CERT` (PEM file or hashed directory), `LDAP_TLS_INSECURE=true` only for debugging (restart php-fpm after).

Active Directory: `LDAP_USER_FILTER=(&(sAMAccountName={user}))`, `LDAP_ID_ATTRIBUTE=BIN;objectGUID`, `LDAP_THUMBNAIL_ATTRIBUTE=thumbnailPhoto`.

Group sync: `LDAP_USER_TO_GROUPS=true`, `LDAP_GROUP_ATTRIBUTE="memberOf"`, `LDAP_REMOVE_FROM_GROUPS=true` to remove unmatched roles. Group names are lowercased with spaces turned into hyphens and matched to role names; a role's "External Authentication IDs" field overrides, comma-separated (escape commas with `\,`). Nested groups are followed; `memberOf` excludes the primary group; OpenLDAP needs the memberof overlay.

Troubleshooting: the php-ldap extension must be installed; `APP_DEBUG=true` briefly; `LDAP_DUMP_USER_DETAILS=true` and `LDAP_DUMP_USER_GROUPS=true` block logins, so use only temporarily. Locked out: set `AUTH_METHOD=standard`, log in, put your LDAP uid in your profile's External Authentication ID, switch back. If an LDAP uid changes, update that field.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/ldap-auth/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
