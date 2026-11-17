---
id: computing-software.devops-ci-cd.forgejo.workflow-expressions-and-operators
name: workflow-expressions-and-operators
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [expressions, workflow-context, logical-operators, forgejo-ref-name]
level: practitioner
status: docs-checked
description: "Use ${{ }} expressions, literals, operators and context variables such as forgejo.ref_name in workflows."
sources:
  - https://forgejo.org/docs/latest/user/actions/basic-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Expressions look like `${{ ... }}` and are evaluated by the runner. In fields such as `if:` the `${{ }}` wrapper is implicit and can be omitted.

The docs warn that implicit boolean conversions are hard to reason about when passed to action inputs or outputs; for easier debugging use explicit strings such as `'yes'` or `'no'` rather than `true` or `'true'`.

Variables read the workflow context, for example `${{ forgejo.ref_name }}` yields the branch name. The workflow reference lists all context values.

Literals: boolean (`true`, `false`), `null`, number (any JSON number format) and string (single quotes).

Operators: `( )` grouping, `[ ]` index, `.` property dereference, `!`, `<`, `<=`, `>`, `>=`, `==`, `!=`, `&&` and `||`. String comparisons are case insensitive.

When functions cast to strings, `null` becomes the empty string, booleans become `'true'` or `'false'`, numbers use decimal format (exponential if large), and arrays and objects are never converted.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Actions | Basic concepts" page, read in full (Expressions, Variables, Literals, Logical operators and the conversion table): the `${{ ... }}` syntax and implicit wrapper in fields like `if:`, the boolean-conversion note, `${{ forgejo.ref_name }}`, the literal types, the operator table, case-insensitive string comparison, and the string conversions.
Corrected: nothing needed; every claim matched the page text. Note that the page's operator table is titled "Logical operators" although it lists comparison and access operators too.
Method: documentation only; no commands were run.
