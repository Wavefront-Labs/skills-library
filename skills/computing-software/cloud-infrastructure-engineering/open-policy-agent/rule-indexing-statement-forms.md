---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rule-indexing-statement-forms
name: rule-indexing-statement-forms
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rule-indexing, performance, glob-match, startswith, membership]
level: sme
status: docs-checked
description: "Which Rego statements OPA's rule indexer can index: equality, glob.match, startswith and any_prefix_match, in, bare references, with concrete yes/no examples."
sources:
  - https://www.openpolicyagent.org/docs/policy-performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let OPA pick the few rules that can match instead of evaluating all of them.

Within the linear fragment OPA indexes rules, sometimes making evaluation constant time as the policy grows. Statements must take an indexable shape.

Equality (`=`, `==`): one side a non-nested reference with no variables, the other a variable, scalar or array. Indexed: `input.x == "foo"`, `input.x[_] == "foo"`, `input.x[input.y] == "foo"` (ground prefix `input.x`). Not indexed: `input.x[i].y == "foo"` (variable is not the last element) and `input.x[i] == ["foo"]`.

Glob: `glob.match("foo:*:bar", [":"], input.x)` is indexed. Not indexed: `**` in the pattern, a variable in the match, `*` embedded in a segment (`"a*"`), or a `null` delimiter.

Prefix and suffix: `startswith(input.path, "/api")`, `endswith(input.path, ".gz")` and `strings.any_prefix_match(input.path, ["/a", "/b"])` are indexed using a radix trie, so lookup cost does not grow with the number of prefixes. Not indexed: a base only known at evaluation (`startswith(input.path, input.prefix)`), `input.path[i]` as the search value, or capturing the result (`x := startswith(...); x == true`).

Membership: `input.role in {"admin", "user"}` and `"admin" in input.roles` are indexed when the value is a scalar. Not indexed: non-scalar values and the three-operand `some k, v in input.obj; v == "admin"`.

Bare reference used as a boolean check: `input.x` and `input.x.y` are indexed, `input.x[i]` is not. A lookup such as `data.groups.admins.members[input.subject]` into base data is indexed on its last element.

Practical rule (the skill's own advice, not stated on the page): keep each rule's discriminating conditions as simple comparisons on `input` references; the page does not say their position in the body matters.

Check: run `opa eval --profile` and confirm unrelated rules show zero evaluations.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Performance page, section Use indexed statements: the equality table (input.x, input.x[i] and input.x[_] and input.x[input.y] indexed on the ground prefix, input.x[i].y and input.x[i] == ["foo"] not indexed), the glob table (** , variable in the match, embedded * and null delimiter not indexed), prefix and suffix statements with the radix trie and the not-indexed list, membership with scalar values and the three-operand in, and bare references. Added the bare-reference line the description promised. The page also documents and/or statements, several values for one reference and local-variable resolution, which this skill does not cover. The Check line is a suggested exercise.

Method: documentation only; no commands were run.
