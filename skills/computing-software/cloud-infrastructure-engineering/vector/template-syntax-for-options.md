---
id: computing-software.cloud-infrastructure-engineering.vector.template-syntax-for-options
name: template-syntax-for-options
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [template-syntax, strftime, partitioning, field-references, missing-fields, vector]
level: practitioner
status: docs-checked
description: "Use {{ field }} and strftime specifiers in options such as key_prefix, and handle missing fields."
sources:
  - https://vector.dev/docs/reference/configuration/template-syntax/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some options accept a template, which makes the value depend on the event. The option's reference page states whether it does. Two forms:

- Event fields: `{{ .parent.child }}` wraps a VRL path.
- strftime specifiers such as `%Y/%m/%d` or `%F`, taken from the event's timestamp field (rename it with the global `timestamp_key` option).

Example partitioning S3 by application and date:

```yaml
sinks:
  backup:
    type: aws_s3
    bucket: all_application_logs
    key_prefix: "application_id={{ application_id }}/date=%F/"
```

An event with `application_id: 1` and a timestamp of 2020-02-14 yields `application_id=1/date=2020-02-14`. Because the sink batches, events are grouped by the rendered value, which gives dynamic partitioning.

Escaping: prefix with a backslash, `\{{ field_name }}` or `\%Y`, to treat the text literally (inside double-quoted YAML strings the percent form needs `\\%Y`).

Fallbacks: templates have no fallback syntax. Set defaults first in a `remap`:

```coffeescript
if !exists(.my_field) {
  .my_field = "default"
}
```

Missing fields: if a referenced field is missing, Vector logs an error and drops the event, and increments `component_errors_total` with `error_type` `template_failed`.

Verify by sending an event without the field and checking that metric.

## Checked

2026-11-03. Read reference/configuration/template-syntax. Confirmed: field references with VRL paths, strftime specifiers from the `timestamp_key` field, the S3 `key_prefix` example and its result, batching by rendered value, backslash escaping with the doubled form in double-quoted YAML, and that a missing field logs an error, drops the event and increments `component_errors_total` with `error_type` `template_failed`. Nothing removed. The 'no fallback syntax' advice is a consequence of the page's syntax list.

Method: documentation only; no commands were run.
