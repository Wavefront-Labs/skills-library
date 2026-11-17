---
id: computing-software.devops-ci-cd.rundeck.key-value-data-log-filter
name: key-value-data-log-filter
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, key-value-data, log-filter, data-variables, capture-group]
level: practitioner
status: docs-checked
description: "Capture step output into Rundeck data variables with the Key Value Data log filter: default pattern, capture groups, multiple matches and key collisions."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/log-filters/key-value-data.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The filter applies a regex to a step's output and exports key/value data to the workflow as a context variable for later steps.

Fields:
- Pattern: regex with one or two capture groups. Two groups: first is the key, second the value. One group: the match is the value and Name Data supplies the key.
- Name Data: variable key (single-group case only).
- Log Data: add a table of captured data to the job log.
- Match Substrings: if off, the pattern must match the entire line.
- Allow Multiple Matches: capture more than one pair per line (default is first match per line).
- Advanced, Invalid Character Pattern: by default strips whitespace and `$`, `{`, `}`, `\`.

Default pattern: `^RUNDECK:DATA:(.+?)\s*=\s*(.+)$`. A step printing `RUNDECK:DATA:EXIP=10.1.1.2` gives `$data.EXIP` in commands and `@data.EXIP@` in scripts.

Multiple pairs per line: pattern `(\w+)=([^\s]+)`, with Match Substrings and Allow Multiple Matches enabled.

Gotcha: when matches share a key, only the last value is kept. Make keys unique (for example `ID1:123, ID2:456`, pattern `(ID\d+):(\d+)`). For multi-line capture use the Multiline Regex Capture filter.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Key-Value Data: pattern with one or two capture groups, Name Data, Log Data, Match Substrings, Allow Multiple Matches (first match per line by default), Invalid Character Pattern defaults, the default pattern, $data.EXIP and @data.EXIP@ usage, the multiple pair example, and the last-value-wins key collision with unique-key fix. Nothing removed.

Method: documentation only; no commands were run.
