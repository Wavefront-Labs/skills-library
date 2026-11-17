---
id: computing-software.networking-hardware-and-wireless.apache-httpd.authorization-require-containers
name: authorization-require-containers
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, authorization, require, requireall, requireany, authmerging, mod-authz-core]
level: practitioner
status: docs-checked
description: "Build authorisation logic with Require providers and RequireAll, RequireAny, RequireNone containers, negation rules, AuthMerging and 401 vs 403 behaviour."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_authz_core.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorisation with Require
## Providers
`Require all granted|denied`, `env`, `method` (GET and HEAD equivalent), `expr`, plus `user`, `group`, `valid-user`, `ip`, `forward-dns`.

Multiple `Require` lines in one section act as `<RequireAny>`.

## Containers
| Container | Granted if | Neutral treated as |
|---|---|---|
| `<RequireAny>` | at least one grants | deny |
| `<RequireAll>` | none deny, one grants | grant |
| `<RequireNone>` | none grant | grant |

`not` turns Granted into Denied and vice versa but Neutral stays Neutral, so a negated directive can never authorise alone.
```apache
<RequireAll>
    Require group alpha beta
    Require not group reject
</RequireAll>
```

## AuthMerging
`Off` (default) replaces inherited logic; `And`/`Or` combine with the predecessor. Not inherited beyond its section. `<Location>` authorisation overwrites `<Directory>` and `<Files>` by default.

## Status codes
When authentication succeeds but authorisation fails, the default is 401 (re-prompts). `AuthzSendForbiddenOnFailure On` returns 403 but reveals that a guessed password was right.

## Misc
`Require` applies to all methods unless in `<Limit>`. `AuthzProviderAlias` creates named provider variants.

## Checked

2026-11-08. Providers, container result table, negation rule, AuthMerging values and default, the 401 and 403 behaviour, the Location overwrite warning, the Limit note and implicit RequireAny confirmed against the full mod_authz_core page (httpd 2.4).

Method: documentation only; no commands were run.
