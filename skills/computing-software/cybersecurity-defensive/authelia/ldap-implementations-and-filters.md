---
id: computing-software.cybersecurity-defensive.authelia.ldap-implementations-and-filters
name: ldap-implementations-and-filters
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, ldap, active-directory, freeipa, lldap, glauth, rfc2307bis, users-filter, groups-filter]
level: advanced
status: docs-checked
description: "Select an Authelia LDAP implementation preset and write users_filter, groups_filter and attribute mappings with the documented placeholders."
sources:
  - https://www.authelia.com/configuration/first-factor/ldap/
  - https://www.authelia.com/integration/ldap/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`implementation` loads sensible defaults for filters and attributes so you only override what differs. Available values: `custom` (not provider-specific), `activedirectory` (also uses the special password change encoding Active Directory needs), `rfc2307bis`, `freeipa`, `lldap` and `glauth`.

```yaml
authentication_backend:
  ldap:
    implementation: 'custom'
    additional_users_dn: 'OU=users'
    users_filter: '(&({username_attribute}={input})(objectClass=person))'
    additional_groups_dn: 'OU=groups'
    groups_filter: '(&(member={dn})(objectClass=groupOfNames))'
    attributes:
      username: 'uid'
      display_name: 'displayName'
      mail: 'mail'
      member_of: 'memberOf'
      group_name: 'cn'
```

- `base_dn` is prefixed with `additional_users_dn` for user searches and `additional_groups_dn` for groups, letting you restrict searches to an OU.
- `users_filter` must exclude disabled accounts. The username attribute must appear in it through the `{username_attribute}` placeholder.
- Filter placeholders are replaced either at startup (the `{..._attribute}` ones: `{distinguished_name_attribute}`, `{username_attribute}`, `{mail_attribute}`, `{display_name_attribute}`, `{member_of_attribute}`) or at search time (`{input}`; in users filters `{date-time:generalized}`, `{date-time:unix}`, `{date-time:microsoft-nt}`; in groups filters `{username}`, `{dn}`, `{memberof:dn}`, `{memberof:rdn}`).
- `users_filter` and `groups_filter` are technically required but implementations set defaults; the same holds for `attributes.username`, `display_name`, `mail`, `member_of` and `group_name`. The defaults per implementation live on other pages not read here.
- For nested groups on Active Directory, the docs suggest a groups filter with the `1.2.840.113556.1.4.1941` matching rule: `(&(member:1.2.840.113556.1.4.1941:={dn})(objectClass=group)(objectCategory=group))`.
- Custom attributes can be loaded with `attributes.extra`: the key is the directory attribute, `name` (optional) renames it inside Authelia, `value_type` (required: `string`, `integer` or `boolean`; integer and boolean values must parse) and `multi_valued` (optional).

Check: log in as a user in a nested group and confirm a group-based access control rule matches.

## Checked

2026-11-08. Read in full: first-factor/ldap, integration/ldap/introduction. Added the full placeholder list with phases and extra attribute rules.

Method: documentation only; no commands were run.
