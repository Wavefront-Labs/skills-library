---
id: computing-software.systems-network-administration.apache-guacamole.ldap-auth-config
name: ldap-auth-config
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, ldap, active-directory, ldap-auth, ldap-user-base-dn, ldap-search-bind-dn, ldap-encryption-method, ldap-group-base-dn, sam-account-name]
level: practitioner
status: docs-checked
description: "Configure Guacamole LDAP/Active Directory authentication: install, ldap-* properties and defaults, search-bind vs direct DN, groups, sAMAccountName, and databases."
sources:
  - https://guacamole.apache.org/doc/gug/ldap-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP / Active Directory authentication

Install: copy `guacamole-auth-ldap-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`, restart Tomcat. Docker: `LDAP_ENABLED=true` plus uppercase `LDAP_*` variables.

Core properties (default):
- `ldap-hostname` (localhost), `ldap-port` (389; 636 for LDAPS), `ldap-encryption-method` (`none`, `ssl`, `starttls`), `ldap-ssl-protocol` (latest, TLSv1.3)
- `ldap-user-base-dn` (**required**), `ldap-username-attribute` (usually `uid`; the manual's Active Directory examples use `sAMAccountName`)
- `ldap-search-bind-dn`, `ldap-search-bind-password`, `ldap-user-search-filter` (`(objectClass=*)`)
- `ldap-group-base-dn` (omit and LDAP groups do not affect permissions), `ldap-group-name-attribute` (`cn`), `ldap-group-search-filter`, `ldap-member-attribute` (`member`), `ldap-member-attribute-type` (`dn` or `uid`)
- `ldap-max-search-results` 1000, `ldap-dereference-aliases` never, `ldap-follow-referrals` false, `ldap-max-referral-hops` 5, `ldap-operation-timeout` 30 s
- `ldap-user-attributes` exposes attributes as `${LDAP_...}` tokens

Bind logic: without a search DN the login DN is `username-attribute=user,user-base-dn`, so users must sit directly in the base. With a search bind account the user can be anywhere under the base; the search account only resolves the DN, then all queries run as the user. Multiple username attributes need a search DN.

Pair with a database for connections and permissions; the LDAP username must match the database username (apache-guacamole.database-auth-overview). For several directories see apache-guacamole.ldap-multi-server; for connections stored in LDAP see apache-guacamole.ldap-connection-storage.

Verify: an AD user logs in with `sAMAccountName`.

## Checked

2026-11-04. Confirmed against the Guacamole manual page ldap-auth: required ldap-user-base-dn, defaults for hostname (localhost), port (389, 636 for LDAPS), encryption methods none/ssl/starttls, ssl protocol TLSv1.3, max results 1000, member attribute and type, group search filter default, dereference aliases never, follow referrals false, max hops 5, operation timeout 30 seconds, search-bind behaviour (search DN only resolves the DN; later queries use the user's credentials), multiple username attributes needing a search DN, ldap-group-base-dn omission, LDAP_ tokens from ldap-user-attributes, and the sAMAccountName examples. Changed: the database pairing statement now says the usernames must match; removed the unsupported verify clause about a wrong base DN.

Method: documentation only; no commands were run.
