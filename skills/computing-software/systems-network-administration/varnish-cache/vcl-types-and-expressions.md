---
id: computing-software.systems-network-administration.varnish-cache.vcl-types-and-expressions
name: vcl-types-and-expressions
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-types, duration-units, regex-pcre, regsub]
level: practitioner
status: docs-checked
description: "Use VCL types correctly: durations and units, booleans, regex with PCRE flags, regsub and regsuball, string conversion rules and std conversion functions."
sources:
  - https://www.varnish.org/docs/reference/vcl/
  - https://www.varnish.org/docs/reference/vmod_std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vcl types and expressions

- DURATION: number plus unit `ms s m h d w y`, fraction allowed (`1.5s`). In string context it prints rounded to 3 decimals without the unit (`1.500`).
- TIME: adding a DURATION to a TIME gives a TIME; as a string it is RFC1123 formatted (`Sun, 06 Nov 1994 08:49:37 GMT`). `now` returns the same value throughout a `vcl_*` subroutine, including user subroutines it calls.
- INT prints as a string like `1234`; REAL prints rounded to 3 decimals (`3.142`).
- BOOL: `true` or `false`. A STRING is false if unset, so `if (req.http.opthdr)` tests presence (even when empty) while `== ""` does not distinguish empty from missing. A BACKEND is false with no backend assigned, an INT is false when zero, a DURATION is false when zero or less.
- Typed variables need the right type on the right-hand side: you cannot assign a STRING to a numeric variable, even `"42"`. Convert with `std.integer()`, `std.duration()`, `std.bytes()`, `std.real()`, `std.time()`, `std.ip()`: each takes exactly one source argument plus an optional `fallback`, and a failed conversion without fallback fails the VCL. Anything can be turned into a STRING.
- Equality: INT, DURATION, BYTES, REAL, TIME compare numerically; DURATION, REAL and TIME are floating point, so equality tests can be unreliable. IPs compare by address; STRINGs by content; BACKEND, ACL, PROBE, STEVEDORE, SUB and INSTANCE compare equal only if they are the same object.
- Regex is PCRE; flags go in a group: `req.http.host !~ "(?i)example\.com$"`.
- `regsub(str, regex, sub)` replaces the first match, `regsuball` all of them; in `sub`, `\0` (or `\&`) is the whole match and `\n` is subgroup n.
- `hash_data(input)` (vcl_hash only; the built-in VCL hashes host and URL) and `synthetic(STRING)` (vcl_synth and vcl_backend_error, same as setting `resp.body`/`beresp.body`) are built-in functions.

## Checked
2026-11-08. Read in full: the VCL reference page and the vmod_std page. Confirmed: type behaviours, string forms, conversion rules, equality notes, regex and regsub semantics. Changed: boolean rules for backends, ints and durations now follow the page exactly. Removed: the `varnishd -C -f` verification command (varnishd manual not read).
Method: documentation only; no commands were run.
