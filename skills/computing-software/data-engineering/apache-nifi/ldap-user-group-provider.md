---
id: computing-software.data-engineering.apache-nifi.ldap-user-group-provider
name: ldap-user-group-provider
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, ldap, ldapusergroupprovider, authorizers, groups]
level: advanced
status: docs-checked
description: "LdapUserGroupProvider in authorizers.xml: user and group search properties, scopes, sync interval (min 10 secs), paging and case-sensitivity options."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LdapUserGroupProvider

Commented out by default in `authorizers.xml`. Its connection properties (authentication strategy, TLS, referral, timeouts, `Url`) are the same set as the LDAP login provider's. Users and groups are synced from the directory and shown read-only in the NiFi UI; identity mapping rules from nifi.properties apply to user identities but group names are not mapped.

Provider-specific properties:
- `Page Size`: no paging if unset.
- `Sync Interval`: duration between syncs (the guide's example is 30 mins); minimum allowable value 10 secs.
- `Group Membership - Enforce Case Sensitivity`: false.
- Users: `User Search Base`, `User Object Class`, `User Search Scope` (`ONE_LEVEL`, `OBJECT`, `SUBTREE`), `User Search Filter`, `User Identity Attribute`, `User Group Name Attribute`, `User Group Name Attribute - Referenced Group Attribute`.
- Groups: `Group Search Base`, `Group Object Class`, `Group Search Scope`, `Group Search Filter`, `Group Name Attribute`, `Group Member Attribute`, `Group Member Attribute - Referenced User Attribute`.

Pair it with `FileAccessPolicyProvider` via its `User Group Provider` property so directory users and groups can receive policies.

Verify: after one sync interval, directory users and groups appear on the Users page.

## Checked

Confirmed in the NiFi Administration Guide, LdapUserGroupProvider property table: Page Size (no paging if unset), Sync Interval minimum 10 secs, case sensitivity default false, all user and group search properties and the scope values, the commented-out default, the read-only UI note, the identity mapping note, and FileAccessPolicyProvider's User Group Provider property.

Method: docs-only read of cited pages, 2026-11-08
