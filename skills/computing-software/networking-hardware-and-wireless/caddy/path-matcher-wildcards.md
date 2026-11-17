---
id: computing-software.networking-hardware-and-wireless.caddy.path-matcher-wildcards
name: path-matcher-wildcards
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [path-matcher, wildcard, prefix-match, normalization, escapes, caddyfile]
level: practitioner
status: docs-checked
description: "Caddy path matchers: exact versus prefix, wildcard positions, slash significance, escape handling and the %* escape wildcard."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write path matchers that match exactly what you intend.

Path matching is exact (but case-insensitive) unless you add `*`. Wildcard positions: at the end only for a prefix (`/prefix/*`), at the beginning only for a suffix (`*.suffix`), on both sides for a substring (`*/contains/*`), in the middle only for a glob (`/accounts/*/info`). Slashes matter: `/foo*` matches `/foo`, `/foobar`, `/foo/` and `/foo/bar`, but `/foo/*` matches neither `/foo` nor `/foobar`. Multiple paths in one matcher are OR-ed.

Cleaning: dot segments are resolved before matching, and multiple slashes merge unless the pattern itself has them, so `/foo` matches `/foo` and `//foo`, but `//foo` matches only `//foo`.

Escapes: the path is normalised (URL-decoded), except where the pattern itself contains an escape. `/foo/bar` matches both `/foo/bar` and `/foo%2Fbar`; `/foo%2Fbar` matches only the escaped form. The special wildcard `%*` leaves its span escaped: `/bands/*/*` does not match `/bands/AC%2FDC/T.N.T` (it is compared as `/bands/AC/DC/T.N.T`), while `/bands/%*/*` does.

Examples: `@assets path /js/* /css/* /images/*`; `@favicon path /favicon.ico`; `@extensions path *.js *.css`; in CEL `path('/js/*', '/css/*')`.

## Checked

2026-11-08. Read the path section of the Caddyfile matchers page (fully, plus the surrounding overview lines). Confirmed: exact case-insensitive matching, the four wildcard positions, slash significance with the `/foo*` and `/foo/*` examples, dot-segment cleaning and slash merging, escape normalisation, the `%*` wildcard with the AC/DC example, OR-ing of multiple paths, and the example matchers.

Method: documentation only; no commands were run.

