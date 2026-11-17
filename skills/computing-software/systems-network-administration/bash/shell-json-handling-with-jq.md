---
id: computing-software.systems-network-administration.bash.shell-json-handling-with-jq
name: shell-json-handling-with-jq
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-jq, json-in-shell, jq-filters, raw-output, jq-args]
level: practitioner
status: draft
description: "Parse, filter and build JSON in shell scripts with jq instead of grep and sed."
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jq in scripts

- Never parse JSON with `grep`/`sed`. `jq -r '.items[].name'` prints raw strings (no quotes); `-e` sets the exit status from the last output (null/false give 1) for use in `if`.
- Pass shell values safely with `--arg name "$value"` (string) or `--argjson n 5`, never by interpolating into the filter: `jq --arg id "$id" '.[] | select(.id == $id)'`. `--slurpfile`/`--rawfile` for files, `--args` for positional.
- Common: `.a // "default"`, `map(select(.x > 1))`, `group_by(.k)`, `to_entries`, `@csv`, `@tsv`, `@sh` (shell-quoted output), `-c` compact one-per-line, `-s` slurp, `-n` with `input`/`inputs`.
- Build JSON: `jq -n --arg a "$a" '{a: $a, ts: now}'`.
- Loop safely over results: `jq -r '.[] | @sh "process \(.id)"'` or `while read -r id; do ...; done < <(jq -r '.[].id' f.json)`.
- NUL separation for hostile data: `jq -j '.[] | .name + "\u0000"'` with `read -d ''`.
- Validate input exists and is valid JSON (`jq empty file`); jq numbers are doubles; big ids should stay strings.
- For YAML use `yq`; for HTML use a parser.
