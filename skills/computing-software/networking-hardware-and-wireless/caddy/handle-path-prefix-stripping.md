---
id: computing-software.networking-hardware-and-wireless.caddy.handle-path-prefix-stripping
name: handle-path-prefix-stripping
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [handle-path, strip-prefix, path-matcher, subpath, caddyfile, reverse-proxy-prefix]
level: practitioner
status: docs-checked
description: "handle_path in a Caddyfile: match a path prefix and strip it before the handlers run, its single-path-matcher limit and the equivalent handle plus uri strip_prefix."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/handle_path
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: mount a backend or file tree under a URL prefix without the backend seeing the prefix.

Syntax: `handle_path <path_matcher> { <directives...> }`. It behaves like `handle` (mutually exclusive with sibling handle blocks) but implicitly applies `uri strip_prefix` for the matched prefix. So `handle_path /prefix/* { ... }` is the same as `handle /prefix/* { uri strip_prefix /prefix  ... }`, only shorter.

Restrictions: exactly one path matcher is required and accepted. Named matchers (`@name`) cannot be used. After stripping, the path always begins with `/`; with `handle_path /prefix*`, a request for `/prefix` is handled with path `/`.

Typical site from the docs: `handle_path /api/* { reverse_proxy localhost:9000 }` strips `/api` before proxying, and a trailing `handle { root /srv  file_server }` serves the static site for everything else. Because handle and handle_path are mutually exclusive, a request is served by only one of them.

The page tells you to be aware of the "subfolder problem" with this pattern.

When you need a named matcher or something other than a prefix strip, use `handle` with an explicit `uri` directive instead.

## Checked
2026-11-03. Confirmed against the Caddy handle_path directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
