---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-default-keyword
name: rego-default-keyword
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, default, deny-by-default, undefined, fallback-value]
level: practitioner
status: docs-checked
description: "Use Rego default to give complete rules and functions a fallback so allow is false instead of undefined, with the restrictions on default values."
sources:
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a rule return a definite value when every definition is undefined.

```rego
package example

default allow := false

allow if {
    input.user == "bob"
    input.method == "GET"
}
```

With `{"user": "bob", "method": "GET"}`, `allow` is true. With any other input, `allow` is `false`. Without the `default` line the document is undefined for the same input.

Syntax is restricted to `default <name> := <term>`. The term can be a scalar, a composite, or a comprehension, but not a variable or reference, and a composite may not contain variables or references. Comprehensions may, because a comprehension result is never undefined.

Functions can have defaults too:

```rego
default clamp_positive(_) := 0

clamp_positive(x) := x if {
    x > 0
}
```

A default function must have the same arity as the other definitions of that name, use only plain variables as arguments (no composite values), and not repeat argument names.

Gotcha: a default function still fails to evaluate, even to the default, if any argument in the call is undefined, because arguments are evaluated before the call and an undefined argument stops evaluation there.

Use `default allow := false` in every authorisation package so the integration never sees undefined for the decision rule.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Language page, section Default Keyword: default for complete definitions, the bob/GET example, the restricted syntax default <name> := <term>, the term restrictions and the comprehension exception, default functions (clamp_positive), the three function conditions (same arity, plain variable arguments, no repeated names) and the undefined-argument note. Removed the unsupported remark about how callers treat an undefined result; the closing recommendation is the skill's own advice, not a docs requirement.

Method: documentation only; no commands were run.
