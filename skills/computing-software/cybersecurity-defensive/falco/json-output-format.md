---
id: computing-software.cybersecurity-defensive.falco.json-output-format
name: json-output-format
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [json-output, output-fields, alert-properties, hostname, iso8601]
level: intro
status: docs-checked
description: "Switch Falco to one-line JSON alerts and know the properties each alert carries, including output_fields and tags."
sources:
  - https://falco.org/docs/concepts/outputs/channels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For every output channel you can switch to JSON in `falco.yaml` with `json_output: true`, or on the command line. Falco then prints one JSON object per alert on a single line, with these properties:

- `time`: alert time in ISO8601 format.
- `rule`: the rule that fired.
- `priority`: the rule priority.
- `output`: the formatted output string.
- `hostname`: the host running Falco (the container name when in a container).
- `tags`: the rule's tags.
- `output_fields`: for each templated value in the output expression, the value taken from the triggering event.
- `source`: the event source, for example `syscall`. The docs list the properties above without it but the sample alert includes it.

Example fragment:

```json
{"hostname": "falco-xczjd", "priority": "Critical", "rule": "Terminal shell in container", "source": "syscall", "tags": ["container", "mitre_execution", "shell"], "output_fields": {"proc.name": "sh", "user.name": "root"}}
```

Extra fields beyond those in the rule output can be added to `output_fields` with `append_output` in `falco.yaml`.

Gotcha: the docs' HTTP output and Slack `jq` pipeline examples both set `json_output: true`, and the `jq` filter reads the `.output` property, so it needs JSON input.

## Checked

2026-11-08. Read the Output Channels page in full. Noted that source appears in the sample but not the property list, and replaced an overstated HTTP/Slack gotcha with what the examples show.

Method: documentation only; no commands were run.
