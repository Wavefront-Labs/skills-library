---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-jsonata-variables-and-data-flow
name: step-functions-jsonata-variables-and-data-flow
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, jsonata, sfn-variables, intrinsic-functions-sfn, jsonpath, data-flow, asl]
level: practitioner
status: docs-checked
description: "Shape data in Step Functions with JSONata (Arguments, Output, Assign) and workflow variables, or JSONPath with intrinsic functions, and stay inside payload limits."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/workflow-variables.html", "https://docs.aws.amazon.com/step-functions/latest/dg/transforming-data.html", "https://docs.aws.amazon.com/step-functions/latest/dg/intrinsic-functions.html", "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions data flow: JSONata, variables, JSONPath

**Goal:** pass exactly the data each state needs, without five layers of
`InputPath/Parameters/ResultSelector/ResultPath/OutputPath` and without a "formatting Lambda".

## 1. Turn on JSONata
Top level `"QueryLanguage": "JSONata"` (or per state to migrate gradually). Then each state has
just two data fields: `Arguments` (what goes to the task) and `Output` (what leaves the
state), plus `Assign` for variables. Expressions live in `"{% ... %}"`.

Reserved `$states`: `$states.input`, `$states.result` (task result, in `Output`/`Assign`),
`$states.errorOutput` (in Catch), `$states.context` (execution/task metadata, e.g.
`$states.context.Execution.Id`, `$states.context.Task.Token`).

```json
"GetCustomer": {
  "Type": "Task",
  "Resource": "arn:aws:states:::dynamodb:getItem",
  "Arguments": {"TableName": "customers", "Key": {"pk": {"S": "{% $states.input.customerId %}"}}},
  "Assign": {"customerTier": "{% $states.result.Item.tier.S %}"},
  "Output": "{% $states.input %}",
  "Next": "Price"
},
"Price": {
  "Type": "Pass",
  "Output": {"total": "{% $sum($states.input.lines.(qty * price)) * ($customerTier = 'gold' ? 0.9 : 1) %}",
             "orderedAt": "{% $now() %}"},
  "End": true
}
```

## 2. Variables
- `Assign` sets variables after the state runs; any later state reads `$name`.
- All assignments in one `Assign` are evaluated against the values *before* that assign.
- Scope is workflow-local: Parallel branches and Map iterations can read outer variables but keep their own variables, and an inner scope cannot assign a name already assigned in an outer scope. A Catch `Assign` can assign in the outer scope. Variables inside Parallel/Map go out of scope when it finishes, so pass data out via `Output`. Distributed Map cannot reference outer-scope variables.
- `Assign` and `Output` are evaluated in parallel: a value you compute in `Assign` is not in `Output` unless you apply the expression there too.
- Limits: 256 KiB per variable, 256 KiB per `Assign` block, 10 MiB total per execution.
- Variables work in JSONPath states too (`"x.$": "$customerTier"`), except in `ResultPath`. Variable names follow Unicode identifier rules, up to 80 characters; you cannot assign to part of a variable (`x.y`).

## 3. JSONPath and intrinsic functions (JSONPath states only)
Order: `InputPath` → `Parameters` → task → `ResultSelector` → `ResultPath` → `OutputPath`.
Intrinsics (JSONPath states only; not available in JSONata states) usable in Pass `Parameters` and in Task, Parallel and Map `Parameters`/`ResultSelector`, nestable up to 10 deep:
`States.Format('order {}', $.id)`, `States.StringToJson`, `States.JsonToString`,
`States.Array`, `States.ArrayPartition($.items, 50)`, `States.ArrayContains`,
`States.ArrayRange`, `States.ArrayGetItem`, `States.ArrayLength`, `States.ArrayUnique`,
`States.Base64Encode/Decode`, `States.Hash($.x, 'SHA-256')` (MD5, SHA-1, SHA-256, SHA-384, SHA-512), `States.JsonMerge($.a, $.b, false)` (shallow merge only),
`States.MathRandom`, `States.MathAdd`, `States.StringSplit`, `States.UUID()`.

## Gotchas
- JSONata `Output`, when specified, overrides the default state output — forget to include `$states.input` and the
  next state loses its keys. (JSONPath's equivalent bug is `ResultPath` default `$`.)
- A JSONata expression that evaluates to *undefined* (or has a type, range, memory or one-second time-limit problem) fails the state with
  `States.QueryEvaluationError`, which Task, Map and Parallel states can Catch or Retry; guard optional fields with `$exists()` or defaults.
- JSONata offers `$partition`, `$range`, `$hash`, `$random`, `$uuid` and `$parse` as replacements for intrinsics; `$eval` is not available.
- Payload limit is 256 KiB per state input/output; store big data in S3 and pass the key. Over the limit raises `States.DataLimitExceeded`.
- Mixing languages: `QueryLanguage` (top level, default JSONPath, or per state) selects the fields; a JSONata state cannot use `InputPath`/`Parameters`/`ResultSelector`/`ResultPath`/`OutputPath`, and JSONPath states cannot use `Arguments`/`Output`; validate with Workflow Studio or `validate-state-machine-definition` before deploy.

## Verify
- [ ] `aws stepfunctions validate-state-machine-definition --definition file://asl.json` returns `OK`.
- [ ] `test-state` on each transformed state (with `--inspection-level DEBUG`) shows the intended output and variables.
- [ ] No state's output exceeds a few KiB in a realistic run (check execution history sizes).

## Checked
Checked 2026-10-24 against the Step Functions developer guide (variables, transforming data with JSONata, intrinsic functions, error handling, service quotas).
Confirmed: QueryLanguage field and defaults, Arguments/Output/Assign, $states members, Assign evaluation order and parallel evaluation with Output, variable limits (256 KiB, 256 KiB per Assign, 10 MiB per execution), scope rules, JSONPath variable use, field order InputPath to OutputPath, intrinsic function list, hash algorithms, JsonMerge shallow-only, JSONata replacement functions, States.QueryEvaluationError, 256 KiB payload limit.
Corrected: the earlier text said inner scopes cannot assign outer variables without noting the Catch exception and the same-name rule.

Method: documentation only; no commands were run.
