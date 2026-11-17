---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-functions
name: rego-functions
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, functions, user-defined-functions, arity, function-conflicts]
level: practitioner
status: docs-checked
description: "Define user-defined Rego functions, how multiple definitions match by argument, conflict and undefined results, and why overloading by arity fails."
sources:
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse logic with functions that behave like built-ins.

```rego
package functions

trim_and_split(s) := x if {
    t := trim(s, " ")
    x := split(t, ".")
}

result := trim_and_split("   foo.bar ")
```

Functions take any number of inputs of any term kind, return exactly one output, and can read both `data` and `input`.

Multiple definitions: a call executes every definition whose signature matches. Arguments can be literals, so definitions can pattern-match:

```rego
r(1, x) := y if { y := x }
r(x, 2) := y if { y := x*4 }
result := r(1, 2)
```

Both definitions match `r(1, 2)` and produce different values (2 and 4), so this raises a conflict error. Matching definitions must agree on the output.

If no definition matches, for instance `s(5, 3)` against `s(x, 2)`, the result is undefined, not an error.

Overloading by parameter count is not supported. Two definitions of `r` with one and two parameters give a compile-time type error. If you must keep one name, take a single array parameter and branch on `count(params)`, but the docs advise against it because it loses compile-time checking and is error-prone. Prefer distinct names.

Functions can be given a fallback with `default` (see rego-default-keyword); a default function still fails if any argument is undefined.

Check: call the function with a matching and a non-matching argument and confirm the second is undefined.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Language page, section Functions: user-defined functions with access to data and input, the trim_and_split example, any number of inputs and exactly one output, conflict error for multiple output bindings, incremental definitions, all matching definitions executing and needing the same output, undefined when nothing matches, no overloading by parameter count (compile-time type error), the single-array workaround and the page's advice against it. Fixed an arithmetic error: r(x, 2) with x = 1 gives 1*4 = 4, not 8. The default-function sentence agrees with the Default Keyword section.

Method: documentation only; no commands were run.
