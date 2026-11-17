---
id: computing-software.networking-hardware-and-wireless.caddy.file-matcher-and-placeholders
name: file-matcher-and-placeholders
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [file-matcher, try-policy, split-path, file-match, glob, caddyfile]
level: practitioner
status: docs-checked
description: "Match on files that exist with the file matcher: root, try_files, try_policy values, split_path, one-line shortcut and the file_match placeholders."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: route by what exists on disk.

Block form: `file { root <path>  try_files <files...>  try_policy first_exist|first_exist_fallback|smallest_size|largest_size|most_recently_modified  split_path <delims...> }`. One-line form: `file <files...>` (policy first_exist). An empty `file` matcher is equivalent to `file {path}`, testing the verbatim URI path under the root.

- `root`: default is the working directory, or `{http.vars.root}` if set by the `root` directive.
- `try_files`: relative to the root, globs expanded, trailing `/` matches directories. With `first_exist`, the last entry may be `=404`-style, raising an error you can catch with `handle_errors`.
- `try_policy`: `first_exist` (default); `first_exist_fallback` assumes the last element exists, skipping a disk access; `smallest_size`; `largest_size`; `most_recently_modified`.
- `split_path`: split each tried path at the first delimiter found; the left part including the delimiter is tried. `/remote.php/dav/` with `.php` tries `/remote.php`. Delimiters must end a path component. Mostly for PHP.

On a match four placeholders appear: `{file_match.relative}` (root-relative, useful for rewrites), `{file_match.absolute}`, `{file_match.type}` (`file` or `directory`) and `{file_match.remainder}` (what remained after splitting).

Examples: `@html file { try_files {path}.html {path} }`; `@html-or-error file {path}.html {path} =404`. The `try_files` directive is a shortcut of this matcher plus `rewrite`.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: block and one-line forms, root default, try_files globbing, try_policy values including =404 fallback, split_path, the four file_match placeholders, try_files directive shortcut.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
