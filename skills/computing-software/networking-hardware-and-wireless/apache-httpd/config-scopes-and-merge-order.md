---
id: computing-software.networking-hardware-and-wireless.apache-httpd.config-scopes-and-merge-order
name: config-scopes-and-merge-order
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, config, directory, location, files, merge-order, if]
level: practitioner
status: docs-checked
description: "Choose between Directory, Files, Location and If containers and predict how overlapping sections merge, including the order each is applied."
sources:
  - https://httpd.apache.org/docs/2.4/sections.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config scopes and merge order
## Filesystem vs webspace
- `<Directory>`, `<Files>` and their `Match` variants match disk paths.
- `<Location>`/`<LocationMatch>` match URLs; use them for proxy, handlers and non-disk content.
- Do not use `<Location>` to restrict disk content: case-insensitive filesystems, symlinks and aliases can bypass it. `<Location "/">` is the exception.

## Merge order (later wins)
1. `<Directory>` (no regex) and `.htaccess` together (`.htaccess` overrides)
2. `<DirectoryMatch>`
3. `<Files>` and `<FilesMatch>`
4. `<Location>` and `<LocationMatch>`
5. `<If>`, wherever enclosed

Within a group sections apply in file order, except `<Directory>`, applied shortest path to longest. `<VirtualHost>` sections apply after main-server ones; only one vhost is selected per request. `<Proxy>` replaces `<Directory>` when mod_proxy serves the request.

## Nesting and conditionals
- `<Files>` may nest in `<Directory>`; `<If>` may nest in Directory, Location and Files but not in another `<If>`.
- `<IfDefine>`, `<IfModule>`, `<IfVersion>` are evaluated at startup; `<If>` per request.
- `*` and `?` wildcards never match `/`.

## Trap
A `<Limit>` inside `<Location>` leaves unlisted methods with no authorization requirement and can override `<Directory>` restrictions. Use `<LimitExcept>`.

## Checked

2026-11-08. Filesystem vs webspace containers, the Location caution and its `<Location "/">` exception, the five-step merge order, shortest-to-longest Directory ordering, VirtualHost and Proxy handling, nesting rules, startup-time If* containers, wildcard behaviour and the Limit trap confirmed against the sections page.

Method: documentation only; no commands were run.
