---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-stdlib-string-functions
name: grafana-alloy-stdlib-string-functions
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [stringformat, stringjoin, stringsplit, stringreplace, stringtrim, stringto-lower, stdlib]
level: practitioner
status: docs-checked
description: "Alloy string standard library: string.format verbs, join, split, replace, trim variants and case conversion, plus secret handling."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/stdlib/string.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# string standard library

- `string.format(spec, values...)` is printf-like: `string.format("There are %d lights", 4)`. Verbs: `%%`, `%t` bool, `%b` binary, `%d` decimal, `%o` octal, `%x`/`%X` hex, `%e`/`%E` scientific, `%f` decimal fraction, `%g`/`%G`, `%s` string, `%q` JSON-quoted. `[n]` before the verb picks a one-based argument (`%[1]s`), and later verbs continue from n+1. Too few arguments, an impossible conversion or an unsupported verb is an error.
- `string.join(list, separator)`: `string.join(["foo","bar","baz"], "-")` gives `"foo-bar-baz"`.
- `string.split(string, separator)`: `string.split("foo,bar,baz", ",")` gives a list; splitting `""` gives `[""]`.
- `string.replace(string, substring, replacement)` replaces every occurrence.
- `string.trim(string, charset)` strips any of the listed characters from both ends (`string.trim("?!hello?!", "!?")` is `"hello"`). `string.trim_prefix` removes a prefix (the string is returned unchanged if it does not start with it) and `string.trim_suffix` removes a suffix. `string.trim_space` removes whitespace.
- `string.to_lower`, `string.to_upper`.

## Secrets
`string.format` does not accept a `secret` directly: wrap it in `convert.nonsensitive` first, which exposes the value. If the result must remain a secret, build it with `+` concatenation instead of `string.format`.

## Checked

2026-11-08. Read the string standard library page in full. Confirmed: the `string.format` verb table and `[n]` indexing and error rules, join, split (including the empty-string case), replace, trim with character set, trim_prefix, trim_suffix, trim_space, to_lower, to_upper, and the secret handling note. Narrowed the trim_prefix and trim_suffix wording to what the page states.

Method: documentation only; no commands were run.
