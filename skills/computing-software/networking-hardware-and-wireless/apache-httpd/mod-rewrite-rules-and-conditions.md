---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-rewrite-rules-and-conditions
name: mod-rewrite-rules-and-conditions
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-rewrite, rewriteengine, rewriterule, rewritecond, backreferences]
level: practitioner
status: docs-checked
description: "Write mod_rewrite RewriteRule and RewriteCond rules: engine enablement, rule ordering, condition flags and variables, back-references and typical examples."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_rewrite rules and conditions
`RewriteEngine on` (default off) is needed in each vhost: rewrite config is not inherited by virtual hosts.

## RewriteRule
`RewriteRule [!]Pattern Substitution [flags]`. Rules apply in file order, each on the previous result.
```apache
RewriteEngine on
RewriteRule "^/old/(.*)$" "/new/$1" [R=301,L,QSA]
```

## RewriteCond
`RewriteCond TestString [!]CondPattern [flags]`
- Multiple conditions are ANDed; a failure abandons the rule.
- `%1`-`%9` refer to the last RewriteCond match; `$1`-`$9` to the RewriteRule match.
- Variables include `%{HTTP_HOST}`, `%{HTTP_USER_AGENT}`, `%{REQUEST_URI}`, `%{QUERY_STRING}`, `%{HTTPS}`, `%{ENV:var}`, `%{HTTP:header}`.
- Tests include `-f -d -s -l -F -U`, `-eq -lt`, and string compares.
- Look-ahead `%{LA-U:var}` / `%{LA-F:var}` resolves later-phase values.
- Flags: `NC`, `OR` (combine with next), `NV`.
```apache
RewriteCond "%{HTTP_USER_AGENT}" "(iPhone|Android)" [NC]
RewriteRule "^/$" "/homepage.mobile.html" [L]
```

## RewriteBase and options
`RewriteBase URL-path` sets the prefix for relative substitutions in per-directory context. `RewriteOptions Inherit` merges parent rules.

## Logging
RewriteLog was removed in 2.4; use `LogLevel alert rewrite:trace3` (trace1-trace8). Above trace2 is very slow.

## Checked

2026-11-08. RewriteEngine default and non-inheritance by virtual hosts, rule ordering, RewriteCond AND/OR logic, %N and $N back-references, condition tests and look-ahead variables, NC/OR/NV flags, RewriteBase, RewriteOptions Inherit, and the 2.4 logging change (RewriteLog replaced by LogLevel rewrite:trace1-trace8, slow above trace2) confirmed against the mod_rewrite page.

Method: documentation only; no commands were run.
