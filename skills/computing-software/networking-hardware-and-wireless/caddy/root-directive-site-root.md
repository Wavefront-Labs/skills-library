---
id: computing-software.networking-hardware-and-wireless.caddy.root-directive-site-root
name: root-directive-site-root
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [root, site-root, http-vars-root, file-server, php-fastcgi, caddyfile]
level: intro
status: docs-checked
description: "Set the Caddy site root with the root directive: relative paths, per-path roots, mutual exclusivity, the http.vars.root placeholder and the systemd /home trap."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/root
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tell Caddy where site files live.

Syntax: `root [<matcher>] <path>`. It sets the `{http.vars.root}` placeholder, which file-aware matchers and directives (`file_server`, `try_files`, `templates`, `php_fastcgi`, the `file` matcher) read. If never set, the working directory is the site root. `root` alone does not serve anything; combine it with `file_server` or `php_fastcgi`.

Multiple `root` directives in one block are mutually exclusive, so overlapping matchers do not cascade or overwrite each other.

Examples: `root /srv` plus `file_server`; a relative path `root public_html` (relative to the working directory) for all requests; and a per-path root `root /foo/* <directory>` which changes the root only for `/foo/*`.

Version note: before v2.8.0 a `/`-leading path was ambiguous with a matcher token, so a wildcard was needed (`root * /srv`). Now `root /srv` is enough.

Systemd trap: under a systemd service the `caddy` user lacks execute permission on `/home`, so roots under it fail. Put files in `/srv` or `/var/www/html`.

Choose the directive over `file_server`'s own `root` subdirective whenever other directives need to see the same root.

## Checked

2026-11-03: read caddyfile/directives/root against this skill. Confirmed: root syntax and {http.vars.root}, mutual exclusivity of multiple roots, relative path example, per-path root, v2.8.0 wildcard note, systemd /home trap.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
