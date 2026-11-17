---
id: computing-software.search-and-information-retrieval.apache-solr.rule-based-authorization
name: rule-based-authorization
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [rule-auth, authorization, rule-based-authorization, permissions, user-role, externalrole]
level: advanced
status: docs-checked
description: "Authorize Solr requests with RuleBasedAuthorizationPlugin: user-role mappings, predefined permissions, custom permissions by collection, path and method, and external roles."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/rule-based-authorization-plugin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rule-based-authorization

Users get roles; permissions grant roles access to APIs. Set the `authorization` block in `security.json`; roles work with any authentication plugin.

Classes: `solr.RuleBasedAuthorizationPlugin` (explicit `user-role` map in `security.json`), `solr.ExternalRoleRuleBasedAuthorizationPlugin` (roles come from the authentication plugin's principal, such as the JWT `rolesClaim`), and `solr.MultiAuthRuleBasedAuthorizationPlugin`.

`user-role` values are one role or an array: `"user2": ["role1", "role2"]`.

Permissions: predefined by name, such as `read`, `all`, `security-read`, `security-edit`, `schema-edit`, `config-edit`, `metrics-read`, `core-admin-read`, `core-admin-edit`, `collection-admin-edit`. Custom ones set `name`, `collection` (default `*`), `path` (wildcard allowed), `method` (GET, POST, PUT, DELETE, HEAD or `*`), `params`, and `role` (`*` lets all roles in).

For an alias, set `collection` to the underlying collections or `*`; the alias name is not used.

## Checked

2026-11-04. Confirmed against the Rule-Based Authorization Plugin page: plugin classes, custom permission properties (`collection`, `path`, `method`, `params`, `role`) and wildcards, predefined permissions, alias handling. Removed an example block not verified on the page.

Method: documentation only; no commands were run.
