---
id: computing-software.systems-network-administration.icinga-2.api-setup-auth-and-permissions
name: api-setup-auth-and-permissions
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, rest-api, apiuser, permissions, client-cn, api-setup, authentication]
level: practitioner
status: docs-checked
description: Set up the Icinga 2 REST API with icinga2 api setup, ApiUser basic auth or client_cn certificates, and restrict users with permissions strings and filter lambdas.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API setup, authentication and permissions
**Setup:** `icinga2 api setup` enables the `api` feature, sets up certificates and creates ApiUser `root` with a generated password in `/etc/icinga2/conf.d/api-users.conf`; restart afterwards. Manually: set up TLS certificates, `icinga2 feature enable api`, create an `ApiUser`.

**Transport:** HTTPS only, TLS 1.2+, default port 5665 (shared with the cluster; change with `bind_port` on the ApiListener). Versioned URLs start with `/v1`. Header size is limited to 8KB. Non-GET requests need `Accept: application/json`.

**Authentication:** HTTP basic auth (`password`) or an X.509 client certificate (`client_cn`, signed by the ApiListener CA); one ApiUser may have both.
```
object ApiUser "root" { password = "..." }
```
Test: `curl -s -u root:PASSWORD --cacert ca.crt 'https://host:5665/v1'`. `-k` disables verification, testing only.

**Permissions:** a new user has none. Set `permissions = [ ... ]` with wildcards (`"*"`), for example `"objects/query/Host"`. Entries can be dicts with a lambda `filter`, such as `filter = {{ regex("^Linux", host.vars.os) }}`.

Permission names include `actions/<action>`, `config/query`, `config/modify`, `console`, `debug`, `events/<type>`, `objects/query|create|modify|delete/<type>`, `status/query`, `templates/<type>`, `types`, `variables`, plus `filter-expression` and `diagnostic-information`. Body size limits: 1 MB per endpoint, 512 MB for `config/modify` or `*`.

## Checked

2026-11-04. Confirmed against the Icinga 2 API chapter: api setup and root user, TLS 1.2+, port 5665 and bind_port, 8KB header limit, basic auth and client_cn, permission names, per-endpoint body size table (1 MB, 512 MB for config/modify and *), filter lambdas.

Method: documentation only; no commands were run.
