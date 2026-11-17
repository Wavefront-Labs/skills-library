---
id: computing-software.systems-network-administration.restic.json-output-scripting
name: json-output-scripting
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, json, scripting, automation, json-lines, quiet]
level: practitioner
status: docs-checked
description: "Parse restic output in scripts with --json and understand single-document versus JSON-lines output and per-command message types."
sources:
  - https://restic.readthedocs.io/en/stable/075_scripting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON output for scripts

Many commands accept `--json` to print machine-readable output on stdout; not all commands support it.

```
restic snapshots --json
restic backup --json /path/to/data
```

## Two formats

- Single JSON document: commands like `snapshots`, `stats`, `find`, `forget`, `key list` and `version` print one document that is parsed as a whole.
- JSON lines: commands such as `backup`, `check`, `diff`, `ls`, `restore`, `tag` and `init` emit new-line separated JSON messages; tell them apart with the `message_type` field (`ls` also has the deprecated `struct_type`).
- `prune` has no JSON support yet, so `forget --prune` mixes JSON and text output.

For `backup`, lines have a message type: status (progress), error, verbose status (with `--verbose=2`), and a final summary. Read the summary line for the snapshot ID and file counts.

## Per-command objects

The scripting page documents the JSON for `backup`, `cat`, `check`, `diff`, `find`, `forget`, `init`, `key list`, `ls`, `restore`, `snapshots`, `stats`, `tag` and `version`. For example, `forget` returns ForgetGroup objects with the snapshots kept or removed and their keep reasons.

## Cautions

Do not rely on human-readable text; the JSON is meant to stay backwards compatible, but new message types or fields may be added at any time, and fields with default values such as 0 or an empty string may be omitted. Fatal errors also print a final `exit_error` JSON message on stderr with the exit code. Check the exit code first (see script-exit-codes), then parse the JSON.

## Checked

Checked 2026-11-08 against the restic Scripting page (075_scripting), read in full. Confirmed: --json, the single document versus JSON lines split per command, backup message types (status, error, verbose_status, summary), snapshot_id in the summary, forget ForgetGroup and KeepReason objects, prune lacking JSON support, backwards-compatibility and omitted-default notes, and exit_error. Removed: the --quiet section (not on the page), prune from the documented-command list, init and key list mis-grouping, and the jq suggestion.

Method: documentation only; no commands were run.
