---
id: computing-software.systems-network-administration.bash.jq-to-shell-vars
name: jq-to-shell-vars
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, jq-to-shell-vars, jq-at-sh, shell-scripting]
level: advanced
status: docs-checked
description: "Load jq output into bash variables and arrays safely using @sh, read, mapfile and @tsv rather than eval."
sources:
  - https://jqlang.github.io/jq/manual/
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading jq output into shell variables
**Goal:** get JSON fields into variables safely.
```bash
read -r name version < <(jq -r '[.name, .version] | @tsv' pkg.json)
mapfile -t hosts < <(jq -r '.hosts[]' cfg.json)
while IFS=$'\t' read -r id state; do echo "$id is $state"; done \
  < <(jq -r '.[] | [.id, .state] | @tsv' list.json)
eval "$(jq -r '@sh "A=\(.a) B=\(.b)"' cfg.json)"      # @sh quotes values safely
IFS= read -r -d '' body < <(jq -r '.body' x.json; printf '\0')
```
- jq's `@sh` escapes a value for use in a POSIX shell command line (an array becomes space-separated strings); `@tsv` writes one array per line with tab separators and escapes line feed, carriage return, tab and backslash as `\n`, `\r`, `\t`, `\\`. Plain string concatenation escapes nothing. Note `@tsv` leaves those escapes in the text, so `read` hands them over unchanged.
- Tab is IFS whitespace, so `IFS=$'\t' read` treats a run of tabs as one delimiter and an empty middle field is lost; pick a non-whitespace delimiter, or emit one value per line with `mapfile`, when fields can be empty.
- `read -d ''` and `mapfile -d ''` end a record at a NUL character, which suits `jq --raw-output0` when values contain newlines.
- With `set -o pipefail` a pipeline returns the last non-zero status of its commands; `PIPESTATUS` holds the status of each command in the most recent foreground pipeline.
- Self-check: values containing spaces and quotes survive.

## Checked
2026-11-08. Confirmed against the jq manual (`@sh`, `@tsv`, `--raw-output0`) and the Bash Reference Manual (`read -d`, `mapfile`, IFS whitespace splitting, `pipefail`, `PIPESTATUS`). Removed the "mapfile needs bash 4+" claim and the claim that process substitution hides jq's exit status, which the manuals do not state.
Method: documentation only; no commands were run.
