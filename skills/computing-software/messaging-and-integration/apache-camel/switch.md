---
id: computing-software.messaging-and-integration.apache-camel.switch
name: switch
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, switch, routing, case-table]
level: practitioner
status: docs-checked
description: "Camel Switch EIP (4.23+): literal case table with selector, case-insensitive matching, otherwise fallback, and when to use Choice or toD."
sources:
  - https://camel.apache.org/components/next/eips/switch-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switch (since Camel 4.23)

Routes each exchange to one destination from a literal case table.

Options: `selector` (required; evaluated once per entry, must return a scalar), `case` (list of literals; duplicate values are rejected at startup), `otherwise` (fixed fallback URI), `disabled` (default `false`).

Matching:
- Scalars are converted to strings and matched case-insensitively.
- An empty string is a valid literal; `*` is literal, not a wildcard.
- Map, collection or array results throw `IllegalArgumentException` and do not select `otherwise`.
- Null or unmatched results use `otherwise`; without it processing continues after the Switch.
- Selector failures follow normal error handling and never select the fallback.

Versus others: Switch has no inline steps, each case sends to one endpoint (link branches with `direct:` or SEDA). Use Choice for predicates, ranges, overlaps or nested processing; use toD when the URI must be computed at runtime.

```java
doSwitch(header("department"))
    .doCase("billing", "direct:billing")
    .otherwise("direct:review")
```
XML uses `<switch>` with `<selector>`, `<case value="..." uri="..."/>` and `<otherwise uri="..."/>`.

Case values and URIs support property placeholders resolved at startup (values are lower-cased after resolution); Simple expressions in URIs are rejected. Management reports selection counts and `UnmatchedCount`; counts reflect selection, not delivery. Output body is unknown.

Verify: department `Billing` (capitalised) still reaches `direct:billing`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Switch EIP page source (switch-eip.adoc) and the Switch model definition (switch.json) from the apache/camel repository, which generate the cited page. Confirmed since 4.23, selector required and evaluated once, scalar conversion and case-insensitive matching, empty string and literal asterisk, duplicate rejection at startup, IllegalArgumentException for map, collection and array results, otherwise and null handling, error handling, placeholders and lower-casing, management counts and UnmatchedCount, unknown output body, and the Choice and toD guidance. Nothing was removed. No commands were run.
