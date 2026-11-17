---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-with-keyword
name: rego-with-keyword
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, with, what-if-queries, input-override, data-override]
level: practitioner
status: docs-checked
description: "Use the Rego with modifier to evaluate a rule under a different input, data or built-in, to ask what-if questions and to stack several overrides in one expression."
sources:
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: evaluate a rule as if the input, data or a function were different.

`with` is a modifier on an expression. It sets values nested under `input`, under `data`, or replaces built-in functions, for that expression only. An expression may carry zero or more `with` modifiers.

```rego
package authz

import data.examples.allow

result := true if {
    allow with input as {"user": "alice", "method": "POST"}
}

result := true if {
    not allow with input as {"user": "bob", "method": "DELETE"}
}
```

Stack several overrides, including data and time:

```rego
result := true if {
    allow with input as {"user": "catherine", "method": "GET"}
        with data.roles as {"dev": ["bob"]}
        with time.weekday as "Sunday"
}
```

Typical uses:
- unit tests and what-if checks (see mocking-data-and-functions-with-with)
- asking whether a hypothetical request would be allowed, from another policy
- replacing a clock or lookup function so a policy is deterministic

Remember `not allow with input as {...}` negates the whole expression including the override, so it asserts the rule is undefined for that input.

Check: run the query with the override and with a different override and confirm the result changes while the real `input` is untouched.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Language page, section With Keyword: with sets values nested under input or data or replaces built-in functions, applies to the attached expression only, zero or more modifiers per expression, and the examples (alice POST, bob DELETE with not, the dev role override, catherine on Sunday with time.weekday). Nothing removed. The page also lists restrictions on targets and function replacements that are covered in mocking-data-and-functions-with-with.

Method: documentation only; no commands were run.
