---
id: computing-software.cloud-infrastructure-engineering.harbor.configuration-api-and-env-override
name: configuration-api-and-env-override
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [configurations-api, config-overwrite-json, auth-mode, token-expiration, harbor]
level: advanced
status: docs-checked
description: "Change Harbor settings by REST call to /api/v2.0/configurations or pin them with CONFIG_OVERWRITE_JSON on the core container."
sources:
  - https://goharbor.io/docs/main/install-config/configure-system-settings-cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor settings outside `harbor.yml` can be changed in the UI, over HTTP, or with an environment variable.

Read current configuration:
`curl -u "<username>:<password>" -H "Content-Type: application/json" -ki <Harbor Server URL>/api/v2.0/configurations`

Update one or more items:
`curl -X PUT -u "<username>:<password>" -H "Content-Type: application/json" -ki <Harbor Server URL>/api/v2.0/configurations -d'{"<item_name>":"<item_value>"}'`

Examples: `{"auth_mode":"ldap_auth"}`, `{"project_creation_restriction":"adminonly"}` and `{"token_expiration":"300"}` (minutes; default 30). A 200 response has no body.

Environment override (since 2.3.0): set `CONFIG_OVERWRITE_JSON` on the core container, for example
`CONFIG_OVERWRITE_JSON={"ldap_verify_cert":"false","auth_mode":"ldap_auth","ldap_base_dn":"dc=example,dc=com","ldap_search_dn":"cn=admin,dc=example,dc=com","ldap_search_password":"admin","ldap_url":"myldap.example.com","ldap_scope":2}`.
Once it is set you can change or remove the settings only by editing the variable and restarting the container. It cannot change the authentication mode if a legacy user exists.

Selected items: `auth_mode` (`db_auth`, `ldap_auth`, `uaa_auth`, `oidc_auth`), `ldap_scope` (0 base, 1 one level, 2 subtree; default 2), `ldap_timeout` (default 5), `ldap_uid` (default cn), `ldap_group_membership_attribute` (default memberof), `read_only` (default false), `project_creation_restriction` (`everyone` or `adminonly`).

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Harbor Configuration (configure-system-settings-cli).
- Removed: an unsupported closing paragraph about multi-item PUT and read-first advice.
Method: documentation only; no commands were run.
