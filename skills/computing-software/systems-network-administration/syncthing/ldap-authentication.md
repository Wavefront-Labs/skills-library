---
id: computing-software.systems-network-administration.syncthing.ldap-authentication
name: ldap-authentication
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, ldap, authentication, active-directory]
level: advanced
status: docs-checked
description: "Configure Syncthing GUI authentication against LDAP or Active Directory, including Bind DN, transport and group filters."
sources: ["https://docs.syncthing.net/users/ldap.html", "https://docs.syncthing.net/users/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP authentication for the GUI

## Settings
Open Actions > Advanced, expand the LDAP tab and set:
- `Address`: LDAP server host name and port, for example `dc1.example.com:389` or `dc1.example.com:636`.
- `Transport`: `plain` (389), `tls` (LDAPS, 636) or `starttls` (usually 389).
- `Bind DN`: pattern for the bind user; the token `%s` stands for the username entered at the login prompt. Examples: `%s@ad.example.com` for Active Directory, `CN=%s,CN=Users,DC=example,DC=com` for standard LDAP servers.
- `Insecure Skip Verify`: disables all certificate verification for LDAPS. Use with care and only when absolutely necessary.
- `Search Base DN` and `Search Filter`: optional, base DN and filter for user searches (see below).

Once these are correct, LDAP authentication must be enabled by setting the authentication mode (`authMode`) to `ldap` in the advanced GUI configuration.

## Restricting to a group
Added in version 1.5.0. Enter the base DN under which users are stored in Search Base DN, and build a search filter that matches both the user ID and the group membership. For an Active Directory setup with a group `Syncthing` in the standard location:

```
(&(sAMAccountName=%s)(memberOf=CN=Syncthing,CN=Users,DC=example,DC=com))
```
Line breaks are for clarity only in the docs; enter it as one long string. The group DN, the membership attribute and the user ID attribute vary with the LDAP schema: AD uses `memberOf` and `sAMAccountName`, others may use `CN` or `UID`.

## Checked
2026-11-04. Read the LDAP Authentication page and the config page (`authMode`): each setting, transport values and ports, `%s` token, enabling step, group filter and version 1.5.0. Removed the Cautions section (generic advice and a cross-reference the page does not make).
Method: documentation only; no commands were run.
