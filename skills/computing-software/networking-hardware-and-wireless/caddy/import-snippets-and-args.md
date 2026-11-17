---
id: computing-software.networking-hardware-and-wireless.caddy.import-snippets-and-args
name: import-snippets-and-args
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [import, snippets, args, globs, reuse, caddyfile, blocks]
level: practitioner
status: docs-checked
description: "Reuse Caddyfile configuration with snippets and the import directive: file and glob patterns, args slice syntax, hidden-file rule and experimental block passing."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/import
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid repeating configuration by importing snippets or files.

`import <pattern> [<args...>] [{block}]` is evaluated before the Caddyfile structure is parsed, so it may appear anywhere and is replaced by the imported tokens. The pattern is a filename, glob or snippet name. Missing specific files are an error; an empty glob is not; an empty specific file only warns. File and glob patterns are relative to the file containing the import. A final-segment `*` skips hidden files; use `.*` to include them. Example: `import sites-enabled/*`.

Arguments are substituted at parse time (not runtime): `{args[n]}` is the 0-based argument, `{args[:]}` all, `{args[:m]}` those before m, `{args[n:]}` from n, `{args[n:m]}` a range. Multi-token forms must stand alone as a token, surrounded by spaces and not quoted. The older `{args.N}` form was deprecated in v2.7.0.

Snippets are defined as `(name) { ... }`. Examples: `(cors) { @origin header Origin {args[0]}  header @origin Access-Control-Allow-Origin "{args[0]}" ... }` used by `import cors example.com`; `(https-proxy) { reverse_proxy {args[:]} { transport http { tls } } }` used with several upstreams; `(proxy-rewrite) { rewrite {args[0]}{uri}  reverse_proxy {args[1:]} }` used as `import proxy-rewrite /api 10.0.0.1 10.0.0.2`.

Experimental (v2.9.x and later): pass a block to the import. `{block}` substitutes the whole block, and `{blocks.key}` substitutes the parameter named `key` from the passed block, enabling snippets with extendable parts such as `{blocks.proxy_target}` and `{blocks.proxy_options}` inside a `reverse_proxy` block. A snippet can also wrap arbitrary directives: `(instrumented-route) { header { ... }  tracing { span args[0] }  {block} }` then `import instrumented-route example-com { respond "OK" }`.

## Checked

2026-11-03: read caddyfile/directives/import against this skill. Confirmed: import syntax and resolution rules, args placeholders, {args.N} deprecated in v2.7.0, snippet definition, experimental v2.9.x+ block and {blocks.key} support, examples.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
