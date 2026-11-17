---
id: computing-software.rpa-and-low-code.n8n.expressions-data-transformation
name: expressions-data-transformation
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, expressions, edit-fields, iife, luxon, credentials-expressions]
level: practitioner
status: docs-checked
description: "Write n8n expressions: prefer Edit Fields for transforms, read webhook body fields, use expressions in credentials, multi-statement IIFEs and fix the three common errors."
sources:
  - https://docs.n8n.io/build/work-with-data/transform-data/expressions-for-data-transformation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: transform data with expressions without cluttering node parameters.

Best practice: prepare data once in an **Edit Fields (Set)** node (add fields from expressions, modify, remove, rename) and pass the result on, rather than scattering complex expressions across nodes. To build one, switch the field to expression mode and drag values from the **INPUT** pane or type them.

## Webhook body
With a Webhook item shaped `{headers, params, query, body: {name, age, city}}`, `{{$json.body.city}}` returns the city; `{{$json['body']['city']}}` is equivalent.

## Credentials
Expression-mode credential fields work too, for example `{{ $('Webhook').item.json.headers.authorization }}`. They are evaluated per execution, so executions do not share data.

## Multiple statements
Variable assignment needs an Immediately Invoked Function Expression inside the braces:
```js
{{(()=>{
  let end = DateTime.fromISO('2017-03-13');
  let start = DateTime.fromISO('2017-02-13');
  let diffInMonths = end.diff(start, 'months');
  return diffInMonths.toObject();
})()}}
```
(uses Luxon `DateTime`.)

## Common errors
- `The 'JSON Output' in item 0 contains invalid JSON` (or `does not contain a valid JSON object`): JSON mode got invalid JSON, or referenced fields missing from some input items. Validate with a JSON checker.
- `Can't get data for expression` / `Referenced node is unexecuted`: the referenced node has not run; test up to it. In code you can guard with `$("<node-name>").isExecuted`. `$input.params` also errors when the step is not connected.
- `Invalid syntax`: for example a trailing period in `{{ $('If').item.json. }}`.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/work-with-data/transform-data/expressions-for-data-transformation

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
