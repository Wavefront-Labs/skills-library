---
id: computing-software.data-engineering.metabase.ldap-auth
name: ldap-auth
category: computing-software
field: data-engineering
product: metabase
tags: [ldap, user-search-base, user-filter, group-mapping, starttls, provisioning]
level: practitioner
status: docs-checked
description: "Configure Metabase LDAP authentication: server and security settings, default attributes, user filter, search base, provisioning and manual group mappings."
sources:
  - https://www.metabase.com/docs/latest/people-and-groups/ldap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server settings: LDAP host (required, e.g. `ldap.yourdomain.org`); port 389 by default, or 636 for SSL; security None, SSL or StartTLS; optional Username or DN and Password for the lookup (bind) user. The Attributes section appears only after you save server settings.

Default attributes: email `mail` (required; without it Metabase cannot create the account), first name `givenname` and last name `sn` (missing values become "Unknown").

User schema: User search base is required, e.g. `ou=People,dc=widgetco,dc=com`. The default User filter is
`(&(objectClass=inetOrgPerson)(|(uid={login})(mail={login})))`
so it matches UID or email and needs objectClass `inetOrgPerson`; change it if your directory differs.

Provisioning: on by default, creating accounts and reactivating deactivated ones at login. When off, users without accounts cannot log in.

Group mapping: enable the toggle, then Manual group mappings, New, enter the LDAP group DN (e.g. `cn=Accounting,ou=Groups,dc=example,dc=org`) and pick Metabase groups. Group search base stays empty if each user entry lists its groups; otherwise set the DN of the group entries.

Gotchas:
- Membership changes apply only after the person logs in again.
- Sync adds and removes members only for mapped groups.
- The Administrators group maps like any other.
- The group membership filter (`{dn}`, `{uid}`) and attribute sync are Pro/Enterprise.
- Group schema settings and environment variables are not covered on this page.

## Checked
2026-11-03. Confirmed against the Metabase docs page People and groups, LDAP: server settings and ports, default attributes (mail, givenname, sn), Unknown name fallback, user search base example, default user filter, provisioning, group mapping steps and caveats, Pro/Enterprise membership filter and attribute sync. Nothing removed.
Method: documentation only; no commands were run.
