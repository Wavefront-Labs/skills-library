---
id: computing-software.cloud-infrastructure-engineering.fluentd.config-value-types-and-ruby-embedding
name: config-value-types-and-ruby-embedding
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, config-types, size, time, hash, array, embedded-ruby, hostname]
level: practitioner
status: docs-checked
description: "Fluentd parameter types (string, size, time, array, hash), multiline values, escapes, and embedded Ruby with hostname, worker_id, use_nil."
sources:
  - https://docs.fluentd.org/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd value types and embedded Ruby
Types: `string` (unquoted, `'` or `"` literals), `integer`, `float`, `size` (`k`/`m`/`g`/`t` suffixes, bare integer = bytes), `time` (`s`, `m`, `h`, `d`; bare number = seconds as float, e.g. `0.1`), `array` (`["a","b"]` or `a,b`), `hash` (`{"k":"v"}` or `k:v,k2:v2`).

Format tips:
- `"` strings, arrays and hashes may span lines; a newline inside a quoted string is kept.
- A value starting with `[` or `{` is parsed as array/hash, so quote it with `'` or `"` if it is not JSON.
- In `"` strings, `\` escapes (`\n`, `\t`, `\"`, `\\`).
- `#{...}` inside a `"` string evaluates Ruby: `"#{Socket.gethostname}"`, `"foo-#{ENV["FOO_BAR"]}"`.
- Shortcuts `hostname` and `worker_id` since v1.1.0.
- `use_nil` and `use_default` since v1.8.0: `"#{ENV["FOOBAR"] || use_nil}"` replaces the entire string with nil or the default, so `"#{use_nil}/some/path"` is nil.
- `config-xxx` mixins use `"${}"`, a different feature from `"#{}"`.

Reserved `@` parameters: `@type`, `@id`, `@label`, `@log_level`.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/config-file and confirmed: value types, format tips, embedded Ruby, shortcuts, reserved parameters. Removed or reworded: nothing.

Method: documentation only; no commands were run.
