---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.rewrite-tag-rules
name: rewrite-tag-rules
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, rewrite-tag, routing, tag-rewrite, regex-capture, keep]
level: advanced
status: docs-checked
description: "Write rewrite_tag rules in KEY REGEX NEW_TAG KEEP form to re-emit records under a new tag for routing."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/rewrite-tag"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rewrite tag rules

The `rewrite_tag` filter re-emits a record under a new tag; the new record enters the pipeline from the start, and the original is kept or discarded. Rules are processed in order until one matches. A rule that does not match is skipped.

Rule format, in the `rule` key:

```text
$KEY  REGEX  NEW_TAG  KEEP
```

- **KEY**: record key prefixed with `$`; nested keys use `$ss['s1']['s2']`. The value must be a string, not a number, Boolean, map or array.
- **REGEX**: pattern on that value. Capture groups become `$0`, `$1`, `$2`. For `abc-123` and `^([a-z]+)-([0-9]+)$`: `$1` is `abc`, `$2` is `123`.
- **NEW_TAG**: characters `a-z A-Z 0-9 . - ,` plus placeholders for the original tag (`$TAG`, `$TAG[1]`), captures, record keys and environment variables such as `${HOSTNAME}`.
- **KEEP**: `true` keeps the original record in the pipeline, `false` discards it. Mandatory, no default.

```yaml
pipeline:
  filters:
    - name: rewrite_tag
      match: test_tag
      rule: $tool ^(fluent)$  from.$TAG.new.$tool.$sub['s1']['s2'].out false
      emitter_name: re_emitted
  outputs:
    - name: stdout
      match: from.*
```

This turns tag `test_tag` into `from.test_tag.new.fluent.bit.out`. Route on the new tag with an output `match`.

Make sure the filter's `match` cannot match the tags it produces; otherwise the emitted records loop back to the same filter. Fluent Bit detects this, rejects the emission and logs an error, keeping the triggering record under its original tag.

## Checked

2026-11-03. Confirmed on the Fluent Bit Rewrite tag page: rule format, KEY, REGEX and capture placeholders, NEW_TAG characters and placeholders, mandatory KEEP, in-order matching, the from.test_tag.new.fluent.bit.out example, and emitter cycle detection. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
