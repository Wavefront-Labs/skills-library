---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-else-keyword
name: rego-else-keyword
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, else, rule-ordering, first-match, iptables-porting]
level: advanced
status: docs-checked
description: "Chain Rego rules with else so evaluation stops at the first match, the ordered-evaluation construct for porting policy from iptables-like systems."
sources:
  - https://www.openpolicyagent.org/docs/policy-language
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: express order-sensitive, first-match-wins policy in Rego.

Rego rules normally combine as a union with no order. The `else` keyword is the control-flow exception: rules grouped by `else` are evaluated in sequence until a match is found, and rules further down the chain are not evaluated once one matches.

```rego
package else_example

authorize := "allow" if {
    input.user == "superuser"           # allow 'superuser' to perform any operation.
} else := "deny" if {
    input.path[0] == "admin"            # disallow 'admin' operations...
    input.source_network == "external"  # from external networks.
} # ... more rules
```

Here a superuser is allowed before the deny branch is ever considered. The docs recommend it when porting policies from an order-sensitive system such as iptables, where the first matching line decides.

Guidance (the skill author's advice; the docs only describe the else behaviour, the iptables use and the example):
- Reach for ordinary incremental rules plus `default` first; they are easier to reason about and test.
- Use `else` only when order is the actual requirement, and put the most specific branch first.
- Add a final `else := "deny"` style branch or a `default` so the chain cannot be undefined.

Check: write one test per branch with `with input as ...`, including an input matching two branches, and confirm the earlier branch wins.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Language page, section Else Keyword: rules grouped with else are evaluated until a match, later rules in the chain are not evaluated after a match, the iptables porting use, and the superuser/alice example. The bulleted guidance and the Check line are the skill's own advice and are not stated on the page. Nothing removed.

Method: documentation only; no commands were run.
