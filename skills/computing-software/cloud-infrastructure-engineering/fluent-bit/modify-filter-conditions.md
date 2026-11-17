---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.modify-filter-conditions
name: modify-filter-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, modify-filter, conditions, key-exists, key-value-matches, regex]
level: advanced
status: docs-checked
description: "Gate every rule of a modify filter instance with conditions such as Key_exists and Key_value_matches."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/modify"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modify filter conditions

Conditions decide whether the rules of a `modify` instance run. They apply to the whole filter instance and all its rules, not to individual rules, and every condition must be true for any rule to apply. Condition names are case-insensitive, parameters are not. Nested keys may use the record accessor syntax.

| Condition | True when |
| --- | --- |
| `Key_exists KEY` | `KEY` exists |
| `Key_does_not_exist KEY` | `KEY` is absent |
| `A_key_matches REGEX` | some key matches the regular expression |
| `No_key_matches REGEX` | no key matches |
| `Key_value_equals KEY VALUE` | `KEY` exists and equals `VALUE` |
| `Key_value_does_not_equal KEY VALUE` | `KEY` exists and differs |
| `Key_value_matches KEY REGEX` | the value of `KEY` matches |
| `Key_value_does_not_match KEY REGEX` | the value does not match |
| `Matching_keys_have_matching_values KEY_REGEX VALUE_REGEX` | all keys matching the first pattern have values matching the second |
| `Matching_keys_do_not_have_matching_values KEY_REGEX VALUE_REGEX` | all matching keys have non-matching values |

```yaml
pipeline:
  filters:
    - name: modify
      match: '*'
      Condition: Key_Value_Equals level error
      Add: alert true
```

Because conditions are shared, use separate `modify` filters when different rules need different conditions.

## Checked

2026-11-03. Confirmed on the Fluent Bit Modify filter page (Conditions): all ten conditions, instance-wide scope, all conditions must be true, record accessor for nested keys, and the Condition usage in YAML. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
