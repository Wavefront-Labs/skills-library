---
id: computing-software.cybersecurity-defensive.falco.cli-validate-and-list
name: cli-validate-and-list
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falco-cli, validate-rules, dry-run, list-fields, support]
level: intro
status: docs-checked
description: "Use Falco command-line flags -V, --dry-run, -L, -l, --list, -i and --support to check rules and discover fields."
sources:
  - https://falco.org/docs/reference/daemon/cli-arguments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Useful `falco` options for checking a setup:

- `-V <rules_file>` (`--validate`): read the file(s), validate the rules, then exit. Repeat for several files.
- `--dry-run`: run without processing events, to check that configuration and rules have no errors.
- `-L`: show name and description of all rules and exit. With `json_output` true it prints rules, macros and lists in JSON.
- `-l <rule>`: show one rule's name and description.
- `--list [=<source>]`: list all defined fields, optionally for one source such as `syscall` or a plugin source. Add `-N` for names only and `--format text|markdown|json`.
- `--list-events`: list syscall events, metaevents and tracepoint events.
- `--list-plugins` and `--plugin-info <plugin_name>`: show loaded plugins and an init config schema.
- `-i`: print events ignored by default for performance.
- `--support`: print version, rules files, loaded config and more, as JSON.
- `--config-schema` and `--rule-schema`: print the JSON schemas.
- `-M <num_seconds>`: stop after that many seconds.
- `-P, --pidfile <path>`: write the PID.
- `-v`: verbose output. `--version`: version info.

Gotcha: `-r` loads only files with `.yml` or `.yaml` extensions when given a directory.

## Checked

2026-11-08. Read in full: the Falco daemon arguments list (raw markdown `docs/content/en/docs/reference/daemon/cli-arguments/cli-arguments.md` in falco-website). Every flag above matches its description there.

Method: documentation only; no commands were run.
