---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-comprehensions
name: rego-comprehensions
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, comprehensions, array-comprehension, set-comprehension, object-comprehension]
level: practitioner
status: docs-checked
description: "Build arrays, sets and objects from sub-queries in Rego with comprehension syntax, outer-variable binding, grouping, and the object key conflict rule."
sources:
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a collection from a sub-query, typically to group or aggregate.

A comprehension has a head and a body. The body is one or more expressions that must all be true; each time it is true, the head produces an element.

Forms:
- array: `[ <term> | <body> ]`
- object: `{ <key>: <term> | <body> }`
- set: `{ <term> | <body> }`

```rego
package comprehensions

region := "west"
names := [name | sites[i].region == region; name := sites[i].name]

app_to_hostnames := {app.name: hostnames |
    app := apps[_]
    hostnames := [hostname |
        name := app.servers[_]
        s := sites[_].servers[_]
        s.name == name
        hostname := s.hostname]
}

my_set := {e | some e in [1, 1, 2, 2, 3, 3]}
```

The body can refer to variables bound in the outer body (`region` above). In the docs the `sites` and `apps` names come from `import data.example.sites` and `import data.example.apps`. OPA reorders expressions in the outer body so those variables are bound before the comprehension runs.

Arrays keep duplicates and order; sets drop duplicates. Object comprehensions may not have conflicting entries: `{"foo": i | some i in [1, 2]}` is an error because one key would have two values.

Typical uses are grouping elements by key and computing aggregates such as the number of containers on a host (wrap the comprehension in `count`).

Check: evaluate the comprehension on its own with `opa eval -d policy.rego data.comprehensions.names` and confirm the element count before using it in a rule.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Language page, section Comprehensions: head and body, outer-variable reference with expression reordering, grouping and aggregate use, the array, object and set forms and examples, and the rule that object comprehensions may not have conflicting entries. Noted the imports the docs examples rely on. The statement that arrays keep duplicates and sets drop them is general Rego behaviour that the page's set example (a set built from [1, 1, 2, 2, 3, 3]) illustrates but does not state in words. The Check line is a suggested exercise.

Method: documentation only; no commands were run.
