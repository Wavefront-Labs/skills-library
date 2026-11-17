---
id: computing-software.systems-network-administration.bash.jq-select-map
name: jq-select-map
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, jq-select-map, jq-filters, shell-scripting]
level: practitioner
status: docs-checked
description: "Filter and transform JSON arrays in shell with jq select, map, group_by and sort_by, with correct quoting."
sources:
  - https://jqlang.github.io/jq/manual/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jq select and map
**Goal:** query JSON from scripts.
```bash
jq -r '.items[] | select(.status == "failed") | .name' data.json
jq '[.items[] | {name, size: (.size / 1024 | floor)}]' data.json
jq 'map(select(.age > 30)) | length' people.json
jq -r 'group_by(.team)[] | "\(.[0].team): \(length)"' people.json
jq --arg n "$name" '.[] | select(.name == $n)' people.json
jq -e '.ok == true' status.json >/dev/null    # exit code reflects the result
```
- Pass shell values with `--arg name value` (always bound as a string) or `--argjson name JSON-text` (parsed as JSON, so `123` is a number), and use `$name` in the filter, rather than interpolating into the filter string (injection and quoting bugs).
- `-r` writes string results without JSON quotes, `-c` puts each output on one line. With `-e`, jq exits 0 if the last output was neither false nor null, 1 if it was false or null, and 4 if no valid result was produced.
- `.foo` on an object gives null, not an error, when the key is absent; `a // b` gives `b` when `a` is false, null or empty, so `.foo // "default"` supplies a default.
- `map(f)` is `[.[] | f]`; `select(f)` passes its input through only when `f` is true; `group_by(.k)` returns an array of arrays sorted by `.k`.
- Self-check: `echo '[{"a":1}]' | jq -r '.[0].a'` prints 1.

## Checked
2026-11-08. Confirmed against the jq manual: `select`, `map`, `group_by`, `floor`, `length`, object shorthand `{name}`, string interpolation, `--arg`, `--argjson`, `-r`, `-c`, `-e` exit codes, null for a missing key and the `//` operator. The manual is for the current jq release; nothing was removed.
Method: documentation only; no commands were run.
