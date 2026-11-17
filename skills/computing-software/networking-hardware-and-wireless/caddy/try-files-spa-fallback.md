---
id: computing-software.networking-hardware-and-wireless.caddy.try-files-spa-fallback
name: try-files-spa-fallback
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [try-files, spa, php-index, first-exist, file-matcher, most-recently-modified, caddyfile]
level: practitioner
status: docs-checked
description: "Rewrite to the first existing file with try_files: policies, directory and glob entries, =404 fallback, the expanded file-matcher form and PHP or SPA recipes."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/try_files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: map pretty URLs to real files or a front controller.

`try_files <files...> { policy first_exist|first_exist_fallback|smallest_size|largest_size|most_recently_modified }` rewrites the path to the first listed file existing under the site root; if none exist, nothing is rewritten. Append `/` to test directories; paths are relative to `root` and globs are expanded. An entry may carry a query string, which replaces the query when that entry matches. With the default `first_exist` policy, the last item may be `=404` (any code), which raises an error that `handle_errors` can catch.

It does not accept a matcher token. For custom logic use the expanded form: `@try_files file <files...>` then `rewrite @try_files {file_match.relative}`, see the file matcher.

Recipes: `try_files {path} /index.php` falls to a PHP router; `try_files {path} /index.php?{query}&p={path}` adds the original path for legacy apps; add `{path}/` to also match directories; `try_files {path} {path}/ =404` returns a catchable 404; and to pick the newest build `try_files {file.base}.*.{file.ext} { policy most_recently_modified }` serves `index.be331df.html` when `index.html` is requested.

Ordering gotcha: `try_files` sorts before `reverse_proxy`, so in a single-page app with an API wrap them in `route` (proxy first), or use `handle` blocks. See route-literal-order.

## Checked
2026-11-03. Confirmed against the Caddy try_files directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
