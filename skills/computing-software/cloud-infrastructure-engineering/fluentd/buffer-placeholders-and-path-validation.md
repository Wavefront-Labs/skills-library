---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-placeholders-and-path-validation
name: buffer-placeholders-and-path-validation
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buffer, placeholders, chunk-id, path-traversal, out-file]
level: practitioner
status: docs-checked
description: "Use chunk-key placeholders (${tag}, ${tag[1]}, strptime, ${key}, ${chunk_id}) in output params and the v1.19.3 path boundary validation."
sources:
  - https://docs.fluentd.org/configuration/buffer-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd buffer placeholders
When chunk keys are set, plugins that call `extract_placeholders` can use them in parameters such as `path`:

- `${tag}`; `${tag[1]}` is the second tag part (zero-origin).
- With `time` key: `%Y`, `%m`, `%d`, `%H`, `%M`, `%S`, giving the first second of the timekey range.
- `${key1}` for a record-field key; nested: `${$.nest.field}` with `<buffer tag,$.nest.field>`.
- `${chunk_id}` needs no chunk key; useful for `secondary_file`, `s3`.

```
<match log.*>
  @type file
  path /data/${tag[1]}/access.%Y-%m-%d.%H%M.log
  <buffer tag,time>
    timekey 1m
  </buffer>
</match>
```
Referencing a key not listed in the chunk keys is a configuration error.

**Path boundary validation (since v1.19.3)**: values substituted into `${tag}` or `${key}` are rejected if they contain `../` or `..\` or start with `/` or `\`, which stops an event from making `out_file` write outside its directory. This raises `Fluent::UnrecoverableError`, so the chunk is not retried but moved to `secondary` or the backup directory. It also catches a bad component formed only after substitution. A `../` written in the config itself is unaffected, and a tag with `../` is harmless where no placeholder is used.

## Checked

2026-11-04. Confirmed against the Fluentd Config: Buffer Section page (docs.fluentd.org/configuration/buffer-section), Placeholders, Path Boundary Validation and Chunk ID sections. Nothing removed.

Method: documentation only; no commands were run.
