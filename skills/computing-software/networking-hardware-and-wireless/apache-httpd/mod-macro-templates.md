---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-macro-templates
name: mod-macro-templates
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-macro, macro, use, undefmacro, templates]
level: advanced
status: docs-checked
description: "Remove repeated config with mod_macro: define parameterised Macro blocks, expand them with Use, and avoid parameter-name and quoting pitfalls."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_macro.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_macro templates
Available from 2.4.5. Macros expand at startup and the result is processed like normal config.

| Directive | Purpose |
|---|---|
| `<Macro name $p1 ...>` | define |
| `Use name v1 ...` | expand |
| `UndefMacro name` | remove |

All three work in server, virtual host and directory context.

```apache
<Macro VHost $name $domain>
<VirtualHost *:80>
    ServerName $domain
    ServerAlias www.$domain
    DocumentRoot "/var/www/vhosts/$name"
    ErrorLog "/var/log/httpd/$name.error_log"
    CustomLog "/var/log/httpd/$name.access_log" combined
</VirtualHost>
</Macro>

Use VHost example example.com
UndefMacro VHost
```

## Rules
- Macro names are case-insensitive; variable names are case-sensitive.
- Start parameter names with `$`, `%` or `@`; without a sigil you get a warning (conflicts with `Define`).
- `$` and `%` parameters are substituted unescaped; `@` parameters are escaped in quotes.
- Avoid names that are prefixes of each other; the longest match is used.
- Use `$(name)` rather than `${name}` inside strings, because `${...}` clashes with `Define`.
- `Use` must pass exactly as many arguments as the macro declares.
- Run `UndefMacro` after use to prevent name conflicts.

## Checked

2026-11-08. Availability from 2.4.5, the Macro, Use and UndefMacro contexts, case rules, sigil warning, escaping of `$`/`%` vs `@`, longest-name matching, `$(...)` vs `${...}`, and the argument-count rule confirmed against the full mod_macro page.

Method: documentation only; no commands were run.
