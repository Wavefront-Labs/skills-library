---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-choice-wait-parallel-and-pass-states
name: step-functions-choice-wait-parallel-and-pass-states
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, choice-state, parallel-state, wait-state, pass-state, amazon-states-language]
level: practitioner
status: docs-checked
description: "Use Step Functions flow states well: Choice rules and defaults, Wait by seconds or timestamp, Parallel branches with error handling, and Pass for shaping data."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/state-choice.html", "https://docs.aws.amazon.com/step-functions/latest/dg/state-wait.html", "https://docs.aws.amazon.com/step-functions/latest/dg/state-parallel.html", "https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions flow states

Examples use JSONata (`"QueryLanguage": "JSONata"` at the top of the definition); the
JSONPath equivalents use `Variable`/`StringEquals` style operators.

## 1. Choice
```json
"RouteOrder": {
  "Type": "Choice",
  "Choices": [
    {"Condition": "{% $states.input.total > 1000 and $states.input.country = 'GB' %}", "Next": "ManualReview"},
    {"Condition": "{% $exists($states.input.coupon) %}", "Next": "ApplyCoupon"}
  ],
  "Default": "Fulfil"
}
```
- Rules are evaluated in order and the first match wins; always set `Default`, otherwise an input that matches nothing makes the state machine fail to transition out of the state.
- Choice cannot have `Retry`/`Catch` and does not run work; it only routes.
- JSONPath variant: `{"Variable": "$.total", "NumericGreaterThan": 1000, "Next": ...}`,
  combinators `And`/`Or`/`Not`, presence tests `IsPresent`, type tests `IsNumeric`.

## 2. Wait
```json
"Cooldown": {"Type": "Wait", "Seconds": 300, "Next": "Retry"},
"UntilSendTime": {"Type": "Wait", "Timestamp": "{% $states.input.sendAt %}", "Next": "Send"}
```
- Exactly one of `Seconds` (0 to 99,999,999), `Timestamp` (RFC 3339 profile: uppercase `T`, and an uppercase `Z` instead of a numeric offset; milliseconds are truncated), or in JSONPath states `SecondsPath`/`TimestampPath`. JSONata states accept expressions in `Seconds`/`Timestamp`.
- The maximum wait is one year in Standard workflows and five minutes in Express workflows.

## 3. Parallel
```json
"Enrich": {
  "Type": "Parallel",
  "Branches": [
    {"StartAt": "GetCustomer", "States": {"GetCustomer": {"Type": "Task", "Resource": "arn:aws:states:::dynamodb:getItem", "Arguments": {...}, "End": true}}},
    {"StartAt": "GetRisk", "States": {"GetRisk": {"Type": "Task", "Resource": "arn:aws:states:::lambda:invoke", "Arguments": {...}, "End": true}}}
  ],
  "Output": "{% {'customer': $states.result[0], 'risk': $states.result[1].Payload} %}",
  "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "EnrichFailed"}],
  "Next": "Decide"
}
```
- Output is an **array** in branch order.
- If any branch fails (uncaught inside the branch), the whole Parallel fails and other
  branches are stopped. Put Retry/Catch inside branches for partial-failure tolerance.
- For a dynamic number of items use Map (or Distributed Map), not Parallel.

## 4. Pass
```json
"Defaults": {"Type": "Pass", "Output": "{% $merge([{'priority': 'normal'}, $states.input]) %}", "Next": "RouteOrder"}
```
Use Pass to inject constants, reshape input, set variables (`"Assign": {"orderId":
"{% $states.input.id %}"}`), or stub states during development. It costs a state
transition like any state.

## 5. Gotchas
- Standard workflows are billed per state transition (and throttled by the state transition quota); Express workflows are billed by executions, duration and memory.
- Payload limit is 256 KiB between states; pass S3 references for large data.
- Mixing JSONPath and JSONata: set the query language per state if needed; field names
  differ (`Parameters`/`ResultSelector` vs `Arguments`/`Output`).

## Verify
- [ ] `aws stepfunctions validate-state-machine-definition --definition file://sm.asl.json` returns no errors.
- [ ] TestState API exercises each Choice branch including Default.
- [ ] Parallel failure in one branch routes to the Catch path in a test execution.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (Choice, Wait, Parallel states, service quotas, workflow type comparison).
Confirmed: Choice rule order, Default behaviour, JSONata Condition and JSONPath comparison operators (And, Or, Not, IsPresent, IsNumeric), Wait field set, range, RFC 3339 timestamp format and one-year/five-minute maxima, Parallel output array in branch order, failure of one branch stopping the others, Arguments/Output in JSONata states, 256 KiB payload limit, billing basis per workflow type.
Corrected: Wait timestamps do not accept numeric offsets. Removed the unreferenced States.NoChoiceMatched error name and the claim that Wait is a cheap scheduler.

Method: documentation only; no commands were run.
