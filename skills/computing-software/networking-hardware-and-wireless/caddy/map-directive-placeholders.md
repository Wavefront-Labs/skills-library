---
id: computing-software.networking-hardware-and-wireless.caddy.map-directive-placeholders
name: map-directive-placeholders
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [map, custom-placeholders, regexp, capture-groups, default, caddyfile]
level: advanced
status: docs-checked
description: "Compute custom placeholders from an input with the Caddyfile map directive: literal and regexp inputs, capture groups, default row, hyphen nulls and type conversion."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/map
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: switch on a value (usually a placeholder) and set new placeholders from a table.

Syntax: `map [<matcher>] <source> <destinations...> { [~]<input> <outputs...>  default <defaults...> }`. Destinations are placeholder names, each a single placeholder like `{my_placeholder}`. Mapped placeholders are evaluated lazily, only when used, so even very large maps are efficient.

Rules: an input prefixed with `~` is a regular expression. Each input may appear once, but a literal `/foo` and a regexp `~/foo` count as different inputs. Outputs fill destinations in order; there may be fewer outputs than destinations (missing ones are filled implicitly) but never more. A literal `-` output means null, so that destination falls back to its default while others take specific values. Outputs are type converted (`true`, `false`, numbers); quote them to stay strings. In a regexp input, `${1}` or `${name}` references capture groups, with `${0}` the full match. `default` supplies outputs when nothing matches.

The page's example switches on `{host}`:
`map {host} {my_placeholder} {magic_number} { example.com "some value" 3   foo.example.com "another value"   ~(.*)\.example\.com$ "${1} subdomain" 5   ~.*\.net$ - 7   ~.*\.xyz$ - 15   default "unknown domain" 42 }`
Results: exact host gets both values; `foo.example.com` gets the string and the default 42; other subdomains build the string from the capture group and get 5; `.net` and `.xyz` hosts get only 7 and 15 with `{my_placeholder}` unset; everything else gets the defaults.

Use the new placeholders in later directives, for example in a matcher or a `respond`.

## Checked

2026-11-03: read caddyfile/directives/map against this skill. Confirmed: map syntax, lazy evaluation, ~ regexp inputs, output count rules, hyphen as null, type conversion, ${group} capture references with 0 as full match, default, the host example.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
