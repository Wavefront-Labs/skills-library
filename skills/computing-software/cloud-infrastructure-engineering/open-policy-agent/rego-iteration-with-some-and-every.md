---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-iteration-with-some-and-every
name: rego-iteration-with-some-and-every
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, some, every, iteration, universal-quantification]
level: practitioner
status: docs-checked
description: "Iterate collections in Rego with some ... in to name variables and every ... { } to require a condition on all elements, with a worked allow rule."
sources:
  - https://www.openpolicyagent.org/docs/cheatsheet
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: loop over collections and quantify over them.

`some` names local query variables and iterates. For arrays it yields elements; with two variables it yields key/index and value:

```rego
allowed_regions contains region_id if {
    some area, regions in all_regions
    some region in regions
    region_id := sprintf("%s_%s", [area, region])
}
```

The body runs once for every combination, adding one `region_id` each time. This is existential: the rule fires if some binding makes the body true.

`every` is universal. It succeeds only if the body holds for every element:

```rego
allow if {
    prefix := sprintf("/docs/%s/", [input.userID])
    every path in input.paths {
        startswith(path, prefix)
    }
}
```

With `userID` `u123`, paths `/docs/u123/notes.txt` and `/docs/u123/q4-report.docx` pass; one path outside the prefix makes `allow` undefined. An empty collection satisfies `every` trivially, (the docs: if the domain is empty, the statement is true), so add a `count(input.paths) > 0` check when emptiness should deny.

`every` does not introduce new bindings into the rule. Negating it is forbidden; write `not every x in xs { p(x) }` as `some x in xs; not p(x)`.

Check: add a test with one non-matching path and an empty list, and confirm the first is denied and the second behaves as you intend.

## Checked

2026-11-04. Confirmed against the OPA docs Cheat Sheet (Some and Every examples, which the code in this skill reproduces) and the Policy Language page sections Some Keyword and Every Keyword: some ... in with one or two variables, existential search for a solution, every over array, object and set domains, the statement undefined if one binding fails, true for an empty domain, no new bindings from every, and the ban on negating every with the some/not rewrite. The count(input.paths) > 0 advice and the Check line are the skill's own suggestions. Nothing removed.

Method: documentation only; no commands were run.
