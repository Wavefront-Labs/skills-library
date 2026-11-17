---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-logical-and-or
name: rego-logical-and-or
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, logical-and, logical-or, in-operator, control-flow]
level: intro
status: docs-checked
description: "Express AND with statements in one rule body and OR with multiple rules, functions or the in operator in Rego, using the official cheat sheet patterns."
sources:
  - https://www.openpolicyagent.org/docs/cheatsheet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write boolean logic the Rego way.

AND: statements in a rule body are joined with logical AND; all must hold.

```rego
valid_staff_email if {
    regex.match(`^\S+@\S+\.\S+$`, input.email) # and
    endswith(input.email, "example.com")
}
```

OR has three idioms.

Multiple rules with the same name:

```rego
valid_email if endswith(input.email, "@example.com")
valid_email if endswith(input.email, "@example.org")
valid_email if endswith(input.email, "@example.net")
```

Functions with several definitions, including literal arguments:

```rego
allowed_firstname(name) if {
    startswith(name, "a")
    count(name) > 2
}

allowed_firstname("joe") # if name == 'joe'

valid_name if allowed_firstname(input.name)
```

The `in` operator against a set:

```rego
valid_request if {
    input.method in {"GET", "POST"}
}
```

Prefer `in` when the alternatives are values of one expression; prefer separate rules when each alternative needs different supporting statements. The Policy Language page also describes `and` and `or` keywords for one rule body (for example `input.user.admin or input.user.owner`); both need an import (`future.keywords.and` or `future.keywords.or`, or rego.v2), neither produces a value, and incremental rules remain the idiom when the disjunction must contribute a value.

Check with the cheat sheet inputs: `{"email": "opa@example.com", "name": "anna", "method": "GET"}` makes `valid_email`, `valid_name` and `valid_request` all true, and changing `method` to `PUT` leaves only `valid_request` undefined.

## Checked

2026-11-04. Confirmed against the OPA docs Cheat Sheet, sections Logical AND and Logical OR (the code in this skill reproduces them, including the cheat sheet input) and the Policy Language page section And and Or Keywords. Replaced a bare statement that there is no || with the documented and/or keywords and their import requirement. The preference advice (in versus separate rules) is the skill's own.

Method: documentation only; no commands were run.
