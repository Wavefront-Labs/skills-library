---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-expressions-operators-references
name: grafana-alloy-expressions-operators-references
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [expressions, operators, component-references, access-operators, string-concatenation, comparison-operators]
level: practitioner
status: docs-checked
description: "Alloy expression operators, precedence, null versus error on missing members, and referencing component exports from arguments."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/expressions/operators.md", "https://github.com/grafana/alloy/blob/main/docs/sources/get-started/expressions/referencing_exports.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Operators and component references

## References
Reference an export as `<component name>.<label>.<export>`: `local.file.target.content`, `prometheus.remote_write.onprem.receiver`. References may appear only in component arguments or config block fields, and a component cannot reference itself. The controller evaluates the referenced component first, resolves the export, and checks the value type matches the attribute. Each time the export changes, dependents are reevaluated.

```alloy
prometheus.scrape "default" {
  targets    = [{ "__address__" = local.file.target.content }]
  forward_to = [prometheus.remote_write.onprem.receiver]
}
```

## Operators (PEMDAS order)
- Arithmetic: `+ - * / % ^`.
- Strings: `+` concatenates two strings, two secrets, or a string and a secret.
- Comparison: `== != < <= > >=`. Equality works on any operands; ordering needs orderable operands of the same type. Strings compare byte-wise.
- Logical: `&&`, `||`, `!`.
- Brackets: `{ }` blocks/objects, `( )` grouping, `[ ]` arrays.

Conditionals are expressed as booleans, for example `remote_write_enabled = sys.env("ENVIRONMENT") == "production"`.

## Assignment rules
`null` can be assigned to any attribute; numbers convert implicitly to string attributes; strings convert to number attributes if they look numeric; blocks cannot be assigned.

## Access
`obj["app"]` or `arr[1]` (zero-indexed) versus `obj.app` and component exports. Gotcha: `[ ]` on a missing member returns `null`, but `.` on a missing member raises an error.

## Checked

2026-11-08. Read the Operators and Component exports pages in full. Confirmed: reference format and placement limits, no self reference, evaluation and reevaluation, type compatibility, PEMDAS ordering, arithmetic, string, comparison (including byte-wise strings), logical and bracket operators, the assignment rules, and the difference between `[ ]` and `.` on missing members.

Method: documentation only; no commands were run.
