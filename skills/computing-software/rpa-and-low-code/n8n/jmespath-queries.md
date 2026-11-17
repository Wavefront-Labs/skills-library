---
id: computing-software.rpa-and-low-code.n8n.jmespath-queries
name: jmespath-queries
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, jmespath, json, projections, code-node, expressions]
level: practitioner
status: docs-checked
description: "Query JSON in n8n with $jmespath(object, searchString): argument order gotcha, JavaScript-only caveat, list, slice and object projections and Python equivalents."
sources:
  - https://docs.n8n.io/build/work-with-data/handle-special-data-types/query-json-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: extract or reshape JSON with JMESPath.

n8n adds `$jmespath(object, searchString)`. It wraps the JavaScript library, so the argument order is `search(object, searchString)`, the reverse of the order in the JMESPath specification examples. Available in expressions and the JavaScript Code node, not in Python (use plain Python). The longer form `require('jmespath').search(object, searchString)` does not work in expressions because they must be single-line. Try the examples with the Code node **Mode** set to **Run Once for Each Item**.

Given webhook data with `body.people` (`first`, `last`) and `body.dogs` (`Fido`, `Spot` each with `color` and `age`):
```js
{{$jmespath($json.body.people, "[*].first" )}}    // ["James","Jacob","Jayden"]  list projection
{{$jmespath($json.body.people, "[:2].first")}}    // ["James","Jacob"]            slice projection
{{$jmespath($json.body.dogs, "*.age")}}           // [7,5]                         object projection
```
In the Code node:
```js
let dogsAges = $jmespath($json.body.dogs, "*.age");
return {dogsAges};
```
Python equivalent:
```python
dogs = _item["json"]["body"]["dogs"]
dogs_ages = [dog["age"] for dog in dogs.values()]
return {"dogsAges": dogs_ages}
```
JMESPath supports five projection kinds: list, slice, object, flatten and filter.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/work-with-data/handle-special-data-types/query-json-data

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
