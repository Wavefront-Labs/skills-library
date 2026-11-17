---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.parser-filter
name: parser-filter
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, parser-filter, key-name, preserve-key, reserve-data, parsers-file]
level: practitioner
status: docs-checked
description: "Parse a field of an existing record with the parser filter and control which fields survive."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/parser"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parser filter

The `parser` filter parses one field of a record using a named parser defined in a parsers file.

| Key | Default | Meaning |
| --- | --- | --- |
| `key_name` | none | field in the record to parse |
| `parser` | none | parser name; several `parser` entries are allowed |
| `preserve_key` | `false` | keep the original `key_name` field in the result |
| `reserve_data` | `false` | keep all other original fields |

The parsers file path goes in the service section as `parsers_file`.

Parser definition:

```yaml
parsers:
  - name: dummy_test
    format: regex
    regex: '^(?<INT>[^ ]+) (?<FLOAT>[^ ]+) (?<BOOL>[^ ]+) (?<STRING>.+)$'
```

Pipeline for the record `{"data":"100 0.5 true This is example"}`:

```yaml
pipeline:
  inputs:
    - name: dummy
      tag: dummy.data
      dummy: '{"data":"100 0.5 true This is example"}'
  filters:
    - name: parser
      match: 'dummy.*'
      key_name: data
      parser: dummy_test
```

With both retention options at their `false` defaults, the output contains only the parsed fields. Set `reserve_data: true` to keep all other original fields, and add `preserve_key: true` to keep the original `key_name` field too.

`Unescape_key` is deprecated; do not use it in new configurations.

## Checked

2026-11-03. Confirmed on the Fluent Bit Parser filter page: key_name, parser, preserve_key and reserve_data with defaults, the parsers_file location, deprecated Unescape_key, and the dummy_test example and its output. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
