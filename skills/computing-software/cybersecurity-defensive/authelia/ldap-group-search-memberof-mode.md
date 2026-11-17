---
id: computing-software.cybersecurity-defensive.authelia.ldap-group-search-memberof-mode
name: ldap-group-search-memberof-mode
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, ldap, memberof, group-search-mode, distinguished-name, groups-filter]
level: sme
status: docs-checked
description: "Decide between Authelia's filter and experimental memberof group search modes and satisfy the memberOf mode's distinguished name requirements."
sources:
  - https://www.authelia.com/integration/ldap/introduction/
  - https://www.authelia.com/configuration/first-factor/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`group_search_mode` controls how a user's groups are discovered.

```yaml
authentication_backend:
  ldap:
    group_search_mode: 'filter'
```

`filter` is the default and is generally recommended: the `groups_filter` is run directly and its results are the user's groups.

`memberof` is documented as generally discouraged and experimental. It works for directories that populate a `memberOf` attribute on users, possibly including indirect groups. Authelia searches the base with subtree scope using a groups filter that must contain one of the `{memberof:*}` replacements, then compares the distinguished names of the results, case-insensitively, against the user's `memberOf` values.

Requirements that follow from this:

1. The groups still have to sit inside the configured search base.
2. The `memberOf` attribute must contain the group's distinguished name.
3. If you use the `{memberof:dn}` replacement, the directory must be able to search on the distinguished name, which requires `attributes.distinguished_name`. The page says only Active Directory is known to support such an attribute.
4. For the `{memberof:rdn}` replacement (memberof mode only), the directory must support searching on the first relative distinguished name as an attribute. Authelia splits each `memberOf` value into its first RDN and joins them in parentheses, so the suggested filter `(|{memberof:rdn})` becomes `(|(CN=abc)(CN=xyz))`.

The `attributes.member_of` setting is currently used only by this mode. The pages do not say what happens when a requirement is unmet; the likely effect is missing groups, so group-based access control rules would not match.

Stay on `filter` unless a directory cannot answer a membership filter. Nested group support on Active Directory is possible with the `filter` mode via a matching-rule filter, which the page says has only been tested against Microsoft Active Directory.

Check: log in as a user who belongs to a known group and confirm a group-based access control rule matches.

## Checked

2026-11-08. Read in full: first-factor/ldap, integration/ldap/introduction. Corrected the requirement list (the RDN requirement belongs to the memberof:rdn replacement) and removed unsupported header claims.

Method: documentation only; no commands were run.
