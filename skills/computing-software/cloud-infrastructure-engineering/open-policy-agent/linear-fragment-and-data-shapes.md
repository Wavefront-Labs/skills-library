---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.linear-fragment-and-data-shapes
name: linear-fragment-and-data-shapes
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [performance, linear-fragment, objects-over-arrays, low-latency, rego-optimisation]
level: advanced
status: docs-checked
description: "Write Rego in the linear fragment for near constant-time decisions and replace id-searched arrays with objects keyed by id, per the OPA performance guide."
sources:
  - https://www.openpolicyagent.org/docs/policy-performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: meet a latency budget (the docs cite about 1 millisecond for microservice authorisation) as the policy grows.

The linear fragment is a subset of Rego engineered to evaluate in near constant time: adding more rules does not significantly increase evaluation time. The docs give this example: the rule has one local variable `user` that can only be assigned one value. Intuitively, evaluating it means checking each condition in the body, and with N such rules evaluation only walks over each of them:

```rego
package linear

allow if {
    some user
    input.method == "GET"
    input.path = ["accounts", user]
    input.user == user
}
```

The cost is no larger than the size of the policy. OPA still lets you write non-linear policies when you need them, but evaluation cost then grows with policy size.

Use objects over arrays. Searching an array of records for an id scans every element:

```rego
# bad: searches all elements
d := [{"id": "a123", "first": "alice", "last": "smith"}]
d[i].id == "a789"
```

Key the data by id instead and the lookup needs no search:

```rego
d := {"a123": {"first": "alice", "last": "smith"},
      "a789": {"first": "clarice", "last": "johnson"}}
d["a789"].first
```

For large membership checks the same advice applies: `"admin" in input.roles` walks the collection, so prefer an object and `input.roles["admin"]`.

Next steps for a policy that still misses its budget: shape statements so the rule indexer can use them (see rule-indexing-statement-forms) and profile with `opa eval --profile`.

Check: benchmark before and after the restructure with the profiler and confirm lower evaluation counts.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Performance page: the 1 millisecond budget example, the linear fragment and its example rule, use objects over arrays, the linear-time cost statement and the note that non-linear policies are allowed, and the advice to prefer an object over `in` on a large collection. Replaced the claim that a rule qualifies when its variables each take one value with the page's more cautious wording (the page calls it intuition from one example, not a qualification test).

Method: documentation only; no commands were run.
