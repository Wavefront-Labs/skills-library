---
id: computing-software.cybersecurity-defensive.falco.append-output-config
name: append-output-config
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [append-output, extra-output, extra-fields, suggested-output, alert-formatting]
level: practitioner
status: docs-checked
description: "Add output text and fields to many Falco rules at once with append_output match, extra_output and extra_fields in falco.yaml or -o."
sources:
  - https://falco.org/docs/concepts/outputs/formatting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `append_output` in `falco.yaml` rather than editing each rule file. It is a list applied in order.

```yaml
append_output:
  - match:
      source: syscall
    extra_output: "on CPU %evt.cpu"
    extra_fields:
      - home_directory: "${HOME}"
      - evt.hostname
```

Every rule with source `syscall` gets `on CPU %evt.cpu` appended to its output line. `extra_fields` go into `output_fields` in JSON output only, not the text line. Environment variables such as `${HOME}` expand in the config file.

`match` keys:
- `source`: rule source, such as `syscall` or a plugin name.
- `rule`: the complete rule name.
- `tags`: list; all listed tags must be present.

All given conditions must hold; with none, or no `match`, the entry applies to every rule.

Suggested fields from extractor plugins are enabled with `- suggested_output: true`, which adds `plugin_field_name=$plugin.field_name`.

Command line:
`falco -o 'append_output[]={"match": {"source": "syscall"}, "extra_output": "on CPU %evt.cpu", "extra_fields": ["evt.hostname"]}'`

Gotcha: this only adds output. To remove or replace output, load a later file with `override: output: replace`.

## Checked

2026-11-08. Read the Alert Formatting page in full; claims match.

Method: documentation only; no commands were run.
