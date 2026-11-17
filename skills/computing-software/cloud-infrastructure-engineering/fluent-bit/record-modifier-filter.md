---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.record-modifier-filter
name: record-modifier-filter
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, record-modifier, allowlist-key, remove-key, uuid-key, environment-variables]
level: practitioner
status: docs-checked
description: "Append fixed fields, add a UUID, or keep and remove keys with the record_modifier filter."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/record-modifier"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Record modifier filter

The `record_modifier` filter appends fields to a record or removes specific ones.

| Key | Meaning |
| --- | --- |
| `record` | append a field; needs a key/value pair |
| `remove_key` | remove the field if the key matches; use this or `allowlist_key` |
| `allowlist_key` | remove every field whose key does not match; `whitelist_key` is an alias |
| `uuid_key` | append a UUID to each record under this key |

The docs append a product name and a host name taken from an environment variable:

```yaml
pipeline:
  inputs:
    - name: mem
      tag: mem.local
  filters:
    - name: record_modifier
      match: '*'
      record:
        - hostname ${HOSTNAME}
        - product Awesome_Tool
  outputs:
    - name: stdout
      match: '*'
```

To drop fields, repeat `remove_key` (for example for `Swap.total`), or keep only a few with repeated `allowlist_key`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Record modifier page: record, remove_key, allowlist_key, whitelist_key alias and uuid_key, and the hostname and product example. Removed: an unsourced filter-choice rule and verification step.

Method: documentation only; no commands were run.
