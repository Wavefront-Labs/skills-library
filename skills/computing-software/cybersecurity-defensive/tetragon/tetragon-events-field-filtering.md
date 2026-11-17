---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-events-field-filtering
name: tetragon-events-field-filtering
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [events-field-filter]
level: advanced
status: docs-checked
description: "Trim Tetragon event fields with INCLUDE and EXCLUDE field filters and redact secrets from arguments and environment variables using RE2 patterns."
sources:
  - "https://tetragon.io/docs/concepts/events/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event field filtering and redaction

## Field filters

Field filters restrict the exported fields per event type. Like export filters they are line-separated JSON objects. They select fields with protobuf field mask syntax under the `"fields"` key: dot-separated paths, several paths separated by commas, for example `"fields":"process.binary,parent.binary,pod.name"`.

- By default a filter applies to all process events; narrow it with `"event_set"`, for example `"event_set":["PROCESS_KPROBE","PROCESS_TRACEPOINT"]`.
- Each filter has an `"action"`: `"INCLUDE"` shows the field, `"EXCLUDE"` hides it.
- With no field filter for an event type, all fields are exported. Defining one or more `"INCLUDE"` filters for an event type makes everything else excluded by default.

Example: only `exec_id` and `parent_exec_id` in all event types except `PROCESS_EXEC`:

```json
{"fields":"process.exec_id,process.parent_exec_id", "event_set": ["PROCESS_EXEC"], "invert_event_set": true, "action": "INCLUDE"}
```

## Redaction filters

Redaction filters remove sensitive strings (for example a secret on a command line) from exported process arguments and environment variables. Pass them as JSON with the `--redaction-filters` flag or the `redactionFilters` Helm value.

- `redact`: RE2 regular expressions; every capture group is replaced with `"*****"`.
- `binary_regex`: limit the filter to matching binaries.
- `redact_str`: custom replacement instead of `"*****"`.
- In JSON, escape backslashes (`\Wpasswd\W?` becomes `{"redact": "\\Wpasswd\\W?"}`).

```json
{"redact": ["--password(?:\\s+|=)(\\S*)"]}
{"binary_regex": ["(?:^|/)foo$"], "redact": ["-p(?:\\s+|=)(\\S*)"]}
{"redact": ["(?:SSHPASS=)+(\\S+)"]}
{"redact": ["--password(?:\\\\s+|=)(\\\\S*)"], "redact_str": "<redacted:password>"}
```

These turn `--password=foo` into `--password=*****` (or `--password=<redacted:password>`), and `SSHPASS=password` into `SSHPASS=*****`.

To keep only requested environment variables, use `--filter-environment-variables VAR1[,VAR2..]`.

## Checked

Date: 2026-11-07

Cited page read in full; every claim matched to page text.

Method: documentation only; no commands were run.
