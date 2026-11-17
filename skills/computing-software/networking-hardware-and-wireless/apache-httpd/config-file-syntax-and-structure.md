---
id: computing-software.networking-hardware-and-wireless.apache-httpd.config-file-syntax-and-structure
name: config-file-syntax-and-structure
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, config, syntax, include, ifmodule, define]
level: intro
status: docs-checked
description: "Write valid httpd.conf: directive syntax, line continuation, quoting, Include, Define variables, IfModule, and where each directive is allowed."
sources:
  - https://httpd.apache.org/docs/2.4/configuring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config file syntax and structure
## Syntax rules
- One directive per line; a trailing `\` continues the line (nothing may follow it).
- `#` comments must be on their own line, never after a directive.
- Directive names are case-insensitive; arguments often are not.
- Quote arguments containing spaces with `"` or `'`. Inside quotes only `\\` and `\"` are escapes.
- Main config lines may run to about 16 MiB; `.htaccess` lines to 8190 characters.

## Building blocks
- `Include` pulls in other files; wildcards match many files.
- `${VAR}` expands values from `Define` or from environment variables that existed before startup. `Define` wins; unknown variables stay unchanged with a warning.
- `<IfModule>` applies directives only when a module is present. The page warns this can hide a missing module.
- The MIME types file is set by `TypesConfig`.

## Where a directive is valid
Check each directive's Context. Process-control directives are valid only in main server context. Changes to main config files apply only on start or restart.

## Checking
`apachectl configtest` or `httpd -t` checks syntax without starting the server. `-l` lists compiled-in modules and `-M` lists loaded ones.

## Checked

2026-11-08. One directive per line, continuation and comment rules, quoting and the two escapes, case rules, ${VAR} expansion and Define precedence, line-length limits, Include, IfModule warning, TypesConfig, process-control context, restart requirement and the configtest/-t/-l/-M checks confirmed against the Configuration Files page.

Method: documentation only; no commands were run.
