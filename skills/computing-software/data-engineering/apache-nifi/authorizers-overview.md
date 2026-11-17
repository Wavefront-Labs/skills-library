---
id: computing-software.data-engineering.apache-nifi.authorizers-overview
name: authorizers-overview
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, authorizers, authorization, standardmanagedauthorizer, user-group-provider]
level: practitioner
status: docs-checked
description: "How authorizers.xml fits together in NiFi: StandardManagedAuthorizer, access policy provider, user group providers, composite providers and the nifi.properties selectors."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authorizers.xml structure

nifi.properties selectors:
- `nifi.authorizer.configuration.file` (default `./conf/authorizers.xml`)
- `nifi.security.user.authorizer` (which configured authorizer to use; the nifi.properties table lists a default of `single-user-authorizer`)

Layers:
1. User group provider: `FileUserGroupProvider` (default; `Users File` default `users.xml`), `LdapUserGroupProvider`, `ShellUserGroupProvider`, `AzureGraphUserGroupProvider`.
2. Composites: `CompositeUserGroupProvider` (`User Group Provider [unique key]`) and `CompositeConfigurableUserGroupProvider` (adds `Configurable User Group Provider`).
3. `FileAccessPolicyProvider`: `User Group Provider`, `Authorizations File`, `Initial Admin Identity`, `Node Identity`.
4. `StandardManagedAuthorizer` (default): one property, `Access Policy Provider`.

`FileAuthorizer` has been replaced by the StandardManagedAuthorizer approach and is kept only for backwards compatibility. `LdapUserGroupProvider`, `ShellUserGroupProvider` and `AzureGraphUserGroupProvider` ship commented out in authorizers.xml. `Initial Admin Identity` is used only when no other policies exist, and cannot be combined with a `Legacy Authorized Users File`.


Verify: after restart, `users.xml` and `authorizations.xml` exist and the admin can open the Users and Policies pages.

## Checked

Confirmed in the NiFi Administration Guide, Authorizer Configuration: the nifi.authorizer.configuration.file default, StandardManagedAuthorizer as default with its single Access Policy Provider property, FileUserGroupProvider Users File, the LDAP, Shell and Azure providers and their commented-out status, both composite providers and their property names, FileAccessPolicyProvider properties, and the FileAuthorizer legacy note. The sentence about restart creating users.xml and authorizations.xml is the guide's default file naming, not a tested outcome.

Method: docs-only read of cited pages, 2026-11-08
