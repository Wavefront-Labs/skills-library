---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.rego-rule-types
name: rego-rule-types
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rego, rules, partial-set, partial-object, complete-rule, incremental-definition]
level: practitioner
status: docs-checked
description: "Choose between single-value, multi-value set and multi-value object Rego rules, how incremental definitions union, and when complete rules conflict."
sources:
  - https://www.openpolicyagent.org/docs/policy-language
  - https://www.openpolicyagent.org/docs/cheatsheet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the rule form that yields the document shape you need.

All rules have the form `<name> <key>? <value>? <body>?`.

Single-value (complete) rules omit the key and assign one value; the body defaults to true if omitted:

```rego
pi := 3.14159
```

Multi-value set rules use `contains`:

```rego
hostnames contains name if {
    name := sites[_].servers[_].hostname
}
```

Multi-value object rules have key and value in the head:

```rego
apps_by_hostname[hostname] := app if { ... }
paths_by_prefix[prefix] contains path if { ... }  # object of sets
```

Incremental definition: the same rule name defined several times produces the union of the results, read as `rule-1 OR rule-2 OR ... OR rule-N`. Use it to abstract over several data sources, such as servers and containers both contributing to `instances`.

Complete rules can hold only one value at a time. If two definitions fire with different values (for example `max_memory := 32 if power_users[user]` and `max_memory := 4 if restricted_users[user]` while the user is in both sets) OPA returns a conflict error. Object comprehensions and object rules likewise may not produce conflicting entries.

A complete rule can also be undefined; use the `default` keyword (see rego-default-keyword) when a fallback is needed.

Check: query `data.<package>` and confirm each rule has the type you intended (set, object or scalar).

## Checked

2026-11-04. Confirmed against the OPA docs Policy Language page, section Rules: the head form <name> <key>? <value>? <body>?, generating sets with contains, generating objects, leaf partial sets under object keys (users_by_country[country] contains user.id), incremental definitions as a union read as rule-1 OR rule-2, the instances example over servers and containers, complete definitions with a body that defaults to true, the max_memory conflict example, undefined complete rules and the default keyword. Removed the request_quota example, which the page does not contain. The paths_by_prefix line is an illustration of the object-of-sets shape the page shows with users_by_country.

Method: documentation only; no commands were run.
